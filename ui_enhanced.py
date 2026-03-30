"""
Enhanced User Interface for Chess Tutor.
Improved puzzle display and interactive solving mode.
"""

from board import ChessBoard
from puzzle_solver import PuzzleSolver
from move_analyzer import MoveAnalyzer


class ChessTutorUI:
    """Command-line interface for the chess tutor."""
    
    def __init__(self):
        """Initialize the UI and all game components."""
        self.puzzle_solver = PuzzleSolver()
        self.analyzer = MoveAnalyzer()
        self.board = None
        self.show_engine_warning()
    
    def show_engine_warning(self):
        """Warn user if Stockfish engine is not available."""
        if not self.analyzer.is_engine_available():
            print("\nWARNING: Stockfish engine not found!")
            print("Move analysis will be limited.")
            print("Download Stockfish from: https://stockfishchess.org/download/")
            path = "stockfish/stockfish-windows-x86-64-avx2"
            if path:
                if self.analyzer.set_engine_path(path):
                    print("Stockfish loaded successfully!\n")
                else:
                    print("Failed to load Stockfish from that path.\n")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("CHESS TUTOR - PUZZLE SOLVER".center(60))
        print("="*60)
        print("\n1. Start solving puzzles")
        print("2. List all puzzles")
        print("3. View progress")
        print("4. Quit")
        print("\nEnter your choice (1-4): ", end="")
    
    def display_puzzle_header(self):
        """Display the puzzle header with progress info."""
        progress = self.puzzle_solver.get_progress()
        puzzle = self.puzzle_solver.get_current_puzzle()
        
        if not puzzle:
            return
        
        print("\n" + "-"*60)
        print(f"PUZZLE {progress['current_puzzle_index']}/{progress['total_puzzles']} - "
              f"{puzzle.get('difficulty', 'Unknown')}")
        print("-"*60)
    
    def show_puzzle(self):
        """Display the current puzzle and board."""
        puzzle = self.puzzle_solver.get_current_puzzle()
        if not puzzle:
            print("No puzzle selected!")
            return False
        
        # Reset board to puzzle position
        self.board = ChessBoard(puzzle["fen"])
        
        self.display_puzzle_header()
        self.display_puzzle_board()
        
        return True
    
    def display_puzzle_board(self):
        """Display puzzle board with description and prompt."""
        puzzle = self.puzzle_solver.get_current_puzzle()
        if not puzzle:
            return
        
        print(f"\nPuzzle: {puzzle.get('name', 'Unnamed')}")
        print(f"Description: {puzzle.get('description', 'Find the best move!')}\n")
        
        # Display whose turn it is
        is_white_turn = self.board.board.turn
        print(f"{'WHITE' if is_white_turn else 'BLACK'} TO MOVE\n")
        
        # Display board
        print("BOARD POSITION:")
        self.board.display_fancy()
        
        print("-"*60)
        print("MOVE INPUT:")
        print("  Format: UCI notation (e.g., e2e4, e7e8q)")
        print("  Commands: 'h'=hints, 'b'=undo, 'n'=next, 'p'=prev, 'q'=quit")
        print("-"*60)
        print("Enter your move: ", end="")
    
    def list_puzzles(self):
        """Display all available puzzles."""
        puzzles = self.puzzle_solver.get_all_puzzles()
        
        print("\n" + "="*70)
        print("AVAILABLE PUZZLES".center(70))
        print("="*70)
        print(f"{'ID':<5} {'Name':<30} {'Difficulty':<15} {'Status':<5}")
        print("-"*70)
        
        for puzzle in puzzles:
            puzzle_id = puzzle.get("id", "?")
            name = puzzle.get("name", "Unnamed")[:28]
            difficulty = puzzle.get("difficulty", "Unknown")
            status = "[OK]" if self.puzzle_solver.is_puzzle_solved(puzzle_id) else "[ ]"
            print(f"{puzzle_id:<5} {name:<30} {difficulty:<15} {status:<5}")
        
        print("-"*70)
        print(f"\nEnter puzzle ID to select (or press Enter to go back): ", end="")
        choice = input().strip()
        
        if choice:
            try:
                if self.puzzle_solver.select_puzzle(int(choice)):
                    print(f"Selected puzzle {choice}")
                else:
                    print(f"Puzzle {choice} not found!")
            except ValueError:
                print("Invalid puzzle ID!")
    
    def get_hints(self):
        """Show hints for the current puzzle."""
        if not self.analyzer.is_engine_available():
            print("\nEngine not available - cannot show hints")
            return
        
        if not self.board:
            return
        
        puzzle = self.puzzle_solver.get_current_puzzle()
        print("\n[ANALYZING POSITION...]")
        
        best_moves = self.analyzer.get_best_moves(self.board.board, top_n=3)
        
        if not best_moves:
            print("Could not analyze position\n")
            return
        
        print("\nHINTS - Top moves:")
        for i, move_info in enumerate(best_moves, 1):
            print(f"  {i}. {move_info['san']:<6} (score: {move_info['score']:>6.2f})")
        
        print(f"\nPuzzle solution(s): {', '.join(puzzle.get('best_moves', []))}\n")
    
    def process_move(self, move_input):
        """
        Process a player's move input.
        
        Args:
            move_input (str): The move in UCI format or command
        """
        if move_input.lower() == 'h':
            self.get_hints()
            return False
        elif move_input.lower() == 'b':
            if self.board.undo_move():
                print("\nMove undone.\n")
            else:
                print("\nNo moves to undo.\n")
            return False
        elif move_input.lower() == 'n':
            if self.puzzle_solver.next_puzzle():
                print("\nMoving to next puzzle...\n")
                return "next_puzzle"
            else:
                print("\nAlready on last puzzle.\n")
            return False
        elif move_input.lower() == 'p':
            if self.puzzle_solver.previous_puzzle():
                print("\nMoving to previous puzzle...\n")
                return "prev_puzzle"
            else:
                print("\nAlready on first puzzle.\n")
            return False
        elif move_input.lower() == 'q':
            return "quit"
        
        # Try to make the move
        if not move_input or len(move_input) < 4:
            print("\nInvalid move format. Use UCI (e.g., e2e4)\n")
            return False
        
        if self.board.make_move(move_input):
            puzzle = self.puzzle_solver.get_current_puzzle()
            
            # Check if it's the correct move
            if self.puzzle_solver.is_solution_correct(move_input):
                print("\n" + "="*60)
                print("[CORRECT!]".center(60))
                print("="*60)
                print(f"Move '{move_input}' is one of the best moves!")
                print("="*60 + "\n")
                
                self.puzzle_solver.mark_puzzle_solved(puzzle["id"])
                self.puzzle_solver.record_attempt(puzzle["id"], move_input, True)
                self.board.display_fancy()
                
                if not self.puzzle_solver.next_puzzle():
                    print("\n" + "="*60)
                    print("[PUZZLE SET COMPLETE!]".center(60))
                    print("You've solved all puzzles!".center(60))
                    print("="*60 + "\n")
                    return "puzzle_complete"
                else:
                    print("Press Enter for next puzzle...")
                    input()
                    return "next_puzzle"
            else:
                best_moves = puzzle.get("best_moves", [])
                print(f"\n[INCORRECT] Not the best move.")
                print(f"Best move(s): {', '.join(best_moves)}\n")
                
                self.puzzle_solver.record_attempt(puzzle["id"], move_input, False)
                self.board.display_fancy()
                
                # Give suggestion
                if self.analyzer.is_engine_available():
                    print("Analyzing better alternatives...")
                    best_moves_list = self.analyzer.get_best_moves(self.board.board, top_n=1)
                    if best_moves_list:
                        best = best_moves_list[0]
                        print(f"Suggested move: {best['san']} (score: {best['score']:.2f})\n")
                else:
                    print()
        else:
            print("\nIllegal move or invalid format.\n")
        
        return False
    
    def show_progress(self):
        """Display player's progress."""
        progress = self.puzzle_solver.get_progress()
        
        print("\n" + "="*60)
        print("YOUR PROGRESS".center(60))
        print("="*60)
        print(f"Puzzles Solved: {progress['solved_puzzles']}/{progress['total_puzzles']}")
        print(f"Progress: {progress['progress_percentage']:.1f}%")
        print(f"Current Puzzle: {progress['current_puzzle_index']}")
        print("="*60)
    
    def show_help(self):
        """Display help information."""
        print("\n" + "="*60)
        print("HELP - KEYBOARD COMMANDS".center(60))
        print("="*60)
        print("\nMove Input Format: UCI notation")
        print("  Examples: e2e4, e7e8q, a1h8")
        print("\nPuzzle Commands:")
        print("  'h' - Show hints (top moves)")
        print("  'b' - Undo last move")
        print("  'n' - Skip to next puzzle")
        print("  'p' - Go to previous puzzle")
        print("  'q' - Quit to main menu")
        print("="*60)
    
    def run(self):
        """Run the main game loop."""
        print("\n" + "="*60)
        print("WELCOME TO CHESS TUTOR!".center(60))
        print("="*60)
        
        while True:
            self.display_menu()
            choice = input().strip()
            
            if choice == "1":
                self.puzzle_solver.current_puzzle_index = 0
                while True:
                    if not self.show_puzzle():
                        break
                    
                    user_input = input().strip()
                    result = self.process_move(user_input)
                    
                    if result == "quit":
                        break
                    elif result == "puzzle_complete":
                        input("\nPress Enter to return to main menu...")
                        break
                    elif result == "next_puzzle":
                        continue
                    elif result == "prev_puzzle":
                        continue
            
            elif choice == "2":
                self.list_puzzles()
            
            elif choice == "3":
                self.show_progress()
            
            elif choice == "4":
                print("\nThanks for using Chess Tutor! Goodbye!\n")
                break
            
            else:
                print("Invalid choice. Please try again.")


def main():
    """Main entry point for the chess tutor."""
    ui = ChessTutorUI()
    try:
        ui.run()
    finally:
        ui.analyzer.quit()


if __name__ == "__main__":
    main()
