"""
Sample chess puzzles for the tutor.
Each puzzle includes a FEN position and the best move(s).
"""

PUZZLES = [
    {
        "id": 1,
        "name": "Scholar's Mate Escape",
        "difficulty": "Easy",
        "fen": "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
        "best_moves": ["d2d4"],
        "description": "White controls the center. Find the move that strengthens the center."
    },
    {
        "id": 2,
        "name": "Back Rank Mate Threat",
        "difficulty": "Medium",
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
        "best_moves": ["f1c1", "g1f1"],
        "description": "White's king is exposed on the back rank. Find a safe move."
    },
    {
        "id": 3,
        "name": "Pawn Promotion",
        "difficulty": "Easy",
        "fen": "8/6P1/8/8/8/8/8/7k w - - 0 1",
        "best_moves": ["g7g8q"],
        "description": "White has a passed pawn near promotion. Promote to a queen to win!"
    },
    {
        "id": 4,
        "name": "Checkmate in One",
        "difficulty": "Hard",
        "fen": "7k/5Q2/6K1/8/8/8/8/8 w - - 0 1",
        "best_moves": ["f7f8"],
        "description": "White can checkmate in one move. Find it!"
    },
    {
        "id": 5,
        "name": "Discovered Attack",
        "difficulty": "Medium",
        "fen": "r1bqkbnr/pppppppp/2n5/8/8/3P1N2/PPP1PPPP/RNBQKB1R b KQkq - 0 1",
        "best_moves": ["c6d4"],
        "description": "Black can create a discovered attack. Find the move!"
    },
    {
        "id": 6,
        "name": "Pin the Bishop",
        "difficulty": "Medium",
        "fen": "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 1",
        "best_moves": ["f3e5"],
        "description": "White's knight can move to a powerful square. Find it!"
    },
    {
        "id": 7,
        "name": "Escape the Trap",
        "difficulty": "Hard",
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/2N5/PPPP1PPP/R1BQK1NR w KQkq - 0 1",
        "best_moves": ["c4d5"],
        "description": "White's bishop is attacked. Find the move that counterattacks!"
    },
    {
        "id": 8,
        "name": "Fork Attack",
        "difficulty": "Easy",
        "fen": "rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 1",
        "best_moves": ["c3d5"],
        "description": "White's knight can fork multiple pieces. Find the winning move!"
    },
]


def get_puzzles_by_difficulty(difficulty):
    """
    Get puzzles filtered by difficulty level.
    
    Args:
        difficulty (str): Difficulty level - 'Easy', 'Medium', or 'Hard'
    
    Returns:
        list: Puzzles matching the difficulty
    """
    return [p for p in PUZZLES if p.get("difficulty") == difficulty]


def add_custom_puzzle(puzzle_id, name, fen, best_moves, difficulty, description=""):
    """
    Add a custom puzzle to the collection.
    
    Args:
        puzzle_id (int): Unique puzzle ID
        name (str): Puzzle name
        fen (str): FEN position string
        best_moves (list): List of best moves in UCI format
        difficulty (str): Difficulty level
        description (str): Optional puzzle description
    """
    puzzle = {
        "id": puzzle_id,
        "name": name,
        "difficulty": difficulty,
        "fen": fen,
        "best_moves": best_moves,
        "description": description
    }
    PUZZLES.append(puzzle)
