"""
User interface module.
Handles all CLI interactions with the user.
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
            print("\n⚠️  WARNING: Stockfish engine not found!")
            print("   Move analysis will be limited.")
            print("   Download Stockfish from: https://stockfishchess.org/download/")
            path = "stockfish/stockfish-windows-x86-64-avx2"
            if path:
                if self.analyzer.set_engine_path(path):
                    print("✓ Stockfish loaded successfully!\n")
                else:
                    print("✗ Failed to load Stockfish from that path.\n")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("        CHESS TUTOR - PUZZLE SOLVER")
        print("="*50)
        print("\n1. Start solving puzzles")
        print("2. List all puzzles")
        print("3. View progress")
        print("4. Quit")
        print("\nEnter your choice (1-4): ", end="")
    
    def display_puzzle_menu(self):
        """Display the puzzle-solving menu."""
        print("\n" + "-"*50)
        puzzle = self.puzzle_solver.get_current_puzzle()
        if not puzzle:
            print("No puzzles available!")
            return
        
        progress = self.puzzle_solver.get_progress()
        print(f"Puzzle {progress['current_puzzle_index']}/{progress['total_puzzles']}")
        print(f"Difficulty: {puzzle.get('difficulty', 'Unknown')}")
        print(f"Name: {puzzle.get('name', 'Unnamed')}")
        print("-"*50)
    
    def show_puzzle(self):
        """Display the current puzzle and board."""
        puzzle = self.puzzle_solver.get_current_puzzle()
        if not puzzle:
            print("No puzzle selected!")
            return False
        
        # Reset board to puzzle position
        self.board = ChessBoard(puzzle["fen"])
        
        self.display_puzzle_menu()
        self.display_puzzle_board()
        
        return True
    
    def display_puzzle_board(self):
        """Display puzzle board with description and prompt."""
        puzzle = self.puzzle_solver.get_current_puzzle()
        if not puzzle:
            return
        
        print("\n" + "="*50)
        print(f"Puzzle: {puzzle.get('name', 'Unnamed')}")
        print("="*50)
        print(f"\n📋 Description: {puzzle.get('description', 'No description')}")
        print(f"🎯 Find the best move!\n")
        
        # Display board
        print("Current position:")
        self.board.display_fancy()
        
        # Display whose turn it is
        if self.board.board.turn:
            print("♔ White to move\n")
        else:
            print("♚ Black to move\n")
        
        print("-"*50)
        print("Enter your move (UCI format, e.g., e2e4)")
        print("Commands: 'h' = hints, 'b' = undo, 'n' = next, 'p' = prev, 'q' = quit")
        print("-"*50)
        print("Your move: ", end="")
    
    def list_puzzles(self):
        """Display all available puzzles."""
        puzzles = self.puzzle_solver.get_all_puzzles()
        
        print("\n" + "="*70)
        print("AVAILABLE PUZZLES")
        print("="*70)
        print(f"{'ID':<5} {'Name':<30} {'Difficulty':<15} {'Solved':<5}")
        print("-"*70)
        
        for puzzle in puzzles:
            puzzle_id = puzzle.get("id", "?")
            name = puzzle.get("name", "Unnamed")[:28]
            difficulty = puzzle.get("difficulty", "Unknown")
            solved = "✓" if self.puzzle_solver.is_puzzle_solved(puzzle_id) else " "
            print(f"{puzzle_id:<5} {name:<30} {difficulty:<15} {solved:<5}")
        
        print("-"*70)
        print(f"\nEnter puzzle ID to select (or press Enter to go back): ", end="")
        choice = input().strip()
        
        if choice:
            if self.puzzle_solver.select_puzzle(int(choice)):
                print(f"✓ Selected puzzle {choice}")
            else:
                print(f"✗ Puzzle {choice} not found!")
    
    def get_hints(self):
        """Show hints for the current puzzle."""
        if not self.analyzer.is_engine_available():
            print("\n⚠️  Engine not available - cannot show hints")
            return
        
        if not self.board:
            return
        
        puzzle = self.puzzle_solver.get_current_puzzle()
        print("\nAnalyzing position...")
        
        best_moves = self.analyzer.get_best_moves(self.board.board, top_n=3)
        
        if not best_moves:
            print("Could not analyze position")
            return
        
        print("\nTop moves:")
        for i, move_info in enumerate(best_moves, 1):
            print(f"{i}. {move_info['san']} (eval: {move_info['score']:.2f})")
        
        print(f"\nBest move(s) for this puzzle: {', '.join(puzzle.get('best_moves', []))}")
    
    def process_move(self, move_input):
        """
        Process a player's move input.
        
        Args:
            move_input (str): The move in UCI format or command
        """
        if move_input.lower() == 'h':
            self.get_hints()
            return
        elif move_input.lower() == 'b':
            if self.board.undo_move():
                print("✓ Move undone")
            else:
                print("✗ No moves to undo")
            return
        elif move_input.lower() == 'n':
            if self.puzzle_solver.next_puzzle():
                print("✓ Moving to next puzzle")
            else:
                print("✗ Already on last puzzle")
            return
        elif move_input.lower() == 'p':
            if self.puzzle_solver.previous_puzzle():
                print("✓ Moving to previous puzzle")
            else:
                print("✗ Already on first puzzle")
            return
        elif move_input.lower() == 'q':
            return "quit"
        
        # Try to make the move
        if not move_input or len(move_input) < 4:
            print("✗ Invalid move format. Use UCI (e.g., e2e4)")
            return
        
        if self.board.make_move(move_input):
            puzzle = self.puzzle_solver.get_current_puzzle()
            
            # Check if it's the correct move
            if self.puzzle_solver.is_solution_correct(move_input):
                print(f"✓ Correct move! {move_input} is one of the best moves!")
                self.puzzle_solver.mark_puzzle_solved(puzzle["id"])
                self.puzzle_solver.record_attempt(puzzle["id"], move_input, True)
                self.board.display()
                
                if not self.puzzle_solver.next_puzzle():
                    print("\n� Congratulations! You've completed all puzzles!")
                    return "puzzle_complete"
            else:
                best_moves = puzzle.get("best_moves", [])
                print(f"✗ Not the best move. Best move(s): {', '.join(best_moves)}")
                self.puzzle_solver.record_attempt(puzzle["id"], move_input, False)
                self.board.display()
                
                # Give hint about best move
                if self.analyzer.is_engine_available():
                    print("\nAnalyzing better alternatives...")
                    best_moves_list = self.analyzer.get_best_moves(self.board.board, top_n=1)
                    if best_moves_list:
                        best = best_moves_list[0]
                        print(f"Better move: {best['san']} (eval: {best['score']:.2f})")
        else:
            print("✗ Illegal move or invalid format")
    
    def show_progress(self):
        """Display player's progress."""
        progress = self.puzzle_solver.get_progress()
        
        print("\n" + "="*50)
        print("YOUR PROGRESS")
        print("="*50)
        print(f"Puzzles solved: {progress['solved_puzzles']}/{progress['total_puzzles']}")
        print(f"Progress: {progress['progress_percentage']:.1f}%")
        print(f"Current puzzle: {progress['current_puzzle_index']}")
        print("="*50)
    
    def show_help(self):
        """Display help information."""
        print("\n" + "="*50)
        print("HELP - COMMANDS")
        print("="*50)
        print("Move format: UCI notation (e.g., e2e4, e7e8q)")
        print("\nCommands during puzzle:")
        print("  h - Show hints (top moves)")
        print("  b - Undo last move")
        print("  n - Next puzzle")
        print("  p - Previous puzzle")
        print("  q - Quit to main menu")
        print("="*50)
    
    def run(self):
        """Run the main game loop."""
        print("\n" + "="*50)
        print("  Welcome to Chess Tutor!")
        print("="*50)
        
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
            
            elif choice == "2":
                self.list_puzzles()
            
            elif choice == "3":
                self.show_progress()
            
            elif choice == "4":
                print("\nThanks for using Chess Tutor! Goodbye!")
                break
            
            else:
                print("✗ Invalid choice. Please try again.")


def main():
    """Main entry point for the chess tutor."""
    ui = ChessTutorUI()
    try:
        ui.run()
    finally:
        ui.analyzer.quit()


if __name__ == "__main__":
    main()
