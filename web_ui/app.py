"""
Chess Tutor Web UI - Flask Backend
Provides REST API endpoints for interactive puzzle solving via web interface
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
from puzzle_solver import PuzzleSolver
from board import ChessBoard
from move_analyzer import MoveAnalyzer
import chess

app = Flask(__name__)

# Initialize puzzle solver and analyzer
puzzle_solver = PuzzleSolver()
move_analyzer = MoveAnalyzer()

# Track current state
current_board = None
current_puzzle = None


@app.route('/')
def index():
    """Serve main web UI"""
    return render_template('index.html')


@app.route('/api/puzzle/current', methods=['GET'])
def get_current_puzzle():
    """Get current puzzle details"""
    global current_puzzle, current_board
    
    puzzle = puzzle_solver.get_current_puzzle()
    if not puzzle:
        return jsonify({'error': 'No puzzle available'}), 404
    
    current_puzzle = puzzle
    current_board = ChessBoard(puzzle['fen'])
    
    progress = puzzle_solver.get_progress()
    
    return jsonify({
        'id': puzzle['id'],
        'name': puzzle['name'],
        'difficulty': puzzle['difficulty'],
        'description': puzzle['description'],
        'fen': puzzle['fen'],
        'best_moves': puzzle['best_moves'],
        'board_display': current_board.display(),
        'board_fancy': current_board.display_fancy(),
        'legal_moves': [move.uci() for move in current_board.board.legal_moves],
        'progress': progress,
        'is_solved': puzzle_solver.is_puzzle_solved(puzzle['id'])
    })


@app.route('/api/puzzle/next', methods=['POST'])
def next_puzzle():
    """Move to next puzzle"""
    if puzzle_solver.next_puzzle():
        return get_current_puzzle()
    else:
        return jsonify({'error': 'No more puzzles'}), 404


@app.route('/api/puzzle/previous', methods=['POST'])
def previous_puzzle():
    """Move to previous puzzle"""
    if puzzle_solver.previous_puzzle():
        return get_current_puzzle()
    else:
        return jsonify({'error': 'No previous puzzle'}), 404


@app.route('/api/puzzle/select/<int:puzzle_id>', methods=['POST'])
def select_puzzle(puzzle_id):
    """Select specific puzzle"""
    if puzzle_solver.select_puzzle(puzzle_id):
        return get_current_puzzle()
    else:
        return jsonify({'error': f'Puzzle {puzzle_id} not found'}), 404


@app.route('/api/move/validate', methods=['POST'])
def validate_move():
    """Validate and execute move"""
    global current_board, current_puzzle
    
    if not current_board or not current_puzzle:
        return jsonify({'error': 'No puzzle loaded'}), 400
    
    data = request.json
    move_uci = data.get('move', '')
    
    # Check if move is legal
    try:
        move = chess.Move.from_uci(move_uci)
        if move not in current_board.board.legal_moves:
            return jsonify({
                'valid': False,
                'message': 'Illegal move',
                'is_solution': False,
                'legal_moves': [m.uci() for m in current_board.board.legal_moves]
            }), 400
    except ValueError:
        return jsonify({
            'valid': False,
            'message': 'Invalid move format',
            'is_solution': False
        }), 400
    
    # Check if it's the solution
    is_solution = puzzle_solver.is_solution_correct(move_uci)
    
    # Record attempt
    puzzle_solver.record_attempt(current_puzzle['id'], move_uci, is_solution)
    
    # Execute the move
    current_board.make_move(move_uci)
    
    response = {
        'valid': True,
        'move': move_uci,
        'is_solution': is_solution,
        'message': 'Correct! Well done!' if is_solution else 'Not the best move. Try again or get hints.',
        'board_display': current_board.display(),
        'board_fancy': current_board.display_fancy(),
        'legal_moves': [m.uci() for m in current_board.board.legal_moves],
        'game_over': current_board.is_game_over()
    }
    
    if is_solution:
        puzzle_solver.mark_puzzle_solved(current_puzzle['id'])
        response['progress'] = puzzle_solver.get_progress()
    
    return jsonify(response)


@app.route('/api/move/hints', methods=['GET'])
def get_hints():
    """Get hint moves"""
    global current_board
    
    if not current_board:
        return jsonify({'error': 'No puzzle loaded'}), 400
    
    if not move_analyzer.is_engine_available():
        # Return legal moves if no engine
        return jsonify({
            'hints': [m.uci() for m in list(current_board.board.legal_moves)[:5]],
            'engine_available': False,
            'message': 'Stockfish not available. Showing legal moves instead.'
        })
    
    try:
        best_moves = move_analyzer.get_best_moves(current_board.board, top_n=5)
        hints = []
        for move, score in best_moves:
            hints.append({
                'move': move.uci(),
                'score': float(score.white().cp) / 100 if score.white().cp else 0
            })
        
        return jsonify({
            'hints': hints,
            'engine_available': True,
            'message': 'Top 5 moves from Stockfish analysis'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'engine_available': False
        }), 500


@app.route('/api/board/undo', methods=['POST'])
def undo_move():
    """Undo last move"""
    global current_board
    
    if not current_board:
        return jsonify({'error': 'No puzzle loaded'}), 400
    
    if current_board.undo_move():
        return jsonify({
            'success': True,
            'board_display': current_board.display(),
            'board_fancy': current_board.display_fancy(),
            'legal_moves': [m.uci() for m in current_board.board.legal_moves]
        })
    else:
        return jsonify({'error': 'No moves to undo'}), 400


@app.route('/api/board/reset', methods=['POST'])
def reset_board():
    """Reset board to puzzle start"""
    global current_puzzle, current_board
    
    if not current_puzzle:
        return jsonify({'error': 'No puzzle loaded'}), 400
    
    current_board = ChessBoard(current_puzzle['fen'])
    
    return jsonify({
        'success': True,
        'board_display': current_board.display(),
        'board_fancy': current_board.display_fancy(),
        'legal_moves': [m.uci() for m in current_board.board.legal_moves]
    })


@app.route('/api/puzzles/list', methods=['GET'])
def list_puzzles():
    """List all puzzles"""
    puzzles = puzzle_solver.get_all_puzzles()
    solved = puzzle_solver.solved_puzzles
    
    puzzle_list = []
    for puzzle in puzzles:
        puzzle_list.append({
            'id': puzzle['id'],
            'name': puzzle['name'],
            'difficulty': puzzle['difficulty'],
            'solved': puzzle['id'] in solved
        })
    
    return jsonify({'puzzles': puzzle_list})


@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get player progress"""
    progress = puzzle_solver.get_progress()
    return jsonify(progress)


if __name__ == '__main__':
    print("🐴 Chess Tutor Web UI Starting...")
    print("📺 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
