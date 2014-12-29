import pygame
from pygame.locals import *

# Window dimensions
window_height = 400
window_width = 800

x_max_velocity = 3
y_max_velocity = 1.5

# Rate by which a key press moves a ball
x_acc_booster = 0.003
y_acc_booster = 0.001

x_orientation = 1
y_orientation = 1

class Main():
    pygame.init()

    def __init__(self):

        # List to hold all the sprites
        all_sprite_list = pygame.sprite.Group()

        # Make the walls. (x_pos, y_pos, width, height)
        wall_list = pygame.sprite.Group()

        background_color = (0, 0, 0)
        screensize = (window_width, window_height)
        surface = pygame.display.set_mode(screensize)

        # Making the balls
        ball1_initial_x = 5
        ball1_initial_y = 5
        ball1_size = (20, 20)
        ball1_color = (250, 0, 0)
        ball1 = Ball(ball1_initial_x, ball1_initial_y, ball1_size, ball1_color)
        all_sprite_list.add(ball1)

        x_velocity = 0.2
        y_velocity = 0.1

        done = False
        key_held = False
        while not done:
            surface.fill(background_color)

            all_sprite_list.update(x_velocity, y_velocity)
            # box2.update(x_velocity, y_velocity)
            # box3.update(x_velocity, y_velocity)

            all_sprite_list.draw(surface)
            # box2.draw(surface)
            # box3.draw(surface)

            pygame.display.flip()

            # To quit when the close button is clicked
            events = pygame.event.get()
            for e in events:
                if e.type is KEYUP:
                    key_held = None
                if e.type is KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        done = True
                    elif e.key == pygame.K_UP:
                        key_held = "UP"
                    elif e.key == pygame.K_DOWN:
                        key_held = "DOWN"
                    elif e.key == pygame.K_LEFT:
                        key_held = "LEFT"
                    elif e.key == pygame.K_RIGHT:
                        key_held = "RIGHT"

                if e.type is QUIT:
                    done = True

            # While the key is held
            if key_held != None:
                if key_held == "UP":
                    y_velocity += y_acc_booster
                elif key_held == "DOWN":
                    y_velocity -= y_acc_booster
                elif key_held == "LEFT":
                    x_velocity -= x_acc_booster
                elif key_held == "RIGHT":
                    x_velocity += x_acc_booster

                    # Instead of letting acceleration go negative
                    # in the y-direction, force it to be zero
            if y_velocity < 0.000:
                y_velocity = 0.1
            elif y_velocity > y_max_velocity:
                y_velocity = y_max_velocity
                # if x_velocity < 0.000:
                # x_velocity = 0.04


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite().__init__()

        # Load the image
        self.image = pygame.image.load("../images/black_ball.png").convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def draw(self, surface):

        # ball = pygame.image.load("../images/black_ball.png")
        # ball_rect = ball.get_rect()
        # surface.blit(ball, [self.rect.x, self.rect.y])


    def update(self, x_velocity, y_velocity):
        global x_orientation
        global y_orientation

        self.rect.x += x_velocity * x_orientation
        self.rect.y += y_velocity * y_orientation
        if self.rect.x >= self.window_width:
            x_orientation = -1
        elif self.rect.x <= 0:
            x_orientation = 1
        if self.rect.y >= self.window_height:
            y_orientation = -1
        elif self.rect.y <= 0:
            y_orientation = 1


class Wall:
    def __init__(self, x, y, height, width, obj_color):
        self.rect.x = x
        self.rect.y = y
        self.size = [height, width]
        self.obj_color = obj_color

    def draw(self, surface):
        wall = pygame.Rect((self.rect.x, self.rect.y), self.size)
        pygame.draw.ellipse(surface, self.obj_color, wall)


Main()