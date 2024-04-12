import pygame
import random

class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

class Snake:
    def __init__(self):
        ### Get window width & height
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        ### Snake block size
        self.snake_block = 10
        
        ### Snake generate xy
        self.x = round(random.randint(0, self.screen_width) / 10) * 10
        self.y = round(random.randint(0, self.screen_height) / 10) * 10

        self.color = Color()
        self.screen = pygame.display.get_surface()

        self.body = [(self.x, self.y)]
    
    def draw_snake(self):
        for part in self.body:
            pass

    def move_snake(self, curr_x, curr_y):
        pygame.draw.rect(self.screen, self.color.yellow, [curr_x, curr_y,
                                                          self.snake_block, self.snake_block])

class Food:
    def __init__(self):
        self.color = Color()
        self.screen = pygame.display.get_surface()

        ### Food block size
        self.food_block = 10
    
    def draw_food(self, curr_x, curr_y):
        pygame.draw.rect(self.screen, self.color.red, [curr_x, curr_y,
                                              self.food_block, self.food_block])

class Game:
    def __init__(self):

        ### Initialize anything
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
        self.snake_speed = 15
        self.score = 0

        self.game_over = False

    def score_text(self):
        message = self.scorefont.render(f'Your Score: {self.score}', True, self.black)
        self.screen.blit(message, [10, 10])

    def main(self):
        color = Color()
        snake = Snake()
        food = Food()

        ### Set up food
        self.food_x = round(random.randint(0, self.screen_width-food.food_block) / 10) * 10
        self.food_y = round(random.randint(0, self.screen_height-food.food_block) / 10) * 10

        ### Set up timer
        clock = pygame.time.Clock()

        ### Draw background
        self.screen.fill(color.blue)

        ### Draw snake
        curr_snake_x, curr_snake_y = snake.x, snake.y

        ### Initial direction step
        x_change, y_change = 0, 0
        
        ### Holding the game window
        while not self.game_over:

            for event in pygame.event.get():

                ### Close window
                if event.type == pygame.QUIT:
                    self.game_over = True

                ### Press 'ESC' to close
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True

                    ### Up
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        y_change = -snake.snake_block
                        x_change = 0

                    ### Down
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        y_change = snake.snake_block
                        x_change = 0

                    ### Right
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        y_change = 0
                        x_change = snake.snake_block
                    
                    ### Left
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        y_change = 0
                        x_change = -snake.snake_block

            ### Get snake next location
            curr_snake_x += x_change
            curr_snake_y += y_change

            ### Draw background & snake & food
            self.screen.fill(color.blue)
            snake.move_snake(curr_snake_x, curr_snake_y)
            food.draw_food(self.food_x, self.food_y)

            ### Update all
            pygame.display.update()

            ### Control while loop speed
            clock.tick(self.snake_speed)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()