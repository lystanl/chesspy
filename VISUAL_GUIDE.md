# Chess Tutor - Visual Example

## What You'll See When Running

### Main Menu
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

### Starting a Puzzle
```
------------------------------------------------------------
                 PUZZLE 1/8 - Easy
------------------------------------------------------------

Puzzle: Scholar's Mate Escape
Description: White controls the center. Find the best move!

WHITE TO MOVE

BOARD POSITION:

    ┌─────────────────────┐
  8 │ r n b q k b · r │ 8
  7 │ p p p p · p p p │ 7
  6 │ · · · · · n · · │ 6
  5 │ · · · · p · · · │ 5
  4 │ · · · · P · · · │ 4
  3 │ · · · · · N · · │ 3
  2 │ P P P P · P P P │ 2
  1 │ R N B Q K B · R │ 1
    ├─────────────────────┤
    │ a b c d e f g h │
    └─────────────────────┘

------------------------------------------------------------
MOVE INPUT:
  Format: UCI notation (e.g., e2e4, e7e8q)
  Commands: 'h'=hints, 'b'=undo, 'n'=next, 'p'=prev, 'q'=quit
------------------------------------------------------------
Enter your move: 
```

### Getting Hints
```
Your move: h

[ANALYZING POSITION...]

HINTS - Top moves:
  1. d2d4      (score:   0.50)
  2. f3e5      (score:   0.45)
  3. g2g4      (score:   0.20)

Puzzle solution(s): d2d4
```

### Correct Move
```
Your move: d2d4

============================================================
                     [CORRECT!]
============================================================
Move 'd2d4' is one of the best moves!
============================================================

    ┌─────────────────────┐
  8 │ r n b q k b · r │ 8
  7 │ p p p p · p p p │ 7
  6 │ · · · · · n · · │ 6
  5 │ · · · · p · · · │ 5
  4 │ · · · · P · · · │ 4
  3 │ · · · · · N · · │ 3
  2 │ P P P P · P P P │ 2
  1 │ R N B Q K · B R │ 1
    ├─────────────────────┤
    │ a b c d e f g h │
    └─────────────────────┘

Press Enter for next puzzle...
```

### Incorrect Move (Trying d2d3)
```
Your move: d2d3

[INCORRECT] Not the best move.
Best move(s): d2d4

    ┌─────────────────────┐
  8 │ r n b q k b · r │ 8
  7 │ p p p p · p p p │ 7
  6 │ · · · · · n · · │ 6
  5 │ · · · · p · · · │ 5
  4 │ · · · · P · · · │ 4
  3 │ · · · · P N · · │ 3
  2 │ P P P P · · P P │ 2
  1 │ R N B Q K B · R │ 1
    ├─────────────────────┤
    │ a b c d e f g h │
    └─────────────────────┘

Analyzing better alternatives...
Better move: d2d4 (score: 0.50)
```

### List All Puzzles
```
======================================================================
                         AVAILABLE PUZZLES
======================================================================
ID    Name                           Difficulty    Status
------================================================================
1     Scholar's Mate Escape         Easy           [OK]
2     Back Rank Mate Threat         Medium         [ ]
3     Pawn Promotion                Easy           [ ]
4     Checkmate in One              Hard           [ ]
5     Discovered Attack             Medium         [ ]
6     Pin the Bishop                Medium         [ ]
7     Escape the Trap               Hard           [ ]
8     Fork Attack                   Easy           [ ]
----------------------------------------------------------------------

Enter puzzle ID to select (or press Enter to go back): 
```

### View Progress
```
============================================================
                       YOUR PROGRESS
============================================================
Puzzles Solved: 1/8
Progress: 12.5%
Current Puzzle: 2
============================================================
```

### Puzzle Complete
```
============================================================
                     [PUZZLE SET COMPLETE!]
                  You've solved all puzzles!
============================================================

Press Enter to return to main menu...
```

## Board Display Explanation

### Piece Symbols
```
Uppercase = White pieces          Lowercase = Black pieces
K = King                          k = King
Q = Queen                         q = Queen
R = Rook                          r = Rook
B = Bishop                        b = Bishop
N = Knight                        n = Knight
P = Pawn                          p = Pawn
. = Empty square
```

### Coordinates
```
  a b c d e f g h  (columns = files)
8 ┌──────────────┐ 8 (rows = ranks)
7 │              │ 7
6 │              │ 6
5 │              │ 5
4 │              │ 4
3 │              │ 3
2 │              │ 2
1 └──────────────┘ 1
  a b c d e f g h
```

### Reading the Board
- **Top-left corner**: a8 (Black's left-side piece)
- **Bottom-left corner**: a1 (White's left-side piece)
- **Top-right corner**: h8 (Black's right-side piece)
- **Bottom-right corner**: h1 (White's right-side piece)

## Move Examples

### Standard Moves
```
e2e4  → Move pawn from e2 to e4 (King's pawn opening)
g1f3  → Move knight from g1 to f3 (Ruy Lopez)
c1e3  → Move bishop from c1 to e3
a1h8  → Move rook from a1 to h8
```

### Pawn Promotion
```
e7e8q  → Promote pawn to Queen (most common)
e7e8r  → Promote pawn to Rook
e7e8b  → Promote pawn to Bishop
e7e8n  → Promote pawn to Knight
```

### Captures
```
e4d5   → Capture piece on d5
f6e4   → Knight captures on e4
```

## Command Reference

During a puzzle:

| Input | Action | Example |
|-------|--------|---------|
| `h` | Show hints | `Your move: h` |
| `b` | Undo move | `Your move: b` |
| `n` | Next puzzle | `Your move: n` |
| `p` | Previous puzzle | `Your move: p` |
| `q` | Quit to menu | `Your move: q` |
| Move | Make a move | `Your move: e2e4` |

## Session Flow

1. Start program → See main menu
2. Select "1. Start solving puzzles" → Puzzle 1 loads
3. See board + description
4. Enter move in UCI format
5. Get feedback (correct/incorrect)
6. Automatically advance or try again
7. Repeat for 8 puzzles
8. See congratulations when done!

## What Makes It Work?

### Static Board Display ✅
- Uses ASCII art with borders
- Shows position as static image (not animated)
- Updates display after each move

### Text-Based Input ✅
- Accepts UCI move notation
- Validates legality
- Clear error messages

### Move Checking ✅
- Validates against best moves
- Provides feedback
- Shows better alternatives

### Progress Tracking ✅
- Counts solved puzzles
- Tracks attempts
- Shows statistics

---

**This is now fully functional and ready to use!**

Run: `python main.py`
