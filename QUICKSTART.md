# Chess Tutor - Quick Start Guide

## Installation (One-time setup)

```bash
# 1. Navigate to project
cd c:\Users\User\OneDrive\Documents\comp sci course\vsc\chess-tutor

# 2. Install python-chess library
python -m pip install python-chess

# Done! You're ready to go.
```

## Running the Puzzle Solver

```bash
# Start the interactive puzzle solver
python main.py
```

You'll see the main menu:
```
============================================================
                WELCOME TO CHESS TUTOR!
============================================================

============================================================
        CHESS TUTOR - PUZZLE SOLVER
============================================================

1. Start solving puzzles
2. List all puzzles
3. View progress
4. Quit

Enter your choice (1-4): 
```

## How to Solve a Puzzle

1. **Press 1** to start solving puzzles

2. **See the puzzle** with board display:
   ```
   WHITE TO MOVE

   BOARD POSITION:
       ┌─────────────────────┐
     8 │ r n b q k b · r │ 8
     7 │ p p p p · p p p │ 7
     ...
   ```

3. **Enter your move** in UCI format (e.g., `e2e4`):
   ```
   Enter your move: d2d4
   ```

4. **Get feedback**:
   - ✅ **CORRECT!** → Move to next puzzle
   - ❌ **INCORRECT** → See the best move, try again

5. **Use commands during puzzle**:
   - `h` → Get hints from chess engine
   - `b` → Undo your move
   - `n` → Skip to next puzzle
   - `p` → Go to previous puzzle
   - `q` → Quit to main menu

## Move Format (UCI Notation)

Moves are entered as: **SOURCE SQUARE → DESTINATION SQUARE**

### Examples:
- `e2e4` → Move from e2 to e4
- `e7e8q` → Promote pawn to queen on e8
- `a1h8` → Move piece from a1 to h8

### Board Coordinates:
```
  a b c d e f g h  (files: left to right)
8 ┌──────────────┐ 8
7 │              │ 7
6 │      BOARD   │ 6  (ranks: top = 8, bottom = 1)
5 │              │ 5
4 │              │ 4
3 │              │ 3
2 │              │ 2
1 └──────────────┘ 1
  a b c d e f g h
```

## Example Session

```
$ python main.py

Press 1 to start:
> 1

You see Puzzle 1: "Scholar's Mate Escape"
WHITE TO MOVE

Your move: d2d4

[CORRECT!]
===============================================
Move 'd2d4' is one of the best moves!
===============================================

Press Enter for next puzzle...
> 

Puzzle 2 loading...
```

## Running the Demo

To see everything in action without playing:

```bash
python demo.py
```

This shows:
- All 8 puzzles
- Board display examples  
- How moves are validated
- Progress tracking demo

## Common Moves

### Pawn Moves
- `e2e4` - Move e-pawn forward 2 squares
- `e2e3` - Move e-pawn forward 1 square
- `a2a4` - Move a-pawn forward 2 squares

### Piece Moves
- `g1f3` - Move knight from g1 to f3
- `b1c3` - Move knight from b1 to c3
- `c1e3` - Move bishop from c1 to e3

### Promotion
- `e7e8q` - Promote to Queen
- `e7e8r` - Promote to Rook
- `e7e8b` - Promote to Bishop
- `e7e8n` - Promote to Knight

## Getting Hints

If you're stuck, press `h` during a puzzle:

```
Your move: h

[ANALYZING POSITION...]

HINTS - Top moves:
  1. d2d4      (score:   0.50)
  2. f3e5      (score:   0.45)
  3. g2g4      (score:   0.20)

Puzzle solution(s): d2d4
```

This shows the top 3 moves analyzed by Stockfish chess engine.

## Solving All Puzzles

Current puzzles by difficulty:

**Easy (3):**
- #1: Scholar's Mate Escape
- #3: Pawn Promotion
- #8: Fork Attack

**Medium (3):**
- #2: Back Rank Mate Threat
- #5: Discovered Attack
- #6: Pin the Bishop

**Hard (2):**
- #4: Checkmate in One
- #7: Escape the Trap

## Tips for Success

1. **Start with Easy** - Build confidence and learn patterns
2. **Use hints as learning** - See what the engine suggests
3. **Undo and retry** - Press `b` to try different moves
4. **Check progress** - See how many you've solved (menu option 3)
5. **Repeat hard puzzles** - Master them for better tactics

## Troubleshooting

### Illegal Move Error
Make sure your move notation is correct:
- ✅ `e2e4` (lowercase)
- ✅ `e7e8q` (4 chars + promotion)
- ❌ `e4` (too short)
- ❌ `E2E4` (uppercase)

### Invalid Format
Move must be exactly 4-5 characters (UCI format):
- `e2e4` ✅
- `Nf3` ❌ (use `g1f3` instead)

### Engine Not Available
If stockfish hints don't work:
- Hints are optional - puzzles work fine without them
- To enable: download Stockfish from stockfishchess.org
- For Mac: `brew install stockfish`
- For Linux: `sudo apt-get install stockfish`

## File Locations

- **Puzzles**: `/puzzles/sample_puzzles.py`
- **Board Logic**: `/board.py`
- **Game Logic**: `/puzzle_solver.py`
- **Engine**: `/move_analyzer.py`
- **UI**: `/ui_enhanced.py`

## Next Steps

- Try solving all 8 puzzles!
- Check out PUZZLE_GUIDE.md for detailed information
- Look at demo.py to understand how it all works
- Consider adding your own puzzles

---

**Ready to solve?** Run: `python main.py`
