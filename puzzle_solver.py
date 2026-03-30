"""
Puzzle management and solving module.
Handles loading puzzles, tracking progress, and validating solutions.
"""

from puzzles.sample_puzzles import PUZZLES


class PuzzleSolver:
    """Manages chess puzzles and tracks solving progress."""
    
    def __init__(self):
        """Initialize the puzzle solver."""
        self.puzzles = PUZZLES
        self.current_puzzle_index = 0
        self.solved_puzzles = set()
        self.puzzle_attempts = {}
    
    def get_current_puzzle(self):
        """
        Get the current puzzle.
        
        Returns:
            dict: Puzzle data including fen, best_moves, difficulty, etc.
        """
        if self.current_puzzle_index < len(self.puzzles):
            return self.puzzles[self.current_puzzle_index]
        return None
    
    def get_puzzle_by_id(self, puzzle_id):
        """
        Get a puzzle by its ID.
        
        Args:
            puzzle_id (int): ID of the puzzle
            
        Returns:
            dict: Puzzle data, or None if not found
        """
        for puzzle in self.puzzles:
            if puzzle["id"] == puzzle_id:
                return puzzle
        return None
    
    def get_all_puzzles(self):
        """
        Get all available puzzles.
        
        Returns:
            list: List of all puzzles
        """
        return self.puzzles
    
    def next_puzzle(self):
        """
        Move to the next puzzle.
        
        Returns:
            bool: True if there's a next puzzle, False otherwise
        """
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.current_puzzle_index += 1
            return True
        return False
    
    def previous_puzzle(self):
        """
        Move to the previous puzzle.
        
        Returns:
            bool: True if there's a previous puzzle, False otherwise
        """
        if self.current_puzzle_index > 0:
            self.current_puzzle_index -= 1
            return True
        return False
    
    def select_puzzle(self, puzzle_id):
        """
        Select a specific puzzle by ID.
        
        Args:
            puzzle_id (int): ID of the puzzle
            
        Returns:
            bool: True if puzzle was found and selected
        """
        for i, puzzle in enumerate(self.puzzles):
            if puzzle["id"] == puzzle_id:
                self.current_puzzle_index = i
                return True
        return False
    
    def is_solution_correct(self, move_uci):
        """
        Check if a move is one of the best moves for current puzzle.
        
        Args:
            move_uci (str): Move in UCI format
            
        Returns:
            bool: True if move is among the best moves
        """
        puzzle = self.get_current_puzzle()
        if not puzzle:
            return False
        return move_uci in puzzle.get("best_moves", [])
    
    def mark_puzzle_solved(self, puzzle_id):
        """
        Mark a puzzle as solved.
        
        Args:
            puzzle_id (int): ID of the puzzle
        """
        self.solved_puzzles.add(puzzle_id)
    
    def is_puzzle_solved(self, puzzle_id):
        """
        Check if a puzzle has been solved.
        
        Args:
            puzzle_id (int): ID of the puzzle
            
        Returns:
            bool: True if puzzle was solved
        """
        return puzzle_id in self.solved_puzzles
    
    def record_attempt(self, puzzle_id, move_uci, correct):
        """
        Record an attempt on a puzzle.
        
        Args:
            puzzle_id (int): ID of the puzzle
            move_uci (str): Move attempted
            correct (bool): Whether the move was correct
        """
        if puzzle_id not in self.puzzle_attempts:
            self.puzzle_attempts[puzzle_id] = []
        
        self.puzzle_attempts[puzzle_id].append({
            "move": move_uci,
            "correct": correct
        })
    
    def get_attempts(self, puzzle_id):
        """
        Get all attempts for a puzzle.
        
        Args:
            puzzle_id (int): ID of the puzzle
            
        Returns:
            list: List of attempts
        """
        return self.puzzle_attempts.get(puzzle_id, [])
    
    def get_progress(self):
        """
        Get overall puzzle-solving progress.
        
        Returns:
            dict: Progress statistics
        """
        total = len(self.puzzles)
        solved = len(self.solved_puzzles)
        
        return {
            "total_puzzles": total,
            "solved_puzzles": solved,
            "progress_percentage": (solved / total * 100) if total > 0 else 0,
            "current_puzzle_index": self.current_puzzle_index + 1
        }
    
    def add_puzzle(self, puzzle_data):
        """
        Add a new puzzle to the collection.
        
        Args:
            puzzle_data (dict): Puzzle data with id, name, fen, best_moves, etc.
        """
        self.puzzles.append(puzzle_data)
    
    def add_multiple_puzzles(self, puzzles_list):
        """
        Add multiple puzzles at once.
        
        Args:
            puzzles_list (list): List of puzzle dictionaries
        """
        self.puzzles.extend(puzzles_list)
