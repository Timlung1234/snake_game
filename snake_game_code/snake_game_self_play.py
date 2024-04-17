import pygame
import random

class Color:
    yellow = (255, 255, 102)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

class Snake:
    def __init__(self):
        ### Get window width & height
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        ### Snake block size
        self.snake_block = 20
        
        ### Snake generate xy
        self.x = round(random.randint(0, self.screen_width) / self.snake_block) * self.snake_block
        self.y = round(random.randint(0, self.screen_height) / self.snake_block) * self.snake_block

        self.screen = pygame.display.get_surface()
    
    def draw_snake(self, body):
        for part in body:
            pygame.draw.rect(self.screen, Color.yellow, [part[0], part[1],
                                                          self.snake_block, self.snake_block])

class Food:
    def __init__(self):
        ### Get window width & height
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.screen = pygame.display.get_surface()

        ### Food block size
        self.food_block = 20
    
    def init_food(self):
        ### Set up food
        self.food_x = round(random.randint(0, self.screen_width-self.food_block) / self.food_block) * self.food_block
        self.food_y = round(random.randint(0, self.screen_height-self.food_block) / self.food_block) * self.food_block

        return self.food_x, self.food_y
    
    def draw_food(self, curr_x, curr_y):
        pygame.draw.rect(self.screen, Color.red, [curr_x, curr_y,
                                              self.food_block, self.food_block])

class Game:
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
        self.score = 0

        self.game_over = False

    def score_text(self):
        message = self.scorefont.render(f'Score: {self.score}', True, Color.black)
        self.screen.blit(message, [5, 5])

    def main(self):
        snake = Snake()
        food = Food()

        food_x, food_y = food.init_food()

        ### Set up timer
        clock = pygame.time.Clock()

        curr_snake_x, curr_snake_y = snake.x, snake.y

        snake_length = 3
        
        ### Initial direction step
        x_change, y_change = 0, 0
        
        self.snake_body = [(curr_snake_x, curr_snake_y + i) \
                            for i in range(0, snake.snake_block * snake_length, snake.snake_block)]
        
        print(self.snake_body)

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
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and y_change <= 0:
                        y_change = -snake.snake_block
                        x_change = 0

                    ### Down
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y_change >= 0:
                        y_change = snake.snake_block
                        x_change = 0

                    ### Right
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x_change >= 0:
                        y_change = 0
                        x_change = snake.snake_block
                    
                    ### Left
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x_change <= 0:
                        y_change = 0
                        x_change = -snake.snake_block

            ### Get snake next location
            curr_snake_x += x_change
            curr_snake_y += y_change

            ### Draw background & snake & food
            self.screen.fill(Color.blue)

            if x_change != 0 or y_change != 0:
                self.snake_body.pop()
                self.snake_body.insert(0, (curr_snake_x, curr_snake_y))

            if curr_snake_x == food_x and curr_snake_y == food_y:
                self.score += 1
                self.score_text()
                
                new_x, new_y = self.snake_body[-1]
                self.snake_body.append((new_x + x_change, new_y + y_change))
                snake.draw_snake(self.snake_body)
                food_x, food_y = food.init_food()
                food.draw_food(food_x, food_y)

            else:
                self.score_text()
                snake.draw_snake(self.snake_body)
                food.draw_food(food_x, food_y)

            if self.snake_body[0] in self.snake_body[1:]:
                self.game_over = True

            if curr_snake_x < 0 or curr_snake_x >= self.screen_width or\
                curr_snake_y < 0 or curr_snake_y >= self.screen_height:
                self.game_over = True

            ### Update all
            pygame.display.update()

            ### Control while loop speed
            clock.tick(self.snake_speed)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()
