
import pygame
from pygame.locals import *

x_orientation = 1
y_orientation = 1

x_max_velocity = 3
y_max_velocity = 1.5

class Main():

    pygame.init()

    def __init__(self):
        x_acc_booster = 0.003
        y_acc_booster = 0.001

        background_color = (0, 0, 0)
        window_height = 400
        window_width = 800
        screensize = (window_width, window_height)
        surface = pygame.display.set_mode(screensize)

        # Making the boxes
        box1_initial_x = 5
        box1_initial_y = 5
        box1_size = (20, 20)
        box1_color = (250, 0, 0)
        box1 = Ball(box1_initial_x, box1_initial_y, box1_size, box1_color, window_width, window_height)

        x_velocity = 0.2
        y_velocity = 0.1

        done = False
        key_held = False
        while not done:
            surface.fill(background_color)

            box1.update(x_velocity, y_velocity)
            # box2.update(x_velocity, y_velocity)
            # box3.update(x_velocity, y_velocity)

            box1.draw(surface)
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
            #     x_velocity = 0.04




class Ball:

    def __init__(self, x, y, size, obj_color, window_width, window_height):
        self.x = x
        self.y = y
        self.size = size
        self.obj_color = obj_color
        self.window_width = window_width
        self.window_height = window_height

    def draw(self, surface):
        ball = pygame.image.load("../images/black_ball.png")
        ball_rect = ball.get_rect()
        surface.blit(ball, [self.x, self.y])

        # box = pygame.Rect((self.x, self.y), self.size)
        # pygame.draw.ellipse(surface, self.obj_color, box)

    def update(self, x_velocity, y_velocity):
        global x_orientation
        global y_orientation

        self.x += x_velocity * x_orientation
        self.y += y_velocity * y_orientation
        if self.x >= self.window_width:
            x_orientation = -1
        elif self.x <= 0:
            x_orientation = 1
        if self.y >= self.window_height:
            y_orientation = -1
        elif self.y <= 0:
            y_orientation = 1

Main()