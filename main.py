from pygame.locals import *
import pygame
import time
import random

pygame.init()
pygame.mixer.init()

SIZE = 40
X_NO = 24
Y_NO = 16
WIDTH = SIZE * X_NO
HEIGHT = SIZE * Y_NO


# SCREEN width X height = 800 X 600

# Ctrl + Alt + l


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.head = pygame.image.load("files/shead.png")
        self.block = pygame.image.load("files/square2.png")
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.head = pygame.transform.scale(self.head, (SIZE, SIZE))
        self.x = [120] * self.length
        self.y = [120] * self.length
        self.direction = 'down'
        self.slow = 0.2  # describes the speed of snake

        self.current_head = self.head  # used for changing direction of head

    # makes head orientation correct
    def update_head_angle(self):
        self.current_head = self.head

        if self.direction == 'left':
            self.current_head = pygame.transform.rotate(self.current_head, -90)

        if self.direction == 'right':
            self.current_head = pygame.transform.rotate(self.current_head, 90)

        if self.direction == 'up':
            self.current_head = pygame.transform.rotate(self.current_head, 180)

        if self.direction == 'down':
            pass

    # increase length of length when it eat an apple
    def increase_length(self):
        self.length = self.length + 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        # head image is special
        self.parent_screen.blit(self.current_head, (self.x[0], self.y[0]))

        # rest of the body will use same block image
        for i in range(1, self.length, 1):  # [0,1,2,3,4]
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

    def walk(self):

        for i in range(self.length - 1, 0, -1):  # i = [9,4,3,2,1]
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] = self.x[0] - SIZE

        if self.direction == 'right':
            self.x[0] = self.x[0] + SIZE

        if self.direction == 'up':
            self.y[0] = self.y[0] - SIZE

        if self.direction == 'down':
            self.y[0] = self.y[0] + SIZE

        self.draw()

    def move_left(self):
        self.direction = 'left'
        self.update_head_angle()

    def move_right(self):
        self.direction = 'right'
        self.update_head_angle()

    def move_up(self):
        self.direction = 'up'
        self.update_head_angle()

    def move_down(self):
        self.direction = 'down'
        self.update_head_angle()


class Apple:
    def __init__(self, screen):
        self.image = pygame.image.load("files/apple.png")
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.parent_screen = screen
        self.x = 40 * random.randint(1, X_NO - 2)
        self.y = 40 * random.randint(1, Y_NO - 2)
        self.background = pygame.image.load("files/grass.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self):
        self.parent_screen.blit(self.background, (0, 0))
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = 40 * random.randint(1, X_NO - 2)
        self.y = 40 * random.randint(1, Y_NO - 2)
        pygame.display.flip()


#  x = 0 to 1000   and y = 0 to 600

class Game:
    def __init__(self):

        pygame.mixer.music.load("files/SnakeBackground.mp3")
        pygame.mixer.music.play(-1)

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))  # 800x600 width x height

        self.dead_bg = pygame.image.load("files/dead_snake.png")
        self.dead_bg = pygame.transform.scale(self.dead_bg, (WIDTH, HEIGHT))

        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

        self.pause = False

    def collide_boundary(self):
        if self.snake.x[0] < 0 or self.snake.y[0] < 0 or self.snake.x[0] > X_NO * SIZE - 2 or \
                self.snake.y[0] > Y_NO * SIZE - 2:
            return True

    def reset(self):
        pygame.mixer.music.play(-1)

        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.pause = False

    def show_game_over(self):
        pygame.mixer.music.pause()

        sound2 = pygame.mixer.Sound("files/snakeEnd.mp3")
        sound2.play()

        self.surface.blit(self.dead_bg, (0, 0))

        font = pygame.font.SysFont('arial', 50)
        text_box1 = font.render(f" Game Over. Your Score was {self.snake.length - 3}", True, (189, 29, 8))
        self.surface.blit(text_box1, (50, 50))

        font2 = pygame.font.SysFont('arial', 28)
        text_box2 = font2.render(f" Press ESCAPE to Quit.           Press Enter to Restart", True, (0, 0, 0))
        self.surface.blit(text_box2, (50, 550))
        pygame.display.flip()
        # 1st => Option for Game Quit
        # 2nd => Reset Game (Score = 0)

    def play(self):

        self.apple.draw()
        self.snake.walk()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("files/grab.mp3")
            sound.play()

            self.apple.move()
            self.snake.increase_length()
            # updating speed of snake according to
            self.snake.slow -= 0.002

        for i in range(1, self.snake.length, 1):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "GameOver"

        if self.collide_boundary():
            raise "GameOver"



    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length - 3}", True, (255, 255, 255))
        self.surface.blit(score, (650, 10))
        pygame.display.flip()

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True

        return False

    def run(self):  # contain game code

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        self.reset()

            try:
                if not self.pause:  # if (pause == False): => if not pause:
                    self.play()  # if (pause == True):  => if pause:

            except Exception:
                self.show_game_over()
                self.pause = True

            time.sleep(self.snake.slow)


if __name__ == '__main__':
    game = Game()
    game.run()
