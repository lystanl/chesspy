#!/usr/bin/env python3
"""
Demo script for Chess Tutor Puzzle System.
Shows how to use the puzzle solver and board display.
"""

from board import ChessBoard
from puzzle_solver import PuzzleSolver
from move_analyzer import MoveAnalyzer


def demo_puzzle_flow():
    """Demonstrate the puzzle solving flow."""
    print("\n" + "="*60)
    print("CHESS TUTOR - PUZZLE SYSTEM DEMO".center(60))
    print("="*60)
    
    # Initialize components
    solver = PuzzleSolver()
    
    print(f"\nTotal puzzles available: {len(solver.get_all_puzzles())}\n")
    
    # Show all puzzles
    print("-"*60)
    print("AVAILABLE PUZZLES:".center(60))
    print("-"*60)
    for puzzle in solver.get_all_puzzles():
        status = "[SOLVED]" if solver.is_puzzle_solved(puzzle["id"]) else "[NOT SOLVED]"
        print(f"ID {puzzle['id']:<2} | {puzzle['name']:<30} | {puzzle['difficulty']:<8} | {status}")
    
    print("\n" + "-"*60)
    print("PUZZLE #1 DEMO".center(60))
    print("-"*60 + "\n")
    
    # Get first puzzle
    puzzle = solver.get_puzzle_by_id(1)
    print(f"Puzzle: {puzzle['name']}")
    print(f"Difficulty: {puzzle['difficulty']}")
    print(f"Description: {puzzle['description']}\n")
    print(f"Best move(s): {', '.join(puzzle['best_moves'])}\n")
    
    # Initialize board with puzzle position
    board = ChessBoard(puzzle["fen"])
    print("BOARD POSITION:")
    board.display_fancy()
    
    # Simulate some moves
    test_moves = [
        ("d2d4", "Testing center control move"),
        ("d2d3", "Testing alternative move"),
    ]
    
    print("\n" + "-"*60)
    print("MOVE VALIDATION TEST:".center(60))
    print("-"*60 + "\n")
    
    for move, description in test_moves:
        is_correct = puzzle["fen"] == solver.get_puzzle_by_id(1)["fen"]
        is_best = move in puzzle['best_moves']
        
        print(f"Move: {move}")
        print(f"  Description: {description}")
        print(f"  Is best move? {is_best}")
        
        # Test board move validation
        board_copy = ChessBoard(puzzle["fen"])
        legal = board_copy.make_move(move)
        print(f"  Legal? {legal}\n")
    
    # Show progress tracking
    print("-"*60)
    print("PROGRESS TRACKING:".center(60))
    print("-"*60 + "\n")
    
    # Simulate solving puzzle 1
    solver.mark_puzzle_solved(1)
    solver.record_attempt(1, "d2d4", True)
    
    progress = solver.get_progress()
    print(f"Puzzles solved: {progress['solved_puzzles']}/{progress['total_puzzles']}")
    print(f"Progress: {progress['progress_percentage']:.1f}%")
    
    # Show all puzzles again
    print("\n" + "-"*60)
    print("PUZZLES STATUS (AFTER SOLVING #1):".center(60))
    print("-"*60 + "\n")
    
    for puzzle in solver.get_all_puzzles():
        status = "[OK]" if solver.is_puzzle_solved(puzzle["id"]) else "[ ]"
        print(f"#{puzzle['id']} {status} {puzzle['name']:<30} ({puzzle['difficulty']})")
    
    print("\n" + "="*60)
    print("DEMO COMPLETE".center(60))
    print("="*60 + "\n")


def demo_board_display():
    """Demonstrate fancy board display."""
    print("\n" + "="*60)
    print("BOARD DISPLAY DEMO".center(60))
    print("="*60 + "\n")
    
    # Standard starting position
    print("1. STANDARD STARTING POSITION:")
    board = ChessBoard()
    board.display_fancy()
    
    print("\n2. AFTER 1.e4:")
    board.make_move("e2e4")
    board.display_fancy()
    
    print("\n3. AFTER 1...c5:")
    board.make_move("c7c5")
    board.display_fancy()
    
    print("\n4. UNDO TEST:")
    board.undo_move()
    print("(After undoing Black's move)")
    board.display_fancy()


def demo_puzzle_categories():
    """Show puzzles organized by difficulty."""
    print("\n" + "="*60)
    print("PUZZLES BY DIFFICULTY".center(60))
    print("="*60 + "\n")
    
    solver = PuzzleSolver()
    
    for difficulty in ["Easy", "Medium", "Hard"]:
        puzzles = [p for p in solver.get_all_puzzles() if p["difficulty"] == difficulty]
        
        print(f"\n{difficulty.upper()} ({len(puzzles)} puzzles):")
        print("-" * 40)
        for puzzle in puzzles:
            print(f"  #{puzzle['id']:<2} {puzzle['name']}")
            print(f"      {puzzle['description']}")


if __name__ == "__main__":
    # Run all demos
    demo_puzzle_flow()
    demo_board_display()
    demo_puzzle_categories()
    
    print("\n" + "="*60)
    print("To start the interactive puzzle solver, run: python main.py")
    print("="*60 + "\n")
