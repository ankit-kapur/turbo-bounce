__author__ = 'ankitkap'

import math
import random
import pygame
from pygame.locals import *
import Utils
from Interactable import Interactable

# No. of walls, coins, and holes
num_of_walls = 7
num_of_collectibles = 8
num_of_holes = 5

# Range of wall lengths
min_wall_length = 50
max_wall_length = 100

# Play area
distance_from_top = 120
play_area_size = 400

# Boundary wall padding
boundary_wall_padding = 20

# Window dimensions
window_width = 800
window_height = 600

x_max_velocity = 5.0
y_max_velocity = 5.0

# Rate by which a key press moves a ball
x_acc_booster = 0.022
y_acc_booster = 0.018

# Colors
wall_color = pygame.Color('darkblue')
# Background color
background_color = pygame.Color('black')

# Spacing in between walls, collectibles and black holes
gap_between_interactables = 40

key_held = None
interactables = []

TOP = 1
BOTTOM = 2
LEFT = 3
RIGHT = 4


class Main():
    def __init__(self):

        # Initialize stuff
        global interactables
        interactables = []

        pygame.init()
        global key_held

        clock = pygame.time.Clock()

        # List to hold all the sprites
        self.all_sprite_list = pygame.sprite.Group()
        # List of walls. (x_pos, y_pos, width, height)
        self.wall_list = pygame.sprite.Group()
        # Collectibles
        self.collectible_list = pygame.sprite.Group()

        screensize = (window_width, window_height)
        self.surface = pygame.display.set_mode(screensize)
        pygame.display.set_caption("Turbo bounce")

        # ----- Making the WALLS
        self.make_the_walls()

        # ---- Making the balls
        ball1_initial_x = 50
        ball1_initial_y = window_height - 100
        # Initial velocities
        initial_x_velocity = 0.2
        initial_y_velocity = 0.1
        self.ball1 = Ball(ball1_initial_x, ball1_initial_y, initial_x_velocity, initial_y_velocity, self.wall_list)
        self.all_sprite_list.add(self.ball1)

        # ----- Making the collectibles
        self.make_the_collectibles()


        quit_game = False
        key_held = []
        while not quit_game:

            self.surface.fill(background_color)

            self.all_sprite_list.update()

            # Check for collisions
            self.check_for_collisions()

            self.all_sprite_list.draw(self.surface)

            # ----- Text banners
            self.show_text_banners()

            # FPS
            clock.tick(170)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # ----------- Event handlers ------------- #
            events = pygame.event.get()
            for e in events:
                if e.type is KEYUP:
                    if e.key == pygame.K_UP:
                        key_held.remove("UP")
                    elif e.key == pygame.K_DOWN:
                        key_held.remove("DOWN")
                    elif e.key == pygame.K_LEFT:
                        key_held.remove("LEFT")
                    elif e.key == pygame.K_RIGHT:
                        key_held.remove("RIGHT")
                if e.type is KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        quit_game = True
                    elif e.key == pygame.K_UP:
                        key_held.append("UP")
                    elif e.key == pygame.K_DOWN:
                        key_held.append("DOWN")
                    elif e.key == pygame.K_LEFT:
                        key_held.append("LEFT")
                    elif e.key == pygame.K_RIGHT:
                        key_held.append("RIGHT")

                if e.type is QUIT:
                    # To quit when the close button is clicked
                    quit_game = True

    def make_the_collectibles(self):
        global interactables

        # --- Random collectibles
        for i in range(1, num_of_collectibles):
            # While the wall generated is valid (not overlapping with anything else)
            is_invalid_collectible = True
            while is_invalid_collectible:
                # Random length
                wall_length = 20
                wall_height = 20

                # Random x and y coords
                wall_x_coord = random.randint(boundary_wall_padding + 50,
                                              window_width - (boundary_wall_padding * 2) - 30 - wall_length)
                wall_y_coord = random.randint(distance_from_top + 50, play_area_size)

                # Check if this wall is valid
                is_invalid_collectible = Utils.is_overlapping(wall_x_coord, wall_y_coord, wall_height, wall_length,
                                                              interactables, gap_between_interactables)

                # Make the collectible
                if not is_invalid_collectible:
                    collectible = Collectible(wall_x_coord, wall_y_coord)
                    self.collectible_list.add(collectible)
                    self.all_sprite_list.add(collectible)
                    # self.make_horiz_wall(wall_x_coord, wall_y_coord, wall_height, wall_length)

                    # Add wall data to list
                    the_collectible = Interactable(wall_x_coord, wall_y_coord, wall_height, wall_length)
                    interactables.append(the_collectible)

    def make_the_walls(self):
        global interactables

        # --- Boundaries
        # Format: x, y, height, width
        self.make_horiz_wall(boundary_wall_padding / 2, distance_from_top, 10,
                             window_width - (boundary_wall_padding * 2))
        self.make_horiz_wall(boundary_wall_padding / 2, window_height - (boundary_wall_padding * 1.5), 10,
                             window_width - (boundary_wall_padding))
        self.make_vertical_wall(boundary_wall_padding / 2, distance_from_top,
                                window_height - (boundary_wall_padding * 1.5) - distance_from_top, 10)
        self.make_vertical_wall(window_width - (boundary_wall_padding * 2.5) + boundary_wall_padding, distance_from_top,
                                window_height - (boundary_wall_padding * 1.5) - distance_from_top, 10)

        # --- Random walls
        for i in range(1, num_of_walls):
            # While the wall generated is valid (not overlapping with anything else)
            is_invalid_wall = True
            while is_invalid_wall:
                # Random length
                wall_length = random.randint(min_wall_length, max_wall_length)
                wall_height = 10

                # Random x and y coords
                wall_x_coord = random.randint(boundary_wall_padding + 50,
                                              window_width - (boundary_wall_padding * 2) - 30 - wall_length)
                wall_y_coord = random.randint(distance_from_top + 50, play_area_size)

                # Check if this wall is valid
                is_invalid_wall = Utils.is_overlapping(wall_x_coord, wall_y_coord, wall_height, wall_length,
                                                       interactables, gap_between_interactables)

                # Make the wall
                if not is_invalid_wall:
                    self.make_horiz_wall(wall_x_coord, wall_y_coord, wall_height, wall_length)

                    # Add wall data to list
                    the_wall = Interactable(wall_x_coord, wall_y_coord, wall_height, wall_length)
                    interactables.append(the_wall)

    def make_horiz_wall(self, x, y, height, width):
        for x_coord in Utils.frange(x, x + width, 20.0):
            wall = Wall(x_coord, y)
            self.wall_list.add(wall)
            self.all_sprite_list.add(wall)

    def make_vertical_wall(self, x, y, height, width):
        for y_coord in Utils.frange(y, y + height, 20.0):
            wall = Wall(x, y_coord)
            self.wall_list.add(wall)
            self.all_sprite_list.add(wall)

    def show_text_banners(self):
        self.show_text("TURBO BOUNCE", 28, pygame.Color('darkred'), None, 10, True)
        self.show_text("Created by Ankit Kapur", 14, pygame.Color('gray36'), None, 50, True)

        # Ball information
        info_xpos = 620
        info_ypos = 150
        x_vel = "x-veloc: %.3f" % self.ball1.x_velocity
        x_ori = "x-orien: %.3f" % self.ball1.x_orientation
        y_vel = "y-veloc: %.3f" % self.ball1.y_velocity
        y_ori = "y-orien: %.3f" % self.ball1.y_orientation

        self.show_text(x_vel, 14, pygame.Color('gray45'), info_xpos, info_ypos, False)
        self.show_text(x_ori, 14, pygame.Color('gray45'), info_xpos, info_ypos + 23, False)
        self.show_text(y_vel, 14, pygame.Color('gray45'), info_xpos, info_ypos + 23 + 33, False)
        self.show_text(y_ori, 14, pygame.Color('gray45'), info_xpos, info_ypos + 23 + 33 + 23, False)

        # Scores
        score_x_location = 670
        score_y_location = 15
        self.show_text("Player 1: %d" % self.ball1.score, 16, pygame.Color('darkblue'), score_x_location, score_y_location, False)
        self.show_text("Player 2: 0", 16, pygame.Color('darkred'), score_x_location, score_y_location + 23, False)

    def show_text(self, text, font_size, font_color, x, y, is_centered):
        font = pygame.font.Font("../fonts/minecraft.ttf", font_size)

        # Render text
        text_surf = font.render(text, 1, font_color)

        if is_centered:
            textpos = text_surf.get_rect()
            textpos.centerx = self.surface.get_rect().centerx
            textpos.y = y
        else:
            textpos = (x, y)

        # Blit it
        self.surface.blit(text_surf, textpos)

    def check_for_collisions(self):

        # Any collectibles collected?
        for collec in self.collectible_list:
            if Utils.do_rects_intersect(self.ball1.rect.x, self.ball1.rect.y, self.ball1.rect.h, self.ball1.rect.w, collec.rect.x, collec.rect.y, collec.rect.h, collec.rect.w):
                # Increase the score
                self.ball1.score += 1
                # Delete the collectible
                self.collectible_list.remove(collec)
                self.all_sprite_list.remove(collec)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, initial_x_velocity, initial_y_velocity, wall_list):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Score is initially zero
        self.score = 0

        # Load the image
        self.image = pygame.image.load("../images/doge.png")
        self.image = pygame.transform.scale(self.image, (45, 35)).convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.x_velocity = initial_x_velocity
        self.y_velocity = initial_y_velocity

        self.x_orientation = 1
        self.y_orientation = -1

        self.wall_list = wall_list

        # def draw(self, self.surface):

        # ball = pygame.image.load("../images/black_ball.png")
        # ball_rect = ball.get_rect()
        # self.surface.blit(ball, [self.rect.x, self.rect.y])

    def deal_with_event(self):
        global key_held

        # While the key is held
        if key_held is not None:
            if "UP" in key_held:
                self.y_velocity += y_acc_booster
            if "DOWN" in key_held:
                self.y_velocity -= y_acc_booster
            if "LEFT" in key_held:
                self.x_velocity -= x_acc_booster
            if "RIGHT" in key_held:
                self.x_velocity += x_acc_booster

        # Instead of letting acceleration go negative
        # in the y-direction, force it to be zero
        if self.y_velocity < 0.000:
            # self.y_velocity = math.fabs(self.y_velocity)
            self.y_velocity = 0.000
            # self.y_orientation = -1
        elif self.y_velocity > y_max_velocity:
            self.y_velocity = y_max_velocity
            # if x_velocity < 0.000:
            # x_velocity = 0.04

        if self.x_velocity < 0.000:
            self.x_velocity = 0.000
            if "LEFT" in key_held:
                self.x_orientation = -1
            elif "RIGHT" in key_held:
                self.x_orientation = 1

        elif self.x_velocity > x_max_velocity:
            self.x_velocity = x_max_velocity

    def update(self):

        self.deal_with_event()

        # Move in x direction
        self.rect.x += round(self.x_velocity * self.x_orientation)

        # Did we collide against a wall after moving in the x-direction?
        for wall in self.wall_list:
            if self.rect.colliderect(wall):
                self.x_orientation *= -1
                self.rect.x += round(self.x_velocity * self.x_orientation)
                break

        self.rect.y += round(self.y_velocity * self.y_orientation)

        # Did we collide against a wall after moving in the x-direction?
        for wall in self.wall_list:
            if self.rect.colliderect(wall):
                self.y_orientation *= -1
                self.rect.y += round(self.y_velocity * self.y_orientation)
                break


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.image = pygame.image.load("../images/wall1.png").convert()

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Random cookie
        cookie_number = random.randint(1,7)

        # Load the image
        self.image = pygame.image.load("../images/cookies/cookie-%d.png" % cookie_number).convert()
        self.image = pygame.transform.scale(self.image, (35, 29))

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


# class New_game_button:
#     def __init__(self, text):


Main()