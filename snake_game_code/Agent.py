import pygame
import random
import torch
import numpy as np
from collections import deque
from snake_game import Snake_game

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 0 ### control the randomness
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        pass

    def get_state(self, game):
        head = game.snake[0]

        ### Find current step x, y
        to_up = (head[0], head[1]-20)
        to_down = (head[0], head[1]+20)
        to_left = (head[0]-20, head[1])
        to_right = (head[0]+20, head[1])

        ### Determine which one are the current direction
        go_up = (game.x_change == 0 and game.y_change < 0)
        go_down = (game.x_change == 0 and game.y_change > 0)
        go_right = (game.x_change > 0 and game.y_change == 0)
        go_left = (game.x_change < 0 and game.y_change < 0)

        state = [
            (go_up and game.crash(to_up)) or
            (go_down and game.crash(to_down)) or
            (go_right and game.crash(to_right)) or
            (go_left and game.crash(to_left)),

            (go_up and game.is_collision(to_right)) or 
            (go_down and game.is_collision(to_left)) or 
            (go_left and game.is_collision(to_up)) or 
            (go_right and game.is_collision(to_down)),

            (go_down and game.is_collision(to_right)) or 
            (go_up and game.is_collision(to_left)) or 
            (go_right and game.is_collision(to_up)) or 
            (go_left and game.is_collision(to_down)),

            go_up,
            go_down,
            go_right,
            go_left,

            game.food[0] < game.head[0],  # food left
            game.food[0] > game.head[0],  # food right
            game.food[1] < game.head[1],  # food up
            game.food[1] > game.head[1]  # food down
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory((state, action, reward, next_state, game_over))
        pass

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        state, action, reward, next_state, game_over = zip(*mini_sample)
        self.trainer.train_step(state, action, reward, next_state, game_over)
        pass

    def train_short_memory(self, state, action, reward, next_state, game_over):
        
        pass

    def get_action(self, state):
        pass

def train():

    total_score = 0
    record = 0

    agent = Agent()
    game = Snake_game()

    ### Init game over == False
    is_game_over = game.game_over

    while True:

        state_old = agent.get_state(game)

        next_move = agent.get_action(state_old)

        reward, is_game_over, score = game.play_game(next_move)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, next_move, reward, state_new, is_game_over)

        agent.remember(state_old, next_move, reward, state_new, is_game_over)

        if is_game_over:
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()


if __name__ == "__main__":
    train()
    pygame.quit()