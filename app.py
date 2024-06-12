import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from agent import DQNAgent
from game import Hexapawn
import logging

app = Flask(__name__)
CORS(app)

# Initialize the game and agent
env = Hexapawn()
state_size = env.reset().shape[0]
action_size = 9  # 3x3 grid with 9 possible moves
agent = DQNAgent(state_size, action_size)
agent.load("models/hexapawn-dqn")  # Ensure this is the correct file name and path

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def board_to_json(board):
    return {'board': board.tolist()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    state = env.reset()
    return jsonify(board_to_json(env.board))

@app.route('/valid_moves', methods=['POST'])
def valid_moves():
    data = request.get_json()
    position = tuple(data['position'])
    logging.debug(f"Received position for valid moves: {position}")
    
    valid_moves = [move[1] for move in env.valid_moves() if move[0] == position]
    logging.debug(f"Valid moves for position {position}: {valid_moves}")
    
    return jsonify({'valid_moves': valid_moves})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    logging.debug(f"Received move: {data['move']}")
    try:
        human_move = (tuple(data['move'][0]), tuple(data['move'][1]))  # Convert move to tuple of tuples
        valid_moves = env.valid_moves()
        logging.debug(f"Valid moves: {valid_moves}")

        if human_move not in valid_moves:
            logging.debug(f"Invalid move: {human_move}")
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
        logging.error(f"Error processing move: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
