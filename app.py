import numpy as np
from flask import Flask, jsonify, request, render_template
from agent import DQNAgent
from game import Hexapawn

app = Flask(__name__)

# Initialize the game and agent
env = Hexapawn()
state_size = env.reset().shape[0]
action_size = 9  # 3x3 grid with 9 possible moves
agent = DQNAgent(state_size, action_size)
agent.load("models/hexapawn-dqn")

def board_to_json(board):
    return {'board': board.tolist()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    state = env.reset()
    return jsonify(board_to_json(env.board))

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    try:
        human_move = tuple(map(tuple, data['move']))  # Ensure the move data is a tuple of tuples
        valid_moves = env.valid_moves()
        
        if human_move not in valid_moves:
            return jsonify({'error': 'Invalid move'}), 400
        
        next_state, reward, done = env.step(human_move)
        
        if done:
            result = 'draw' if reward == 0 else 'win' if reward == 1 else 'lose'
            return jsonify({'board': env.board.tolist(), 'result': result})
        
        state = np.reshape(next_state, [1, state_size])
        valid_moves = env.valid_moves()
        agent_action_index = agent.act(state, valid_moves)
        agent_action = valid_moves[agent_action_index]
        next_state, reward, done = env.step(agent_action)
        
        result = 'draw' if done and reward == 0 else 'lose' if reward == -1 else None
        
        return jsonify({'board': env.board.tolist(), 'result': result})
    except Exception as e:
        print(f"Error processing move: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
