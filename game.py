import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y) )
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24)*SIZE
        self.y = random.randint(1, 14)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.length = 1
        self.parent_screen = parent_screen
        # load img
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [40]
        self.y = [40]
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]) )
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


class button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Snake and Apple")
        pygame.mixer.init()
        self.play_background_music()
        # Draw surface
        self.surface = pygame.display.set_mode((1000, 600))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()



    def is_collision(self, x1, y1, x2, y2):
        if (x1 >= x2) and (x1 < x2 + SIZE):
            if (y1 >= y2) and (y1 < y2 + SIZE):
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (200, 200, 200) )
        self.surface.blit(score, (850, 10))

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0) )

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 600):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Score: {self.snake.length}", True, (200, 200, 200) )
        self.surface.blit(line1, (350, 200))
        line2 = font.render("To play again hit ENTER", True, (255, 255, 255) )
        self.surface.blit(line2, (350, 250))
        line3 = font.render("To exit press ESCAPE", True, (255, 255, 255))
        self.surface.blit(line3, (350, 300))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if self.snake.direction == 'down' or self.snake.direction == 'up':
                            if event.key == K_LEFT:
                                self.snake.move_left()
                            if event.key == K_RIGHT:
                                self.snake.move_right()
                        if self.snake.direction == 'left' or self.snake.direction == 'right':
                            if event.key == K_UP:
                                self.snake.move_up()
                            if event.key == K_DOWN:
                                self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.1)

    def startgame(self):
        run = True
        start_button = button((0, 255, 0), 160, 225, 250, 100, "Start")
        exit_button = button((0, 255, 0), 640, 225, 250, 100, "Exit")

        while run:
            bg = pygame.image.load("resources/background.jpg")
            win = pygame.display.set_mode((1000, 600))
            win.blit(bg, (0, 0))
            start_button.draw(win, (0, 0, 0))
            exit_button.draw(win, (0, 0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isOver(pos):
                        game.run()
                    elif exit_button.isOver(pos):
                        print("See you soon...")
                        quit()

                if event.type == pygame.MOUSEMOTION:
                    if start_button.isOver(pos):
                        start_button.color = (255, 0, 0)
                    elif exit_button.isOver(pos):
                        exit_button.color = (255, 0, 0)
                    else:
                        start_button.color = (0, 255, 0)
                        exit_button.color = (0, 255, 0)

if __name__ == "__main__":
    game = Game()
    game.startgame()
