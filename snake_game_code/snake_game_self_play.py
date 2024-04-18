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
    def __init__(self):
        ### Initialize
        pygame.init()

        ### Game window setup
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

        ### Title of window
        pygame.display.set_caption('Game')
        
        ### Font style
        self.scorefont = pygame.font.SysFont("comicsansms", 35)

        ### Game status & setting
        self.snake_speed = 10
        self.object_size = 20

        self.reset()

        self.clock = pygame.time.Clock()

    def generate_food(self) -> tuple:
        food_xy = self.generate_xy()

        if food_xy in self.snake:
            food_xy = self.generate_xy()
        
        return food_xy

    def reset(self) -> None:
        ### Reset all setting
        self.score = 0
        self.snake_length = 3
        self.food = None

        self.walk_step = 0
        self.game_over = False

        self.x_change = 0
        self.y_change = 0

        ### Generate snake xy
        self.snake_head = self.generate_xy()
        self.snake = [(self.snake_head[0], self.snake_head[1] + i) \
                      for i in range(0, self.object_size * self.snake_length, self.object_size)]
        
        self.food = self.generate_food()

        print(self.snake)
        print(self.food)
        print()

    def generate_xy(self) -> tuple:
        x = round(random.randint(0, self.screen_width) / self.object_size) * self.object_size
        y = round(random.randint(0, self.screen_height) / self.object_size) * self.object_size

        return (x, y)

    def refresh_gui(self) -> None:
        ### Draw background
        self.screen.fill(Color.blue)

        ### Draw snake
        for part in self.snake:
            pygame.draw.rect(self.screen, Color.yellow, [part[0], part[1],
                                                         self.object_size, self.object_size])
        
        ### Draw food
        pygame.draw.rect(self.screen, Color.red, [self.food[0], self.food[1],
                                                  self.object_size, self.object_size])
        
        message = self.scorefont.render(f'Score: {self.score}', True, Color.black)
        self.screen.blit(message, [5, 5])

        ### Update
        pygame.display.update()

        ### Control while loop speed
        self.clock.tick(self.snake_speed)

    def crash(self):
        head_x, head_y = self.snake[0]

        ### Crash itself
        if self.snake[0] in self.snake[1:]:
            return True
        
        ### Crash the wall
        if head_x < 0 or head_x >= self.screen_width or\
            head_y < 0 or head_y >= self.screen_height:
            return True

        return False

    def play_game(self, action=None):
        ### Get info from pygame interface
        for event in pygame.event.get():

            ### Close window
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                quit()

            ### Press 'ESC' to close
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    pygame.quit()
                    quit()

                ### Up
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.y_change <= 0:
                    self.y_change = -self.object_size
                    self.x_change = 0

                ### Down
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.y_change >= 0:
                    self.y_change = self.object_size
                    self.x_change = 0

                ### Right
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) or action == [1, 0, 0] \
                    and self.x_change >= 0:
                    self.y_change = 0
                    self.x_change = self.object_size
                
                ### Left
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.x_change <= 0:
                    self.y_change = 0
                    self.x_change = -self.object_size

        ### Get snake next location
        new_x = self.snake[0][0] + self.x_change
        new_y = self.snake[0][1] + self.y_change

        self.reward = 0

        if self.x_change != 0 or self.y_change != 0:
            self.snake.pop()
            self.snake.insert(0, (new_x, new_y))
            self.walk_step += 1
            print('step: ', self.walk_step)
        
        if (new_x, new_y) == self.food:
            self.reward += 10
            self.score += 1

            self.walk_step = 0

            self.food = self.generate_food()

            self.snake_length += 1

            tail_x, tail_y = self.snake[-1]

            self.snake.append((tail_x + self.x_change * -1,
                               tail_y + self.y_change * -1))
        
        if self.crash() or self.walk_step > 200:
            self.game_over = True
            self.reward -= 10
            return self.reward, self.game_over, self.score

        self.refresh_gui()

        return self.reward, self.game_over, self.score
    
if __name__ == "__main__":
    
    game = Snake_game()

    while True:
        _, is_game_over, _ = game.play_game()

        if is_game_over:
            game.reset()