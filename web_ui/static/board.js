// Chess Tutor Web UI - Frontend Logic

// Piece Unicode symbols
const PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
};

// State
let currentPuzzle = null;
let currentBoard = null;
let selectedSquare = null;
let moveHistory = [];
let legalMoves = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadCurrentPuzzle();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    document.getElementById('submitBtn').addEventListener('click', submitMove);
    document.getElementById('moveInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitMove();
    });
    document.getElementById('hintsBtn').addEventListener('click', getHints);
    document.getElementById('undoBtn').addEventListener('click', undoMove);
    document.getElementById('resetBtn').addEventListener('click', resetBoard);
    document.getElementById('prevBtn').addEventListener('click', previousPuzzle);
    document.getElementById('nextBtn').addEventListener('click', nextPuzzle);
}

// Load current puzzle
async function loadCurrentPuzzle() {
    try {
        const response = await fetch('/api/puzzle/current');
        const data = await response.json();
        
        if (!response.ok) {
            showFeedback('Error loading puzzle', 'error');
            return;
        }
        
        currentPuzzle = data;
        currentBoard = data.fen;
        legalMoves = data.legal_moves;
        moveHistory = [];
        
        updatePuzzleInfo();
        renderBoard();
        updateProgress(data.progress);
        loadPuzzlesList();
        
        clearFeedback();
        document.getElementById('moveInput').focus();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Update puzzle information
function updatePuzzleInfo() {
    document.getElementById('puzzleName').textContent = currentPuzzle.name;
    document.getElementById('puzzleDescription').textContent = currentPuzzle.description;
    
    const diffBadge = document.getElementById('difficultyBadge');
    diffBadge.textContent = currentPuzzle.difficulty.toUpperCase();
    diffBadge.className = `difficulty ${currentPuzzle.difficulty.toLowerCase()}`;
    
    document.getElementById('puzzleNumber').textContent = 
        `Puzzle ${currentPuzzle.progress.index + 1} / ${currentPuzzle.progress.total}`;
}

// Render chess board
function renderBoard() {
    const board = document.getElementById('chessboard');
    board.innerHTML = '';
    
    const fen = currentBoard;
    const fenParts = fen.split(' ');
    const position = fenParts[0];
    
    let squareIndex = 0;
    const ranks = position.split('/');
    
    for (let rank = 0; rank < 8; rank++) {
        const rankStr = ranks[rank];
        let file = 0;
        
        for (let char of rankStr) {
            if (isNaN(char)) {
                // It's a piece
                addBoardSquare(board, rank, file, char, squareIndex);
                file++;
                squareIndex++;
            } else {
                // It's empty squares
                const emptyCount = parseInt(char);
                for (let i = 0; i < emptyCount; i++) {
                    addBoardSquare(board, rank, file, '', squareIndex);
                    file++;
                    squareIndex++;
                }
            }
        }
    }
    
    updateLegalMovesDisplay();
}

// Add board square
function addBoardSquare(board, rank, file, piece, squareIndex) {
    const square = document.createElement('div');
    square.className = 'square';
    
    // Determine if square is light or dark
    if ((rank + file) % 2 === 0) {
        square.classList.add('light');
    } else {
        square.classList.add('dark');
    }
    
    // Convert rank/file to algebraic notation
    const fileChar = String.fromCharCode(97 + file); // a-h
    const rankNum = 8 - rank; // 8-1
    const squareName = fileChar + rankNum;
    
    square.id = squareName;
    square.dataset.square = squareName;
    
    // Add piece
    if (piece && PIECES[piece]) {
        const pieceEl = document.createElement('span');
        pieceEl.className = 'piece';
        pieceEl.textContent = PIECES[piece];
        square.appendChild(pieceEl);
    }
    
    // Click handler
    square.addEventListener('click', () => selectSquare(squareName, piece));
    
    board.appendChild(square);
}

// Handle square selection
function selectSquare(squareName, piece) {
    // If clicking on a legal move destination
    if (selectedSquare && legalMoves.some(m => m.endsWith(squareName))) {
        const moveUci = selectedSquare + squareName;
        if (legalMoves.includes(moveUci)) {
            document.getElementById('moveInput').value = moveUci;
            submitMove();
            deselectSquare();
            return;
        }
    }
    
    // If clicking on own piece
    if (piece && piece !== '.') {
        selectedSquare = squareName;
        highlightSquare(squareName);
        highlightLegalMoves(squareName);
    } else {
        deselectSquare();
    }
}

// Highlight selected square
function highlightSquare(squareName) {
    document.querySelectorAll('.square').forEach(sq => sq.classList.remove('selected'));
    const square = document.getElementById(squareName);
    if (square) square.classList.add('selected');
}

// Highlight legal moves from position
function highlightLegalMoves(fromSquare) {
    document.querySelectorAll('.square').forEach(sq => sq.classList.remove('legal-move'));
    
    legalMoves.forEach(move => {
        if (move.startsWith(fromSquare)) {
            const toSquare = move.substring(2, 4);
            const square = document.getElementById(toSquare);
            if (square) square.classList.add('legal-move');
        }
    });
}

// Deselect square
function deselectSquare() {
    selectedSquare = null;
    document.querySelectorAll('.square').forEach(sq => {
        sq.classList.remove('selected', 'legal-move');
    });
}

// Update legal moves display
function updateLegalMovesDisplay() {
    const list = document.getElementById('legalMovesList');
    list.innerHTML = '';
    
    legalMoves.slice(0, 12).forEach(move => {
        const badge = document.createElement('span');
        badge.className = 'legal-move-badge';
        badge.textContent = move;
        badge.addEventListener('click', () => {
            document.getElementById('moveInput').value = move;
            submitMove();
        });
        list.appendChild(badge);
    });
    
    if (legalMoves.length > 12) {
        const more = document.createElement('span');
        more.className = 'legal-move-badge';
        more.textContent = `+${legalMoves.length - 12} more`;
        more.style.cursor = 'default';
        list.appendChild(more);
    }
}

// Submit move
async function submitMove() {
    const move = document.getElementById('moveInput').value.trim().toLowerCase();
    
    if (!move) {
        showFeedback('Please enter a move', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/move/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ move })
        });
        
        const data = await response.json();
        
        if (!data.valid) {
            showFeedback(data.message || 'Invalid move', 'error');
            return;
        }
        
        // Update board
        currentBoard = data.board_display;
        legalMoves = data.legal_moves;
        moveHistory.push(move);
        
        // Update UI
        renderBoard();
        updateMoveHistory();
        
        if (data.is_solution) {
            showFeedback(data.message, 'success');
            if (data.progress) {
                updateProgress(data.progress);
                loadPuzzlesList();
            }
            document.getElementById('nextBtn').focus();
        } else {
            showFeedback(data.message, 'info');
        }
        
        document.getElementById('moveInput').value = '';
        deselectSquare();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Get hints
async function getHints() {
    try {
        const response = await fetch('/api/move/hints');
        const data = await response.json();
        
        if (!response.ok) {
            showFeedback(data.message || 'Could not get hints', 'error');
            return;
        }
        
        const hintsPanel = document.getElementById('hintsPanel');
        const hintsList = document.getElementById('hintsList');
        hintsList.innerHTML = '';
        
        data.hints.forEach(hint => {
            const item = document.createElement('div');
            item.className = 'hint-item';
            
            if (typeof hint === 'string') {
                item.innerHTML = `
                    <span class="hint-move">${hint}</span>
                `;
            } else {
                const score = hint.score ? (hint.score > 0 ? '+' : '') + hint.score.toFixed(2) : '?';
                item.innerHTML = `
                    <span class="hint-move">${hint.move}</span>
                    <span class="hint-score">${score}</span>
                `;
            }
            
            item.addEventListener('click', () => {
                const hintMove = hint.move || hint;
                document.getElementById('moveInput').value = hintMove;
                submitMove();
            });
            
            hintsList.appendChild(item);
        });
        
        hintsPanel.style.display = 'block';
        showFeedback(data.message, 'info');
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Undo move
async function undoMove() {
    try {
        const response = await fetch('/api/board/undo', { method: 'POST' });
        const data = await response.json();
        
        if (!data.success) {
            showFeedback(data.error || 'Cannot undo', 'error');
            return;
        }
        
        currentBoard = data.board_display;
        legalMoves = data.legal_moves;
        if (moveHistory.length > 0) moveHistory.pop();
        
        renderBoard();
        updateMoveHistory();
        showFeedback('Move undone', 'info');
        deselectSquare();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Reset board
async function resetBoard() {
    try {
        const response = await fetch('/api/board/reset', { method: 'POST' });
        const data = await response.json();
        
        if (!data.success) {
            showFeedback(data.error || 'Cannot reset', 'error');
            return;
        }
        
        currentBoard = data.board_display;
        legalMoves = data.legal_moves;
        moveHistory = [];
        
        renderBoard();
        updateMoveHistory();
        showFeedback('Board reset to starting position', 'info');
        deselectSquare();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Update move history
function updateMoveHistory() {
    const moveList = document.getElementById('moveList');
    
    if (moveHistory.length === 0) {
        moveList.innerHTML = '<span class="empty-moves">No moves yet</span>';
        return;
    }
    
    moveList.innerHTML = moveHistory
        .map(move => `<span class="move-item">${move}</span>`)
        .join('');
}

// Navigate to next puzzle
async function nextPuzzle() {
    try {
        const response = await fetch('/api/puzzle/next', { method: 'POST' });
        
        if (!response.ok) {
            showFeedback('No more puzzles', 'info');
            return;
        }
        
        await loadCurrentPuzzle();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Navigate to previous puzzle
async function previousPuzzle() {
    try {
        const response = await fetch('/api/puzzle/previous', { method: 'POST' });
        
        if (!response.ok) {
            showFeedback('No previous puzzle', 'info');
            return;
        }
        
        await loadCurrentPuzzle();
    } catch (error) {
        showFeedback(`Error: ${error.message}`, 'error');
    }
}

// Load puzzles list
async function loadPuzzlesList() {
    try {
        const response = await fetch('/api/puzzles/list');
        const data = await response.json();
        
        const puzzlesList = document.getElementById('puzzlesList');
        puzzlesList.innerHTML = '';
        
        data.puzzles.forEach(puzzle => {
            const item = document.createElement('div');
            item.className = 'puzzle-item';
            if (puzzle.id === currentPuzzle.id) item.classList.add('active');
            
            item.innerHTML = `
                <span class="puzzle-item-name">${puzzle.id}. ${puzzle.name}</span>
                <span class="puzzle-item-status">${puzzle.solved ? '✓' : ''}</span>
            `;
            
            item.addEventListener('click', async () => {
                try {
                    const selectResponse = await fetch(`/api/puzzle/select/${puzzle.id}`, { method: 'POST' });
                    if (selectResponse.ok) {
                        await loadCurrentPuzzle();
                    }
                } catch (error) {
                    showFeedback(`Error: ${error.message}`, 'error');
                }
            });
            
            puzzlesList.appendChild(item);
        });
    } catch (error) {
        showFeedback(`Error loading puzzles: ${error.message}`, 'error');
    }
}

// Update progress
function updateProgress(progress) {
    const percentage = (progress.solved / progress.total) * 100;
    document.getElementById('progressFill').style.width = percentage + '%';
    document.getElementById('progressText').textContent = 
        `${progress.solved} / ${progress.total} solved`;
}

// Show feedback
function showFeedback(message, type) {
    const feedback = document.getElementById('feedback');
    feedback.textContent = message;
    feedback.className = `feedback ${type}`;
}

// Clear feedback
function clearFeedback() {
    const feedback = document.getElementById('feedback');
    feedback.textContent = '';
    feedback.className = 'feedback empty';
}
