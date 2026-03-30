"""
Move analysis module.
Evaluates positions and finds best moves using Stockfish engine.
"""

import chess
from chess.engine import Cp, Mate
import os


class MoveAnalyzer:
    """Analyzes chess positions and finds best moves."""
    
    def __init__(self, stockfish_path=None):
        """
        Initialize the move analyzer.
        
        Args:
            stockfish_path (str, optional): Path to Stockfish executable.
                                           If None, tries to find it automatically.
        """
        self.engine = None
        self.stockfish_path = stockfish_path
        self._load_engine()
    
    def _load_engine(self):
        """Load the Stockfish engine."""
        import chess.engine
        
        if self.stockfish_path and os.path.exists(self.stockfish_path):
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            except Exception as e:
                print(f"Error loading Stockfish from {self.stockfish_path}: {e}")
                self.engine = None
        else:
            # Try common paths
            common_paths = [
                "stockfish",  # Linux/Mac
                "stockfish.exe",  # Windows
                "/usr/bin/stockfish",  # Linux
                "/usr/local/bin/stockfish",  # Mac
                "C:\\Program Files\\stockfish\\stockfish.exe",  # Windows
            ]
            
            for path in common_paths:
                try:
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    self.stockfish_path = path
                    break
                except:
                    continue
    
    def is_engine_available(self):
        """
        Check if Stockfish engine is available.
        
        Returns:
            bool: True if engine loaded successfully
        """
        return self.engine is not None
    
    def set_engine_path(self, path):
        """
        Set a new path for Stockfish engine and reload it.
        
        Args:
            path (str): Path to Stockfish executable
            
        Returns:
            bool: True if engine loaded successfully
        """
        if self.engine:
            self.engine.quit()
        self.stockfish_path = path
        self._load_engine()
        return self.is_engine_available()
    
    def evaluate_position(self, board, depth=15):
        """
        Evaluate the current position.
        
        Args:
            board (chess.Board): The board to evaluate
            depth (int): Search depth for engine
            
        Returns:
            dict: Evaluation info with 'score', 'mate_in', and 'best_move'
        """
        if not self.engine:
            return {"error": "Stockfish engine not available"}
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            
            result = {}
            
            # Get score
            if "score" in info:
                score = info["score"]
                if isinstance(score.white(), Mate):
                    result["mate_in"] = score.white().moves
                else:
                    result["score"] = score.white().cp / 100  # Convert to pawns
            
            # Get best move
            if "pv" in info and len(info["pv"]) > 0:
                result["best_move"] = info["pv"][0].uci()
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_best_moves(self, board, top_n=3, depth=15):
        """
        Get the top best moves for a position.
        
        Args:
            board (chess.Board): The board to analyze
            top_n (int): Number of top moves to return
            depth (int): Search depth for engine
            
        Returns:
            list: List of dicts with move, score, and evaluation
        """
        if not self.engine:
            return []
        
        try:
            # Analyze all legal moves
            moves_with_scores = []
            
            for move in list(board.legal_moves)[:20]:  # Limit to speed up
                board.push(move)
                info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
                board.pop()
                
                if "score" in info:
                    score = info["score"]
                    if isinstance(score.white(), Mate):
                        eval_score = 10000 if score.white().moves > 0 else -10000
                    else:
                        eval_score = -score.white().cp / 100  # Flip perspective
                    
                    moves_with_scores.append({
                        "move": move.uci(),
                        "san": board.san(move),
                        "score": eval_score
                    })
            
            # Sort by score and return top N
            moves_with_scores.sort(key=lambda x: x["score"], reverse=True)
            return moves_with_scores[:top_n]
        except Exception as e:
            print(f"Error analyzing moves: {e}")
            return []
    
    def is_move_best(self, board, move_uci, depth=15, tolerance=0.5):
        """
        Check if a move is among the best moves for the position.
        
        Args:
            board (chess.Board): The board state
            move_uci (str): Move to evaluate in UCI format
            depth (int): Search depth for engine
            tolerance (float): Tolerance in pawns for "good" moves
            
        Returns:
            dict: Result with 'is_best', 'evaluation', and 'best_move'
        """
        if not self.engine:
            return {"error": "Stockfish engine not available"}
        
        try:
            # Evaluate current position
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            best_move = info["pv"][0].uci() if "pv" in info else None
            
            # Evaluate position after the move
            board.push_uci(move_uci)
            move_info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            board.pop()
            
            if "score" in move_info:
                score = move_info["score"]
                if isinstance(score.white(), Mate):
                    move_eval = 10000
                else:
                    move_eval = -score.white().cp / 100
            else:
                return {"error": "Could not evaluate move"}
            
            # Get best move evaluation
            if best_move:
                board.push_uci(best_move)
                best_info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
                board.pop()
                
                if "score" in best_info:
                    best_score = best_info["score"]
                    if isinstance(best_score.white(), Mate):
                        best_eval = 10000
                    else:
                        best_eval = -best_score.white().cp / 100
                else:
                    best_eval = move_eval
            else:
                best_eval = move_eval
            
            return {
                "move": move_uci,
                "evaluation": move_eval,
                "best_move": best_move,
                "best_evaluation": best_eval,
                "is_best": move_uci == best_move,
                "is_good": abs(move_eval - best_eval) <= tolerance
            }
        except Exception as e:
            return {"error": str(e)}
    
    def quit(self):
        """Close the Stockfish engine."""
        if self.engine:
            self.engine.quit()
