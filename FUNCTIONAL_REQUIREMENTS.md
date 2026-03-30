# Chess Tutor - Functional Requirements Document

## Executive Summary

The **Chess Tutor** is an interactive, text-based chess puzzle solving application that teaches chess tactics through a series of puzzles. Users solve puzzles by inputting moves in UCI notation, receive immediate feedback on solution correctness, and track their progress through a collection of chess problems.

---

## 1. System Overview

### Primary Purpose
Enable chess players to practice tactical problem-solving through an interactive CLI (Command-Line Interface) puzzle solver.

### Core User Flow
```
1. User launches application
2. Selects "Start solving puzzles"
3. Sees a chess position (static board display)
4. Enters a move in UCI format
5. Gets feedback (correct/incorrect)
6. Progresses to next puzzle or retries
7. Tracks overall progress and statistics
```

### Target Users
- Chess players (beginner to intermediate)
- Puzzle enthusiasts
- Tactical trainers
- Students learning chess

---

## 2. Functional Requirements by Component

### 2.1 Main Menu System

**REQ-MENU-001: Display Main Menu**
- Show 4 menu options
- Options: Start puzzles, List puzzles, View progress, Quit
- Loop until user exits

**REQ-MENU-002: Handle Menu Selection**
- Accept numeric input (1-4)
- Route to appropriate function
- Handle invalid input gracefully
- Return to menu after actions

**REQ-MENU-003: Exit Handler**
- Clean shutdown on option 4
- Display goodbye message
- Close all resources (engine, etc.)

---

### 2.2 Puzzle Display & Board Rendering

**REQ-DISPLAY-001: Show Current Puzzle**
- Display puzzle number and difficulty
- Show puzzle name
- Show puzzle description
- Display whose turn it is (White/Black)

**REQ-DISPLAY-002: Render Chess Board**
- Convert FEN string to ASCII display
- Show all 64 squares with pieces
- Label ranks (1-8) and files (a-h)
- Use standard chess piece symbols (K, Q, R, B, N, P)
- Differentiate White (uppercase) and Black (lowercase)
- Format as static text-based image (not animated)

**REQ-DISPLAY-003: Board Borders & Formatting**
- Add visual borders around board
- Display coordinate labels
- Use ASCII art for clarity
- Make board easily readable

**REQ-DISPLAY-004: Progress Indicator**
- Show current puzzle number (e.g., "1/8")
- Display difficulty level
- Show solution status (solved/unsolved)

---

### 2.3 Move Input & Validation

**REQ-MOVE-001: Accept User Input**
- Prompt user for move or command
- Accept input from standard input (keyboard)
- Handle multiple input types:
  - UCI moves (e.g., "e2e4")
  - Promotion moves (e.g., "e7e8q")
  - Commands (h, b, n, p, q)

**REQ-MOVE-002: Parse UCI Notation**
- Accept 4-character format: source + destination
- Examples: "e2e4", "a1h8", "g1f3"
- Support 5-character format for promotions: "e7e8q"
- Extract source square, destination square, promotion piece
- Reject malformed input

**REQ-MOVE-003: Validate Move Legality**
- Check if move is legal in current position
- Use python-chess library for validation
- Reject illegal moves
- Provide error message for invalid moves

**REQ-MOVE-004: Handle Special Moves**
- Pawn promotions (e7e8q, e7e8r, e7e8b, e7e8n)
- Castling moves (e1g1, e1c1, e8g8, e8c8)
- Captures and en passant (handled by chess library)

---

### 2.4 Solution Validation

**REQ-SOLUTION-001: Check Against Best Moves**
- Get best moves from puzzle definition
- Compare user move to best moves
- Determine if move is correct solution

**REQ-SOLUTION-002: Provide Immediate Feedback**
- **Correct move**: Display success message, mark puzzle as solved
- **Incorrect move**: Show best move(s), allow retry or hint
- Show move in readable format
- No artificial delay

**REQ-SOLUTION-003: Handle Multiple Solutions**
- Support puzzles with multiple correct moves
- Accept any move from best_moves list
- Treat all best moves as equally valid

---

### 2.5 Puzzle Navigation

**REQ-NAV-001: Next Puzzle**
- Advance to next puzzle in sequence
- Auto-advance on correct solution
- Manual advance via 'n' command
- Detect end of puzzle set

**REQ-NAV-002: Previous Puzzle**
- Go back to previous puzzle
- Manual command via 'p'
- Prevent going before first puzzle

**REQ-NAV-003: Select Puzzle**
- From puzzle list, select by ID
- Jump directly to selected puzzle
- Update puzzle index

**REQ-NAV-004: Detect Completion**
- When all puzzles solved, show congratulations
- Return to main menu

---

### 2.6 Move Undo & Retry

**REQ-UNDO-001: Undo Last Move**
- Via 'b' (back) command
- Revert board to previous position
- Allow multiple undo operations
- Prevent undo before first move

**REQ-UNDO-002: Retry After Wrong Move**
- After incorrect move, keep puzzle active
- Allow user to undo and try again
- Keep failed attempt recorded

---

### 2.7 Hint System

**REQ-HINT-001: Show Move Hints**
- Via 'h' command during puzzle
- Show top 3 recommended moves
- Display move quality (evaluation score)
- Show solutions specific to puzzle

**REQ-HINT-002: Engine Integration (Optional)**
- Use Stockfish chess engine if available
- Analyze position
- Provide evaluation
- Suggest best continuation

**REQ-HINT-003: Graceful Degradation**
- Work without engine
- Inform user if engine unavailable
- Function with basic hints only

---

### 2.8 Puzzle Management

**REQ-PUZZLE-001: Load Puzzle Database**
- Load all puzzles at startup
- Store in memory
- Provide access by ID or index

**REQ-PUZZLE-002: Puzzle Data Structure**
```
Each puzzle contains:
- id (unique identifier)
- name (descriptive name)
- difficulty (Easy/Medium/Hard)
- fen (board position)
- best_moves (array of correct solutions)
- description (tactical theme explanation)
```

**REQ-PUZZLE-003: Initial Puzzle Set**
- Provide 8 pre-loaded puzzles
- Mix of difficulty levels
- Variety of tactical themes

---

### 2.9 Progress Tracking

**REQ-PROGRESS-001: Track Solved Puzzles**
- Record which puzzles user solved
- Persist during session
- Mark solved status visually

**REQ-PROGRESS-002: Record Attempts**
- Store each attempt (move + correct/incorrect)
- Track number of tries per puzzle
- Calculate success rate

**REQ-PROGRESS-003: Display Progress**
- Show puzzles solved / total puzzles
- Display progress percentage
- Show current puzzle number
- Accessible from menu

---

### 2.10 Command Interface

**REQ-CMD-001: Command Shortcuts**
During puzzle solving, support commands:

| Command | Function | Result |
|---------|----------|--------|
| `h` | Hints | Show best moves |
| `b` | Back/Undo | Revert last move |
| `n` | Next | Skip to next puzzle |
| `p` | Previous | Go to prev puzzle |
| `q` | Quit | Return to menu |

**REQ-CMD-002: Command Parsing**
- Detect commands (single character)
- Distinguish from moves (4-5 characters)
- Handle case-insensitively

**REQ-CMD-003: Command Execution**
- Execute immediately
- Provide feedback
- Allow new command/move input

---

### 2.11 Error Handling

**REQ-ERROR-001: Invalid Move Format**
- Reject moves not in UCI format
- Provide format hint
- Prompt for retry

**REQ-ERROR-002: Illegal Moves**
- Identify moves violating chess rules
- Show why move is illegal
- Allow new move input

**REQ-ERROR-003: Invalid Input**
- Handle non-integer menu selections
- Handle out-of-range selections
- Provide guidance

**REQ-ERROR-004: Missing Data**
- Handle missing puzzle data gracefully
- Skip malformed puzzles
- Log errors

---

## 3. Non-Functional Requirements

### 3.1 Performance
- **REQ-PERF-001**: Puzzle load time < 1 second
- **REQ-PERF-002**: Move validation < 100ms
- **REQ-PERF-003**: Board display render < 50ms
- **REQ-PERF-004**: Hint generation < 5 seconds (with engine)

### 3.2 Usability
- **REQ-USE-001**: No prerequisite knowledge needed
- **REQ-USE-002**: Clear prompts and instructions
- **REQ-USE-003**: Immediate feedback on all actions
- **REQ-USE-004**: Intuitive command interface

### 3.3 Compatibility
- **REQ-COMPAT-001**: Python 3.7+
- **REQ-COMPAT-002**: Works on Windows, Mac, Linux
- **REQ-COMPAT-003**: Standard terminal/console support
- **REQ-COMPAT-004**: Optional Stockfish (not required)

### 3.4 Data Integrity
- **REQ-DATA-001**: Accurate FEN parsing
- **REQ-DATA-002**: Correct move legality checking
- **REQ-DATA-003**: No data loss during session
- **REQ-DATA-004**: Consistent puzzle state

---

## 4. Module-Specific Requirements

### 4.1 board.py - Chess Board Logic

**Functions:**
- `__init__(fen)` - Initialize board
- `display()` - Show basic board format
- `display_fancy()` - Show formatted board
- `make_move(uci)` - Execute move, return bool
- `undo_move()` - Revert last move
- `get_legal_moves()` - List valid moves
- `is_game_over()` - Check endgame
- `to_fen()` - Export board state

**Requirements:**
- REQ-BOARD-001: Accurate FEN parsing
- REQ-BOARD-002: Correct move validation
- REQ-BOARD-003: Legal move generation
- REQ-BOARD-004: Move undo capability

### 4.2 puzzle_solver.py - Puzzle Management

**Functions:**
- `get_current_puzzle()` - Get active puzzle
- `get_puzzle_by_id(id)` - Fetch specific puzzle
- `is_solution_correct(move)` - Validate move
- `next_puzzle()` - Advance puzzle
- `previous_puzzle()` - Go back puzzle
- `mark_puzzle_solved(id)` - Track completion
- `get_progress()` - Return statistics
- `record_attempt(id, move, correct)` - Log attempt

**Requirements:**
- REQ-SOLVER-001: Puzzle state management
- REQ-SOLVER-002: Solution validation
- REQ-SOLVER-003: Progress tracking
- REQ-SOLVER-004: Attempt recording

### 4.3 move_analyzer.py - Engine Integration

**Functions:**
- `__init__(stockfish_path)` - Initialize engine
- `is_engine_available()` - Check engine status
- `get_best_moves(board, top_n)` - Get top moves
- `evaluate_position(board)` - Position eval
- `quit()` - Close engine

**Requirements:**
- REQ-ANALYZER-001: Optional engine support
- REQ-ANALYZER-002: Best move calculation
- REQ-ANALYZER-003: Position evaluation
- REQ-ANALYZER-004: Graceful fallback if unavailable

### 4.4 ui_enhanced.py - User Interface

**Functions:**
- `display_menu()` - Show main menu
- `show_puzzle()` - Display puzzle
- `display_puzzle_board()` - Render board
- `process_move(input)` - Handle move/command
- `get_hints()` - Show hints
- `list_puzzles()` - Browse puzzles
- `show_progress()` - Show statistics
- `run()` - Main game loop

**Requirements:**
- REQ-UI-001: Clear menu system
- REQ-UI-002: Input processing
- REQ-UI-003: Feedback display
- REQ-UI-004: Navigation handling

---

## 5. Data Flow

### Puzzle Solving Flow
```
1. User sees puzzle display
   │
2. User enters move or command
   │
3. Input parsed:
   ├─ If command → Execute command
   ├─ If move → Validate format
   │
4. Move validation:
   ├─ Check legality → If illegal, reject
   ├─ Execute move on board
   │
5. Solution check:
   ├─ Compare to best moves
   ├─ If correct → Mark solved, advance
   ├─ If wrong → Show best move, stay
   │
6. Attempt recording:
   ├─ Log move attempt
   ├─ Record correct/incorrect
   │
7. Display updated board & prompt
   │
8. Return to step 2
```

---

## 6. State Management

### Application States
```
MENU → PUZZLE_DISPLAY → INPUT_WAIT → MOVE_PROCESSING → FEEDBACK_DISPLAY → (PUZZLE_DISPLAY or MENU)
```

### Puzzle States
- **NOT_STARTED**: Puzzle available but not attempted
- **IN_PROGRESS**: Puzzle being solved
- **SOLVED**: Correct solution found
- **ATTEMPTED**: Wrong moves tried

### Board States
- **INITIAL**: Starting position for puzzle
- **AFTER_MOVE**: Position after user move
- **UNDONE**: Position after undo

---

## 7. Puzzle Definition

### Puzzle Structure
```python
{
    "id": 1,
    "name": "Puzzle Name",
    "difficulty": "Easy",  # Easy, Medium, Hard
    "fen": "rnbqkb1r/pppp1ppp/...",  # Board position
    "best_moves": ["d2d4"],  # Solution(s)
    "description": "Tactical theme description"
}
```

### Example Puzzle
```python
{
    "id": 1,
    "name": "Scholar's Mate Escape",
    "difficulty": "Easy",
    "fen": "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
    "best_moves": ["d2d4"],
    "description": "White controls the center. Find the move that strengthens the center."
}
```

---

## 8. User Interactions

### User Can:
1. ✅ View main menu
2. ✅ Start puzzle solving mode
3. ✅ View current puzzle board
4. ✅ Enter moves in UCI format
5. ✅ Get feedback on move quality
6. ✅ Undo incorrect moves
7. ✅ Skip to next puzzle
8. ✅ Go back to previous puzzle
9. ✅ Request hints
10. ✅ View all puzzles
11. ✅ Browse puzzle list
12. ✅ View progress statistics
13. ✅ Select specific puzzle
14. ✅ Exit to main menu
15. ✅ Quit application

### User Cannot:
- ❌ Modify puzzle definitions
- ❌ Save progress (current version)
- ❌ Share results
- ❌ See future puzzles
- ❌ Access detailed analytics

---

## 9. System Constraints

### Input Constraints
- Move must be 4-5 characters (UCI format)
- Menu selection must be 1-4
- Puzzle ID must exist
- Commands must be single character

### Output Constraints
- Board must be ASCII-only (no graphics)
- Text-based interface only
- No audio/video output
- Linear text flow

### Resource Constraints
- Memory: Minimal (all puzzles in RAM)
- CPU: Light (simple calculations)
- Storage: Not persistent (no save file)
- Network: None required

---

## 10. Success Criteria

A puzzle is considered **solved** when:
1. User enters a legal move
2. Move matches one of the best_moves
3. System marks puzzle as solved
4. Progress updates
5. System advances to next puzzle

A puzzle is considered **unsolved** when:
1. User enters an incorrect move (not in best_moves)
2. System provides feedback
3. User can retry or request hints

---

## 11. Extensibility Requirements

The system should support:
- **REQ-EXT-001**: Adding new puzzles (edit JSON)
- **REQ-EXT-002**: Changing board display format
- **REQ-EXT-003**: Adding new commands
- **REQ-EXT-004**: Custom puzzle collections
- **REQ-EXT-005**: Different difficulty groupings

---

## 12. Documentation Requirements

- User quick-start guide ✅
- Complete reference manual ✅
- Visual examples ✅
- API documentation ✅
- Demo script ✅

---

## Summary of Requirements

| Category | Count | Status |
|----------|-------|--------|
| Menu/Navigation | 3 | ✅ Complete |
| Display/Rendering | 4 | ✅ Complete |
| Move Input/Validation | 4 | ✅ Complete |
| Solution Validation | 3 | ✅ Complete |
| Puzzle Navigation | 4 | ✅ Complete |
| Undo/Retry | 2 | ✅ Complete |
| Hints | 3 | ✅ Complete |
| Puzzle Management | 3 | ✅ Complete |
| Progress Tracking | 3 | ✅ Complete |
| Commands | 3 | ✅ Complete |
| Error Handling | 4 | ✅ Complete |
| **TOTAL** | **41** | **✅ 100%** |

---

**Status: ALL REQUIREMENTS MET** ✅

**Version:** 1.0
**Last Updated:** March 29, 2026
