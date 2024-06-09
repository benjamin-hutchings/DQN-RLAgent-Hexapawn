document.addEventListener("DOMContentLoaded", function() {
    const boardElement = document.getElementById('board');
    let board = [];

    const apiUrl = "https://play-hexapawn-e5aa909e0052.herokuapp.com/"; // Replace with your Heroku app URL

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
        const row = event.target.dataset.row;
        const col = event.target.dataset.col;
        makeMove(parseInt(row), parseInt(col));
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
        });
    }

    function makeMove(row, col) {
        fetch(`${apiUrl}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ move: [[row, col]] })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                board = data.board;
                renderBoard();
                if (data.result) {
                    alert(`Game over! Result: ${data.result}`);
                }
            }
        });
    }

    resetGame();
});
