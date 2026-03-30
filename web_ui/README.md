# Chess Tutor Web UI 🐴

A beautiful, interactive web-based interface for the Chess Tutor puzzle solver. Play chess puzzles directly in your browser with visual feedback, hints, and progress tracking.

## Features

✨ **Interactive 2D Board**
- Visual chessboard with proper colors
- Click-to-select pieces and squares
- Legal move highlighting
- Piece Unicode symbols (♔♕♖♗♘♙)

🎮 **Intuitive Controls**
- Enter moves in UCI notation (e.g., e2e4)
- Click pieces to see legal moves
- Click destination square to make move
- Keyboard support (Enter to submit)

💡 **Smart Hints**
- AI-powered move suggestions (requires Stockfish)
- Fallback to legal moves if engine unavailable
- Click hints to apply them instantly

📊 **Progress Tracking**
- Visual progress bar
- Solved puzzle counter
- Puzzle list with completion status
- Active puzzle highlighting

🎯 **Navigation**
- Previous/Next puzzle buttons
- Direct puzzle selection from list
- Puzzle difficulty indicators
- Easy/Medium/Hard categories

♻️ **Board Controls**
- Undo last move
- Reset board to puzzle start
- Move history display

## Installation

### Prerequisites
- Python 3.7+
- Flask (`pip install flask`)
- Existing Chess Tutor installation

### Setup

1. **Install Flask** (if not already installed):
```bash
pip install flask
```

2. **Optional: Install Stockfish** for enhanced hints:
```bash
# Windows via Chocolatey
choco install stockfish

# macOS via Homebrew
brew install stockfish

# Linux (Ubuntu/Debian)
sudo apt-get install stockfish
```

## Running the Web UI

### Start the Flask server:

```bash
cd web_ui
python app.py
```

Output:
```
🐴 Chess Tutor Web UI Starting...
📺 Open http://localhost:5000 in your browser
```

### Open in browser:
- **URL:** `http://localhost:5000`
- **Port:** 5000 (default)

## How to Use

### 1. **Playing a Puzzle**

**Method 1 - Type Moves:**
```
Example: e2e4
- Type the starting square (e2)
- Type the destination square (e4)
- Press Enter or click "Play Move"
```

**Method 2 - Click Moves:**
```
- Click on a piece to select it
- See legal moves highlighted as dots
- Click destination square to move
```

### 2. **Getting Hints**
- Click **"💡 Get Hints"** button
- Top 5 moves displayed with evaluations
- Click a hint to apply it instantly

### 3. **Navigation**
- Click **"Next →"** to advance to next puzzle
- Click **"← Previous"** to go back
- Click puzzle name in list to jump directly
- See checkmark (✓) next to solved puzzles

### 4. **Board Actions**
- **"↶ Undo Last"** - Revert your last move
- **"🔄 Reset Board"** - Start puzzle over
- **Info Panel** - Shows legal moves you can make

### 5. **Move History**
- Shows all your moves in order
- Helpful for reviewing your solution attempt

## File Structure

```
web_ui/
├── app.py                    # Flask backend (API routes)
├── templates/
│   └── index.html           # Main web UI (HTML)
├── static/
│   ├── style.css            # Styling (CSS)
│   └── board.js             # Interactive logic (JavaScript)
└── README.md                # This file
```

## API Endpoints

The Flask backend provides REST API endpoints:

### Puzzle Management
- `GET /api/puzzle/current` - Get current puzzle
- `POST /api/puzzle/next` - Move to next puzzle
- `POST /api/puzzle/previous` - Move to previous puzzle
- `POST /api/puzzle/select/<id>` - Jump to puzzle by ID
- `GET /api/puzzles/list` - Get all puzzles

### Move Handling
- `POST /api/move/validate` - Submit and validate move
- `GET /api/move/hints` - Get AI hints
- `POST /api/board/undo` - Undo last move
- `POST /api/board/reset` - Reset board

### Progress
- `GET /api/progress` - Get player progress stats

## Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full support |
| Firefox | ✅ Full support |
| Edge | ✅ Full support |
| Safari | ✅ Full support |
| Mobile | ✅ Responsive design |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit move |
| Escape | Clear selection |
| → | Next puzzle |
| ← | Previous puzzle |

## Integration with CLI

The Web UI runs **independently** alongside the CLI version:

```bash
# Terminal 1: Run CLI version
python main.py

# Terminal 2: Run Web UI
cd web_ui
python app.py
```

Both share the same:
- Puzzle database
- Progress tracking
- Move validation engine
- Analytics

## Troubleshooting

### "Connection Refused" Error
- Make sure Flask is running: `python app.py`
- Check port 5000 is not in use
- Try different port: `app.run(port=5001)`

### No Hints Available
- Stockfish engine not installed
- Web UI will show legal moves instead
- Install Stockfish for AI hints: see Installation

### Board Not Displaying
- Clear browser cache (Ctrl+Shift+Delete)
- Refresh page (F5)
- Check browser console for errors (F12)

### Moves Not Registering
- Ensure move format is correct: `e2e4` (not `e2 e4`)
- Check move is truly legal in position
- Verify legal moves list on right panel

## Customization

### Change Port
Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change 5000 to 8000
```

### Change Board Size
Edit `static/style.css`:
```css
.chessboard {
    max-width: 600px;  /* Default 500px */
}
```

### Enable Production Mode
Edit `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Performance

- Light-weight Flask server
- Client-side rendering for speed
- No database required
- Typical page load: < 1 second
- Move validation: < 100ms

## Future Enhancements

🔮 Potential improvements:
- Puzzle time limits
- Leaderboard / statistics
- Multiple games simultaneously
- Puzzle creator tool
- Analysis board view
- Export game history
- Multiplayer support

## Notes

- All puzzle data comes from existing `puzzle_solver.py`
- Move validation uses python-chess library
- Hints provided by optional Stockfish engine
- Progress syncs between CLI and Web UI
- No external dependencies beyond Flask

## Support

Having issues? Check:
1. [Chess Tutor Main README](../README.md)
2. [QUICKSTART.md](../QUICKSTART.md)
3. Flask documentation: https://flask.palletsprojects.com/

---

**Chess Tutor Web UI** | Made with ♔ for chess lovers | 2026
