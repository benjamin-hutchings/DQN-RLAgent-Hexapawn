import numpy as np
from agent import DQNAgent
from game import Hexapawn

# Load the trained agent
env = Hexapawn()
state_size = env.reset().shape[0]
action_size = 9  # 3x3 grid with 9 possible moves
agent = DQNAgent(state_size, action_size)
agent.load("hexapawn-dqn")

def print_board(board):
    board_symbols = {1: 'X', -1: 'O', 0: '.'}
    for row in board:
        print(' '.join(board_symbols[cell] for cell in row))
    print()

def human_move(board, valid_moves):
    print_board(board)
    print("Valid moves (in the form (from_row, from_col) -> (to_row, to_col)):")
    for i, move in enumerate(valid_moves):
        print(f"{i}: {move[0]} -> {move[1]}")
    
    while True:
        try:
            move_index = int(input("Enter the number of your chosen move: "))
            if move_index < 0 or move_index >= len(valid_moves):
                raise ValueError
            return valid_moves[move_index]
        except ValueError:
            print(f"Invalid input. Please enter a number between 0 and {len(valid_moves) - 1}.")

def play_game():
    try:
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        board_positions = [env.board.copy()]
        
        while True:
            valid_moves = env.valid_moves()
            if not valid_moves:
                print("No valid moves left for you. It's a draw!")
                break
            
            print("Your turn:")
            human_action = human_move(env.board, valid_moves)
            next_state, reward, done = env.step(human_action)
            board_positions.append(env.board.copy())
            print_board(env.board)
            if reward == 1:
                print("You win!")
                break
            elif done:
                if reward == -1:
                    print("Agent wins!")
                else:
                    print("No valid moves left for the agent. It's a draw!")
                break
            
            state = np.reshape(next_state, [1, state_size])
            valid_moves = env.valid_moves()
            if not valid_moves:
                print("No valid moves left for the agent. It's a draw!")
                break
            
            print("Agent's turn:")
            agent_action_index = agent.act(state, valid_moves)
            agent_action = valid_moves[agent_action_index]
            next_state, reward, done = env.step(agent_action)
            board_positions.append(env.board.copy())
            print_board(env.board)
            if reward == -1:
                print("Agent wins!")
                break
            elif done:
                if reward == 1:
                    print("You win!")
                else:
                    print("No valid moves left for you. It's a draw!")
                break
            
            state = np.reshape(next_state, [1, state_size])
        
        print("Game over! Let's replay the game board by board:")
        for i, board in enumerate(board_positions):
            print(f"Board position after move {i}:")
            print_board(board)
            
    except Exception as e:
        print(f"An error occurred during the game: {e}")

play_game()