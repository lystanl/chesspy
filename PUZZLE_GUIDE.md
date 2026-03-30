# Chess Tutor - Puzzle System Documentation

## Overview

The **Chess Tutor** is an interactive command-line chess puzzle solver that teaches players through tactical puzzles. It features:

- ✅ **8 Pre-loaded Puzzles** (Easy, Medium, Hard)
- ✅ **Text-based Board Display** (ASCII visualization)
- ✅ **Move Validation** using python-chess
- ✅ **Progress Tracking** (solved puzzles, statistics)
- ✅ **Interactive Puzzle Solving** (guess the best move)
- ✅ **Hints System** (optional Stockfish engine)
- ✅ **Move Navigation** (next, previous puzzles)

## Installation

### Prerequisites
- Python 3.7+
- python-chess 1.10.0+
- Optional: Stockfish engine (for move hints)

### Setup

```bash
# Navigate to project directory
cd chess-tutor

# Install dependencies
python -m pip install -r requirements.txt

# (Optional) Download Stockfish for move analysis
# Linux: sudo apt-get install stockfish
# Mac: brew install stockfish
# Windows: Download from https://stockfishchess.org/download/
```

## Quick Start

### Run the Interactive Puzzle Solver
```bash
python main.py
```

### Run the Demo
```bash
python demo.py
```

This shows:
- All available puzzles
- Board display examples
- Puzzle solving mechanics
- Progress tracking

## Features

### 1. Interactive Puzzle Mode

When you select "Start solving puzzles", you'll see:
- A formatted chessboard position
- Puzzle name and description
- Hints about whose turn it is (White/Black)
- A prompt to enter your move

```
PUZZLE 1/8 - Easy
---------

Puzzle: Scholar's Mate Escape
Description: White controls the center. Find the best move!

WHITE TO MOVE

BOARD POSITION:
    ┌─────────────────────┐
  8 │ r n b q k b · r │ 8
  7 │ p p p p · p p p │ 7
  ...
```

### 2. Move Input (UCI Format)

Moves are entered using **UCI (Universal Chess Interface) notation**:
- Standard move: `e2e4`
- Pawn promotion: `e7e8q` (promotes to queen)
- Capture: `e4d5`

Examples:
```
e2e4      # Move pawn from e2 to e4
e7e8q     # Promote pawn on e7 to queen on e8
a1h8      # Move piece from a1 to h8
```

### 3. Puzzle Commands

During puzzle solving, use these shortcuts:

| Command | Action |
|---------|--------|
| `h` | Show hints (top 3 moves) |
| `b` | Undo last move |
| `n` | Skip to next puzzle |
| `p` | Go to previous puzzle |
| `q` | Quit to main menu |

Example:
```
Your move: h
[ANALYZING POSITION...]

HINTS - Top moves:
  1. d2d4    (score:   0.50)
  2. f3e5    (score:   0.45)
  3. g2g4    (score:   0.20)

Puzzle solution(s): d2d4
```

### 4. Progress Tracking

Track your progress with:
- **Puzzles Solved**: Shows how many you've completed
- **Progress Percentage**: Visual progress indicator
- **Current Puzzle**: Current puzzle number in sequence

View progress anytime from the main menu → Option 3.

### 5. Puzzle Database

Browse all available puzzles:
- **List View**: Main menu → Option 2
- **Organized by Difficulty**: Easy (3), Medium (3), Hard (2)
- **Status Indicator**: [OK] = solved, [ ] = not solved

## Puzzle Structure

Each puzzle contains:

```python
{
    "id": 1,
    "name": "Scholar's Mate Escape",
    "difficulty": "Easy",  # Easy, Medium, Hard
    "fen": "rnbqkb1r/...",  # Board position (FEN notation)
    "best_moves": ["d2d4"],  # Expected solution move(s)
    "description": "White controls the center. Find the move that strengthens the center."
}
```

### Current Puzzles

1. **Scholar's Mate Escape** (Easy) - Center control tactics
2. **Back Rank Mate Threat** (Medium) - King safety
3. **Pawn Promotion** (Easy) - Endgame promotion
4. **Checkmate in One** (Hard) - Mate in one move
5. **Discovered Attack** (Medium) - Discovered tactics
6. **Pin the Bishop** (Medium) - Knight positioning
7. **Escape the Trap** (Hard) - Tactical defense
8. **Fork Attack** (Easy) - Knight forks

## How to Play

### Example Game Session

```
1. Start the application:
   $ python main.py

2. Select "1. Start solving puzzles"

3. You see Puzzle 1 with board display

4. Enter your move (e.g., "d2d4")

5. System tells you:
   [CORRECT!] - Move is one of the best moves → Next puzzle
   [INCORRECT] - Shows the best move → Try again or press 'h' for hints

6. Repeat until all puzzles are solved!
```

## Board Display Format

The board uses ASCII art with:
- Rank numbers (1-8) on the left
- File letters (a-h) on the bottom
- Piece symbols:
  - Uppercase = White pieces (K, Q, R, B, N, P)
  - Lowercase = Black pieces (k, q, r, b, n, p)
  - `.` = Empty square

### Legend

```
K/k = King        B/b = Bishop
Q/q = Queen       N/n = Knight
R/r = Rook        P/p = Pawn
```

## Project Structure

```
chess-tutor/
├── main.py                 # Entry point
├── ui_enhanced.py         # Interactive UI
├── board.py               # Board management
├── puzzle_solver.py       # Puzzle logic
├── move_analyzer.py       # Stockfish integration
├── demo.py                # Demo script
├── requirements.txt       # Dependencies
├── puzzles/
│   ├── __init__.py
│   └── sample_puzzles.py  # Puzzle database
└── __pycache__/

```

## API Reference

### ChessBoard Class

```python
from board import ChessBoard

# Initialize board
board = ChessBoard()                    # Standard position
board = ChessBoard(fen_string)         # From FEN

# Methods
board.display()                        # Text display
board.display_fancy()                  # Fancy border display
board.make_move("e2e4")              # Make move (returns bool)
board.undo_move()                      # Undo last move (returns bool)
board.get_legal_moves()               # List all legal moves
board.is_game_over()                  # Check if game ended
board.to_fen()                        # Get FEN string
```

### PuzzleSolver Class

```python
from puzzle_solver import PuzzleSolver

solver = PuzzleSolver()

# Methods
solver.get_current_puzzle()            # Get current puzzle dict
solver.get_puzzle_by_id(puzzle_id)    # Get specific puzzle
solver.get_all_puzzles()              # Get all puzzles list
solver.is_solution_correct(move_uci)  # Check if move is best
solver.mark_puzzle_solved(puzzle_id)  # Mark as solved
solver.is_puzzle_solved(puzzle_id)    # Check if solved
solver.get_progress()                 # Get progress dict
solver.next_puzzle()                  # Advance puzzle (returns bool)
solver.previous_puzzle()              # Go back puzzle (returns bool)
solver.select_puzzle(puzzle_id)       # Jump to specific puzzle
```

### MoveAnalyzer Class

```python
from move_analyzer import MoveAnalyzer

analyzer = MoveAnalyzer()

# Methods
analyzer.is_engine_available()          # Check if Stockfish loaded
analyzer.get_best_moves(board, top_n=3) # Get top moves for position
analyzer.evaluate_position(board)       # Get position evaluation
analyzer.quit()                         # Close engine gracefully
```

## Extending the System

### Adding New Puzzles

Edit `puzzles/sample_puzzles.py`:

```python
PUZZLES = [
    # ... existing puzzles ...
    {
        "id": 9,
        "name": "Your Puzzle Name",
        "difficulty": "Medium",  # Easy, Medium, Hard
        "fen": "r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2",
        "best_moves": ["move1", "move2"],  # In UCI format
        "description": "Puzzle description here"
    },
]
```

### Getting FEN from Chess.com/Lichess

1. Open the position on Chess.com or Lichess
2. Click "Share" → "Export/Copy FEN"
3. Paste into the puzzle's "fen" field

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'chess'"
**Solution**: Install dependencies
```bash
python -m pip install python-chess
```

### Issue: Stockfish hints not working
**Solution**: Install Stockfish separately
- Download: https://stockfishchess.org/download/
- On Mac: `brew install stockfish`
- On Linux: `sudo apt-get install stockfish`
- Windows: Run the installer, note installation path

### Issue: Invalid move error
**Solution**: Use correct UCI notation
- ✅ Correct: `e2e4` (lowercase, 4-character)
- ❌ Wrong: `ne2e4`, `e4`, `E2E4`

## Performance Tips

1. Use `h` for hints to learn from engine analysis
2. Work through Easy puzzles first to learn patterns
3. Use `b` to undo and try different moves
4. Check `p` (progress) to see your improvement
5. Repeating Hard puzzles helps master tactics

## Future Enhancements

- [ ] Progress persistence (save/load)
- [ ] Puzzle categories (tactics, strategy, endgames)
- [ ] Time-based solving challenges
- [ ] Puzzle statistics (average time, attempts)
- [ ] Custom puzzle import
- [ ] Online puzzle collection integration
- [ ] GUI version (tkinter/pygame)

## License

Open source - feel free to modify and extend!

## Contributing

To add puzzles or improvements:
1. Test thoroughly with the demo script
2. Verify FEN positions with Chess.com
3. Ensure moves are in correct UCI format
4. Document any new features

---

**Happy puzzle solving!** 🎯♟️
