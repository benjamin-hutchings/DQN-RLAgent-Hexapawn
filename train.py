import numpy as np
from agent import DQNAgent
from game import Hexapawn

EPISODES = 100
BATCH_SIZE = 32
env = Hexapawn()
state_size = env.reset().shape[0]
action_size = 9  # 3x3 grid with 9 possible moves
agent = DQNAgent(state_size, action_size)

for e in range(EPISODES):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    print(f"Episode {e + 1}/{EPISODES} started with epsilon {agent.epsilon:.2f}.")
    
    for time in range(50):
        valid_moves = env.valid_moves()
        if not valid_moves:
            print("No valid moves left.")
            break
        
        action = agent.act(state, valid_moves)
        move = valid_moves[action]
        print(f"Step {time + 1} - Action taken: {move}")
        
        next_state, reward, done = env.step(move)
        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        
        print(f"Step {time + 1} - Reward received: {reward}, Done: {done}")
        
        if done:
            print(f"Episode {e + 1}/{EPISODES} finished after {time + 1} steps. Epsilon: {agent.epsilon:.2}")
            break
        
        if len(agent.memory) > BATCH_SIZE:
            print(f"Training on batch of size {BATCH_SIZE}.")
            agent.replay(BATCH_SIZE)
    
    if (e + 1) % 10 == 0:
        print(f"Saving model at episode {e + 1}.")
        agent.save("hexapawn-dqn")

agent.save("hexapawn-dqn")
print("Training completed. Model saved.")
