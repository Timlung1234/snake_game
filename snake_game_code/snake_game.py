import pygame
import random
import torch
import numpy as np

### Set up color
class Color:
    yellow = (255, 255, 102)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

class Snake_game:

    def __init__(self, width=720, height=480):
        ### Initialize
        pygame.init()

        ### Game window setup
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

        ### Font style
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        
        ### Game status & setting
        self.snake_speed = 10
        self.object_size = 20

        ### Init / Reset all game element
        self.reset()

    def generate_xy(self) -> tuple:
        x = round(random.randint(0, self.screen_width) / self.object_size) * self.object_size
        y = round(random.randint(0, self.screen_width) / self.object_size) * self.object_size

        return (x, y)

    def reset(self) -> None:
        self.body = 3
        self.score = 0
        self.game_over = False

        self.draw_food()

        self.snake = [self.generate_xy() for i in range(self.body)]
        self.draw_snake()
        self.score_text()

    def draw_food(self) -> None:
        self.food = self.generate_xy()

        ### Avoid food in snake
        if self.food in self.snake:
            self.food = self.generate_xy()

    def draw_snake(self):
        for part in self.snake:
            pygame.draw.rect(self.screen, Color.yellow, [part[0], part[1],
                                                         self.object_size, self.object_size])

    def score_text(self):
        message = self.score_font.render(f'Score: {self.score}', True, Color.black)
        self.screen.blit(message, [5, 5])

    def play_game(self):
        pass
