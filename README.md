# Hexapawn Game with Deep Q-Network (DQN)

## Table of Contents

- [Introduction](#introduction)
- [How to Play](#how-to-play)
- [Technical Details](#technical-details)
  - [Deep Q-Network (DQN)](#deep-q-network-dqn)
  - [Technologies Used](#technologies-used)
  - [Design Steps](#design-steps)
  - [Future Work](#future-work)
- [Installation](#installation)
  - [Local Development](#local-development)
  - [Docker](#docker)
- [Deployment](#deployment)
  - [Heroku](#heroku)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository contains the source code for a Hexapawn game where the player competes against a Deep Q-Network (DQN) agent. The project serves as a proof of concept to demonstrate the integration of a deep learning model within a web application, allowing users to interact with an AI agent in real-time.

## How to Play

Hexapawn is a simple two-player game played on a 3x3 grid. The objective is to either:
1. Reach the opposite side of the board with one of your pawns.
2. Block your opponent such that they have no valid moves left.

In this implementation, you play as 'X' against the DQN agent playing as 'O'. To make a move, select one of your pawns and then choose a valid position to move to.

## Technical Details

### Deep Q-Network (DQN)

The DQN agent is trained using the following methodology:
- **State Representation:** The board is represented as a 1D array of size 9 (3x3 grid).
- **Action Space:** There are 9 possible moves (each cell in the grid).
- **Neural Network:** The agent uses a neural network with three fully connected layers to predict the Q-values for each action.
- **Training:** The agent was trained using 100 episodes, with experience replay and target network updates to stabilize learning.

The training script (`train.py`) sets up the environment, initializes the agent, and runs the training loop where the agent plays games against itself, learning from each game.

### Technologies Used

This application leverages several technologies:
- **Python:** For the backend logic and DQN training.
- **Flask:** For serving the web application.
- **JavaScript:** For handling the frontend interactions.
- **Docker:** For containerizing the application and making it easily deployable.
- **Heroku:** For hosting the application online.

### Design Steps

The design process involved the following steps:
1. Define the game logic for Hexapawn.
2. Develop the DQN agent and train it using self-play.
3. Build the Flask backend to serve the game and handle moves.
4. Create a simple HTML/CSS/JavaScript frontend for user interaction.
5. Containerize the application using Docker.
6. Deploy the application to Heroku.

### Future Work

This project was a proof of concept to understand the process of building and deploying a game with a deep learning agent. The next steps involve:
- Exploring more complex games and environments.
- Improving the training process for the DQN agent.
- Enhancing the frontend for a better user experience.

## Installation

### Local Development

To run the application locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/hexapawn-dqn.git
    cd hexapawn-dqn
    ```

2. Set up a virtual environment and install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Start the Flask application:
    ```sh
    python app.py
    ```

4. Open your browser and go to `http://127.0.0.1:5000/` to see the application.

### Docker

To run the application using Docker:

1. Build the Docker image:
    ```sh
    docker build -t hexapawn-flask-app .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 5000:5000 hexapawn-flask-app
    ```

3. Open your browser and go to `http://localhost:5000/` to see the application.

## Deployment

### Heroku

To deploy the application to Heroku:

1. Log in to Heroku:
    ```sh
    heroku login
    ```

2. Create a new Heroku application:
    ```sh
    heroku create your-app-name
    ```

3. Push the code to Heroku:
    ```sh
    git push heroku main
    ```

4. Scale the application:
    ```sh
    heroku ps:scale web=1
    ```

5. Open the deployed application:
    ```sh
    heroku open
    ```

## Usage

Once the application is running, you can interact with the Hexapawn game via the web interface. The interface allows you to reset the game, select a pawn, and make a move by selecting a valid target position. The DQN agent will then make its move.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes. Ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
