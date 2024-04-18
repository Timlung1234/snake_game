import pygame
import random
import torch
import numpy as np
from snake_game import Snake_game


class Agent:
    pass

def train():

    agent = Agent()
    game = Snake_game()

    ### Init game over == False
    is_game_over = game.game_over

    while True:
        reward, is_game_over, score = game.play_game()

        if is_game_over:
            game.reset()


if __name__ == "__main__":
    train()
    pygame.quit()