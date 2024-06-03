const symbols = {"1": 'X', "-1": 'O', "0": '.'};  // Object keys must be strings
let board = [];
let selectedPiece = null;
let validMoves = [];

function renderBoard() {
    const table = document.getElementById('board');
    table.innerHTML = '';
    for (let r = 0; r < 3; r++) {
        const row = document.createElement('tr');
        for (let c = 0; c < 3; c++) {
            const cell = document.createElement('td');
            cell.textContent = symbols[board[r][c].toString()];
            cell.className = '';
            if (selectedPiece && validMoves.includes(`${r},${c}`)) {
                cell.className = 'highlight';
                cell.onclick = () => makeMove(selectedPiece, [r, c]);
            } else if (board[r][c] === 1) {
                cell.onclick = () => selectPiece([r, c]);
            }
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
}

async function resetGame() {
    try {
        const response = await fetch('/reset', {method: 'POST'});
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Game reset:', data);
        board = data.board;
        selectedPiece = null;
        validMoves = [];
        renderBoard();
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

function selectPiece(piece) {
    selectedPiece = piece;
    validMoves = [];
    const r = piece[0];
    const c = piece[1];
    if (r < 2 && board[r + 1][c] === 0) {
        validMoves.push(`${r + 1},${c}`);
    }
    if (r < 2 && c > 0 && board[r + 1][c - 1] === -1) {
        validMoves.push(`${r + 1},${c - 1}`);
    }
    if (r < 2 && c < 2 && board[r + 1][c + 1] === -1) {
        validMoves.push(`${r + 1},${c + 1}`);
    }
    renderBoard();
}

async function makeMove(from, to) {
    try {
        const move = [from, to];
        const response = await fetch('/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({move: move})
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }
        console.log('Move made:', data);
        board = data.board;
        selectedPiece = null;
        validMoves = [];
        renderBoard();
        if (data.result) {
            alert(`Game over: ${data.result}`);
        }
    } catch (error) {
        console.error('Error making move:', error);
    }
}

window.onload = resetGame;
