import warnings
import pygame
from pygame.locals import *


class Main():

    pygame.init()

    def __init__(self):
        x_acc_booster = 0.04
        y_acc_booster = 0.01

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
        box1 = Box(box1_initial_x, box1_initial_y, box1_size, box1_color, window_width, window_height)

        box2_initial_x = window_width-1
        box2_initial_y = 5
        box2_size = (30, 30)
        box2_color = (0, 0, 250)
        box2 = Box(box2_initial_x, box2_initial_y, box2_size, box2_color, window_width, window_height)

        box3 = Box(window_width-1, window_height-1, (40,40), (100,100,30), window_width, window_height)

        x_velocity = 0.2
        y_velocity = 0.1

        done = False
        key_held = False
        while not done:
            surface.fill(background_color)

            box1.update(x_velocity, y_velocity)
            box2.update(x_velocity, y_velocity)
            box3.update(x_velocity, y_velocity)

            box1.draw(surface)
            box2.draw(surface)
            box3.draw(surface)

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

                        # Instead of letting acceleration go negative
                        # in the y-direction, force it to be zero
                        if y_velocity < 0.000:
                            y_velocity = 0.000
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


class Box:

    def __init__(self, x, y, size, obj_color, window_width, window_height):
        self.x = x
        self.y = y
        self.size = size
        self.obj_color = obj_color
        self.window_width = window_width
        self.window_height = window_height
        self.x_orientation = 1
        self.y_orientation = 1

    def draw(self, surface):
        ball = pygame.image.load("src/images/black_ball.png")
        ball_rect = ball.get_rect()
        surface.blit(ball, [self.x, self.y])

        # box = pygame.Rect((self.x, self.y), self.size)
        # pygame.draw.ellipse(surface, self.obj_color, box)

    def update(self, x_velocity, y_velocity):
        self.x += x_velocity * self.x_orientation
        self.y += y_velocity * self.y_orientation
        if self.x >= self.window_width:
            self.x_orientation = -1
        elif self.x <= 0:
            self.x_orientation = 1
        if self.y >= self.window_height:
            self.y_orientation = -1
        elif self.y <= 0:
            self.y_orientation = 1

Main()