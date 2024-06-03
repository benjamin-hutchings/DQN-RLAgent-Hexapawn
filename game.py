import numpy as np

class Hexapawn:
    def __init__(self):
        self.board = np.array([[1, 1, 1],
                               [0, 0, 0],
                               [-1, -1, -1]])
        self.current_player = 1  # 1 for agent, -1 for opponent

    def reset(self):
        self.board = np.array([[1, 1, 1],
                               [0, 0, 0],
                               [-1, -1, -1]])
        self.current_player = 1
        return self.board.flatten()

    def valid_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r, c] == self.current_player:
                    if self.current_player == 1 and r < 2:
                        if self.board[r + 1, c] == 0:
                            moves.append(((r, c), (r + 1, c)))
                        if c > 0 and self.board[r + 1, c - 1] == -1:
                            moves.append(((r, c), (r + 1, c - 1)))
                        if c < 2 and self.board[r + 1, c + 1] == -1:
                            moves.append(((r, c), (r + 1, c + 1)))
                    elif self.current_player == -1 and r > 0:
                        if self.board[r - 1, c] == 0:
                            moves.append(((r, c), (r - 1, c)))
                        if c > 0 and self.board[r - 1, c - 1] == 1:
                            moves.append(((r, c), (r - 1, c - 1)))
                        if c < 2 and self.board[r - 1, c + 1] == 1:
                            moves.append(((r, c), (r - 1, c + 1)))
        return moves

    def step(self, move):
        (r1, c1), (r2, c2) = move
        self.board[r2, c2] = self.board[r1, c1]
        self.board[r1, c1] = 0
        reward = self.check_winner()
        done = reward != 0 or not self.valid_moves()
        self.current_player *= -1
        return self.board.flatten(), reward, done

    def check_winner(self):
        if np.any(self.board[2, :] == 1) or not np.any(self.board == -1):
            return 1
        if np.any(self.board[0, :] == -1) or not np.any(self.board == 1):
            return -1
        return 0
