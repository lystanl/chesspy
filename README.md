# Chess Tutor Game

A command-line chess tutor application that helps players solve chess puzzles and learn best moves analysis. Built with Python and integrated with Stockfish for intelligent move analysis.

## Features

- 🎯 **Puzzle Solver**: Load and solve chess puzzles with progressive difficulty
- 📊 **Move Analysis**: Get immediate feedback on your moves and see the best alternatives
- ♟️ **Interactive Board**: Visual representation of chess positions in the terminal
- 💡 **AI-Powered Analysis**: Stockfish engine integration for best-move suggestions
- 📈 **Progress Tracking**: Track your puzzle-solving progress and statistics

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Stockfish chess engine (download below)

### Installation (5 minutes)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/favourjimi/chess-tutor.git
   cd chess-tutor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download & Setup Stockfish:**
   - **Windows**: Download from [stockfishchess.org](https://stockfishchess.org/download/)
   - **Mac**: `brew install stockfish`
   - **Linux**: `sudo apt-get install stockfish`
   - Note the path to the `stockfish` executable

4. **Run the application:**
   ```bash
   python main.py
   ```

   On first run, you'll be prompted to provide the path to your Stockfish executable. The path is saved for future runs.

## Project Structure

```
chess-tutor/
├── main.py                      # Entry point and game loop
├── board.py                     # Chess board display and management
├── puzzle_solver.py             # Puzzle loading and validation logic
├── move_analyzer.py             # Stockfish integration and move analysis
├── ui.py                        # CLI user interface (basic version)
├── ui_enhanced.py               # Enhanced UI with better formatting
├── demo.py                      # Demo/testing script
├── test.py                      # Test suite
├── requirements.txt             # Python dependencies
├── puzzles/
│   ├── __init__.py
│   └── sample_puzzles.py        # Puzzle data and definitions
├── web_ui/                      # (Optional) Web-based UI
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   ├── board.js
│   │   └── style.css
│   └── templates/
│       └── index.html
└── Documentation/
    ├── ARCHITECTURE.md          # System design and architecture
    ├── FUNCTIONAL_REQUIREMENTS.md
    ├── IMPLEMENTATION.md        # Implementation details
    └── QUICKSTART.md            # Quick reference guide
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Entry point - starts the game loop and handles user menu |
| `board.py` | Displays chess board and manages board state |
| `move_analyzer.py` | Communicates with Stockfish for move analysis |
| `puzzle_solver.py` | Loads puzzles and validates user moves |
| `ui.py` / `ui_enhanced.py` | User interface layer for game interaction |
| `puzzles/sample_puzzles.py` | Contains puzzle definitions in FEN notation |

## How to Play

1. Start the game: `python main.py`
2. Select "Start solving puzzles" from the menu
3. A chess position appears on the board
4. Enter your move in **UCI notation** (e.g., `e2e4`)
5. Get instant feedback on correctness
6. See the best move analysis from Stockfish
7. Progress to the next puzzle

### Move Format

Chess moves use **UCI (Universal Chess Interface) notation**:
- **Format**: `<from_square><to_square>[promotion]`
- **Examples**:
  - `e2e4` - move pawn from e2 to e4
  - `e7e8q` - move pawn from e7 to e8 and promote to queen
  - `g1f3` - move knight from g1 to f3

**Squares** are referenced as: `a1, a2, ..., h8` (coordinates on the board)

## Development & Contributing

### For Teammates Working on This Project

#### Setting Up Your Development Environment

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests:**
   ```bash
   python test.py
   ```

#### Adding New Puzzles

Edit `puzzles/sample_puzzles.py` and add to the `PUZZLES` list:

```python
{
    "id": 5,
    "name": "Back Rank Checkmate Trap",
    "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
    "best_moves": ["e4e5"],
    "difficulty": "Medium",
    "description": "Find the strongest move"
}
```

**FEN Format**: `position pieces - active color - castling rights - en passant - halfmove clock - fullmove number`

#### Code Organization

- **board.py**: All board display and management logic
- **move_analyzer.py**: All Stockfish engine communication
- **puzzle_solver.py**: Puzzle loading and move validation
- **ui.py**: CLI interface (keep UI separate from logic)

Each module is designed to be independent for easy testing and modification.

#### Making Changes

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly: `python test.py`
4. Commit with clear messages: `git commit -m "Add feature: description"`
5. Push to GitHub: `git push origin feature/your-feature-name`
6. Create a Pull Request for review

#### Common Customizations

**Change Stockfish engine difficulty:**
```python
# In move_analyzer.py
self.engine.set_skill_level(15)  # Range: 0-20, higher = stronger
```

**Modify puzzle loading logic:**
```python
# In puzzle_solver.py - edit the load_puzzles() function
```

**Update UI formatting:**
```python
# In ui.py or ui_enhanced.py - modify display functions
```

### Dependencies

- **python-chess** (v1.9+): Chess logic, move validation, and FEN parsing
- **stockfish**: Chess engine for analysis (requires binary installation)

View full dependency list in `requirements.txt`

## Documentation

For more detailed information, see:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, data flow, and module interactions
- **[FUNCTIONAL_REQUIREMENTS.md](FUNCTIONAL_REQUIREMENTS.md)** - Detailed feature specifications
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Implementation details and design decisions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide for running the project
- **[REQUIREMENTS_MAPPING.md](REQUIREMENTS_MAPPING.md)** - How requirements map to code
- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - UI and visual system guide

## Troubleshooting

### Stockfish Not Found
- **Windows**: Verify the path to `stockfish.exe` is correct
- **Mac/Linux**: Ensure Stockfish is installed: `which stockfish`
- Solution: Re-run `main.py` and provide the correct path when prompted

### Import Errors
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Or update if needed
pip install --upgrade python-chess
```

### Board Display Issues
- Try running with `ui_enhanced.py` for better formatting
- Ensure terminal supports UTF-8 characters

## Project Goals

This project demonstrates:
- ✅ Object-oriented Python design
- ✅ Integration with external tools (Stockfish)
- ✅ Interactive CLI applications
- ✅ Game logic and move validation
- ✅ Modular, testable code architecture

## License

Class project - Feel free to modify and extend!

## Questions or Issues?

- Check the [QUICKSTART.md](QUICKSTART.md) for common questions
- Review the documentation files listed above
- Check existing puzzles in `puzzles/sample_puzzles.py` for format examples
