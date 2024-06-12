document.addEventListener("DOMContentLoaded", function() {
    const boardElement = document.getElementById('board');
    const resetButton = document.getElementById('reset-button');
    const messageElement = document.getElementById('message');
    let board = [];
    let selectedCell = null;
    let currentPhase = 'selectCross'; // Initial phase

    const apiUrl = ""; // Leave empty to use the same origin as the frontend

    function renderBoard() {
        boardElement.innerHTML = '';
        for (let row = 0; row < 3; row++) {
            const tr = document.createElement('tr');
            for (let col = 0; col < 3; col++) {
                const td = document.createElement('td');
                td.dataset.row = row;
                td.dataset.col = col;
                td.textContent = convertToSymbol(board[row][col]);
                td.addEventListener('click', handleCellClick);
                tr.appendChild(td);
            }
            boardElement.appendChild(tr);
        }
    }

    function convertToSymbol(value) {
        if (value === 1) return 'X';
        if (value === -1) return 'O';
        return '';
    }

    function handleCellClick(event) {
        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

        if (currentPhase === 'selectCross') {
            if (board[row][col] === 1) {
                selectedCell = { row, col };
                highlightValidMoves(row, col);
                currentPhase = 'selectPosition';
            }
        } else if (currentPhase === 'selectPosition') {
            if (event.target.classList.contains('valid-move')) {
                const startRow = selectedCell.row;
                const startCol = selectedCell.col;
                const endRow = row;
                const endCol = col;

                makeMove(startRow, startCol, endRow, endCol);
                clearHighlights();
                selectedCell = null;
                currentPhase = 'selectCross';
            }
        }
    }

    function highlightValidMoves(row, col) {
        fetch(`${apiUrl}/valid_moves`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ position: [row, col] })
        })
        .then(response => response.json())
        .then(data => {
            data.valid_moves.forEach(move => {
                const [endRow, endCol] = move;
                const cell = document.querySelector(`[data-row="${endRow}"][data-col="${endCol}"]`);
                cell.classList.add('valid-move');
            });
        });
    }

    function clearHighlights() {
        document.querySelectorAll('.valid-move').forEach(cell => {
            cell.classList.remove('valid-move');
        });
    }

    function resetGame() {
        fetch(`${apiUrl}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            board = data.board;
            renderBoard();
            currentPhase = 'selectCross';
            messageElement.textContent = ''; // Clear the message
        });
    }

    function makeMove(startRow, startCol, endRow, endCol) {
        fetch(`${apiUrl}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ move: [[startRow, startCol], [endRow, endCol]] })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageElement.textContent = data.error;
            } else {
                board = data.board;
                renderBoard();
                if (data.result) {
                    messageElement.textContent = `Game over! Result: ${data.result}. Please reset the board.`;
                }
            }
        });
    }

    resetButton.addEventListener('click', resetGame);

    resetGame();
});
