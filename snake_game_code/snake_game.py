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
        self.screen_width = 400
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

        ### Title of window
        pygame.display.set_caption('Game')
        
        ### Font style
        self.scorefont = pygame.font.SysFont("comicsansms", 35)

        ### Game status & setting
        self.snake_speed = 50
        self.object_size = 20

        self.reset()

        self.clock = pygame.time.Clock()

    def generate_food(self) -> tuple:
        food_xy = self.generate_xy()

        while food_xy in self.snake:
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

        self.pre_snake = None
        self.new_snake = None

    def generate_xy(self) -> tuple:
        x = round(random.randint(0, self.screen_width - self.object_size) / self.object_size) * self.object_size
        y = round(random.randint(0, self.screen_height - self.object_size) / self.object_size) * self.object_size

        return (x, y)

    def refresh_gui(self) -> None:
        ### Draw background
        self.screen.fill(Color.blue)

        ### Draw snake
        pygame.draw.rect(self.screen, Color.green, [self.snake[0][0], self.snake[0][1],
                                                    self.object_size, self.object_size])
        for part in self.snake[1:]:
            pygame.draw.rect(self.screen, Color.yellow, [part[0], part[1],
                                                         self.object_size, self.object_size])
        
        ### Draw food
        pygame.draw.rect(self.screen, Color.red, [self.food[0], self.food[1],
                                                  self.object_size, self.object_size])
        
        message = self.scorefont.render(f'Score: {self.score}', True, Color.black)
        self.screen.blit(message, [5, 5])

        self.crash_path()

        ### Update
        pygame.display.update()

        ### Control while loop speed
        self.clock.tick(self.snake_speed)

    def crash(self, direction=None):
        if direction is None:
            direction = self.snake[0]

        ### Crash itself
        if direction in self.snake[1:]:
            return True
        
        ### Crash the wall
        if direction[0] < 0 or direction[0] >= self.screen_width or\
            direction[1] < 0 or direction[1] >= self.screen_height:
            return True

        return False

    def crash_path(self):
        head = self.snake[0]

        #pygame.draw.line(self.screen, Color.green, head, (head[0], 0))
        #pygame.draw.line(self.screen, Color.green, head, (0, head[1]))
        #pygame.draw.line(self.screen, Color.green, head, (self.screen_width, head[1]))
        #pygame.display.flip()
        pass

    def body_check(self, action):
        x, y = self.snake[0]

        if action == 'up':
            direction = [1, 0, 0, 0]
        elif action == 'down':
            direction = [0, 1, 0, 0]
        elif action == 'right':
            direction = [0, 0, 1, 0]
        elif action == 'left':
            direction = [0, 0, 0, 1]

        ### Up
        if direction == [1, 0, 0, 0]:
            dis = y
            while dis > 0:
                dis -= self.object_size
                if (x, dis) in self.snake[1:]:
                    return True
        ### Down
        elif direction == [0, 1, 0, 0]:
            dis = y
            while dis < self.screen_height:
                dis += self.object_size
                if (x, dis) in self.snake[1:]:
                    return True
        ### Right
        elif direction == [0, 0, 1, 0]:
            dis = x
            while dis < self.screen_width:
                dis += self.object_size
                if (dis, y) in self.snake[1:]:
                    return True
        ### Left
        elif direction == [0, 0, 0, 1]:
            dis = x
            while dis > 0:
                dis -= self.object_size
                if (dis, y) in self.snake[1:]:
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

            # ### Press 'ESC' to close
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self.game_over = True
            #         pygame.quit()
            #         quit()

        ### Up
        if action == [1, 0, 0, 0] and self.y_change <= 0:#and self.y_change <= 0: or event.key == pygame.K_UP:
            self.y_change = -self.object_size
            self.x_change = 0

        ### Down
        elif action == [0, 1, 0, 0] and self.y_change >= 0:#and self.y_change >= 0: or event.key == pygame.K_DOWN:
            self.y_change = self.object_size
            self.x_change = 0

        ### Right
        elif action == [0, 0, 1, 0] and self.x_change >= 0:#and self.x_change >= 0: or event.key == pygame.K_RIGHT:
            self.y_change = 0
            self.x_change = self.object_size
        
        ### Left
        elif action == [0, 0, 0, 1] and self.x_change <= 0:#and self.x_change <= 0: or event.key == pygame.K_LEFT:
            self.y_change = 0
            self.x_change = -self.object_size

        ### Previous snake head coordinate
        self.pre_snake = self.snake[0]

        ### Get snake next location
        new_x = self.snake[0][0] + self.x_change
        new_y = self.snake[0][1] + self.y_change

        ### Updated snake head coordinate
        self.new_snake = new_x, new_y

        self.reward = 0

        ### Update snake coordinate list
        if self.x_change != 0 or self.y_change != 0:
            self.snake.pop()
            self.snake.insert(0, (new_x, new_y))
            self.walk_step += 1
        
        ### When Updated snake head eat the food
        if (new_x, new_y) == self.food:
            ### Increase the reward by the length of snake
            self.reward += 10 + (len(self.snake)*0.5)

            self.score += 1

            self.walk_step = 0

            self.snake_length += 1

            tail_x, tail_y = self.snake[-1]

            self.snake.append((tail_x + self.x_change * -1,
                               tail_y + self.y_change * -1))
            
            self.food = self.generate_food()

        ### Update the whole window
        self.refresh_gui()

        pre_dist = ((self.pre_snake[0] - self.food[0])**2 + (self.pre_snake[1] - self.food[1])**2)**(1/2)
        new_dist = ((self.new_snake[0] - self.food[0])**2 + (self.new_snake[1] - self.food[1])**2)**(1/2)

        if new_dist < pre_dist:
            self.reward += (1 / len(self.snake))
        else:
            self.reward -= (1 / len(self.snake))
        
        if self.crash() or self.walk_step > (100 + len(self.snake) * 5.5):
            self.game_over = True
            self.reward -= 20
            return self.reward, self.game_over, self.score
        elif self.crash() == False:
            self.reward += 1 + len(self.snake) * 2.2
        
        return self.reward, self.game_over, self.score

#if __name__ == '__main__':
#    game = Snake_game()
#    game.play_game()