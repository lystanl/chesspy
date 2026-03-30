"""
Chess board management and display module.
Handles board state, display, and move validation.
"""

import chess


class ChessBoard:
    """Represents a chess board and manages board state."""
    
    def __init__(self, fen=None):
        """
        Initialize a chess board.
        
        Args:
            fen (str, optional): FEN string to load a specific position.
                                If None, initializes standard starting position.
        """
        if fen:
            self.board = chess.Board(fen)
        else:
            self.board = chess.Board()
    
    def display(self):
        """
        Print the current board state in a human-readable format.
        Shows rank numbers and file letters for reference.
        """
        print("\n  a b c d e f g h")
        print("  ---------------")
        for rank in range(7, -1, -1):
            print(f"{rank + 1} ", end="")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    print(f"{piece} ", end="")
                else:
                    print(". ", end="")
            print(f" {rank + 1}")
        print("  ---------------")
        print("  a b c d e f g h\n")
    
    def display_fancy(self):
        """
        Print the board with a fancy border display.
        Better for puzzle presentation.
        """
        board_str = "\n"
        board_str += "    ┌─────────────────────┐\n"
        
        for rank in range(7, -1, -1):
            board_str += f"  {rank + 1} │ "
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    board_str += f"{piece} "
                else:
                    # Checkerboard pattern with . or ·
                    if (rank + file) % 2 == 0:
                        board_str += "· "
                    else:
                        board_str += "· "
            board_str += f"│ {rank + 1}\n"
        
        board_str += "    ├─────────────────────┤\n"
        board_str += "    │ a b c d e f g h │\n"
        board_str += "    └─────────────────────┘\n"
        
        print(board_str)
    
    def make_move(self, move_uci):
        """
        Make a move on the board.
        
        Args:
            move_uci (str): Move in UCI format (e.g., 'e2e4')
            
        Returns:
            bool: True if move was valid and made, False otherwise
            
        Raises:
            ValueError: If the move format is invalid
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if move not in self.board.legal_moves:
                return False
            self.board.push(move)
            return True
        except ValueError:
            return False
    
    def undo_move(self):
        """
        Undo the last move.
        
        Returns:
            bool: True if a move was undone, False if no moves to undo
        """
        if self.board.move_stack:
            self.board.pop()
            return True
        return False
    
    def get_legal_moves(self):
        """
        Get all legal moves in the current position.
        
        Returns:
            list: List of moves in UCI format
        """
        return [move.uci() for move in self.board.legal_moves]
    
    def is_game_over(self):
        """
        Check if the game is over (checkmate or stalemate).
        
        Returns:
            bool: True if game is over
        """
        return self.board.is_game_over()
    
    def get_game_status(self):
        """
        Get the current game status.
        
        Returns:
            str: Description of game status (checkmate, stalemate, ongoing, etc.)
        """
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_check():
            return "Check"
        else:
            return "Ongoing"
    
    def reset(self, fen=None):
        """
        Reset the board to a new position.
        
        Args:
            fen (str, optional): FEN string for new position.
                                If None, resets to starting position.
        """
        if fen:
            self.board = chess.Board(fen)
        else:
            self.board = chess.Board()
    
    def to_fen(self):
        """
        Get the current board position as FEN string.
        
        Returns:
            str: FEN representation of current position
        """
        return self.board.fen()
