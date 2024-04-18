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
        pass

    def remember(self, state, action, reward, next_state, game_over):
        pass

    def train_long_memory(self):
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