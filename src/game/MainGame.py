__author__ = 'ankitkap'

import Crystal_title
import random
import pygame
from pygame.locals import *
import Utils
from Interactable import Interactable

# No. of walls, coins, and asteroids
num_of_walls = 7
num_of_cookies = 8
num_of_asteroids = 9

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

# Player 1
player1_main_color = 'gold'
player1_color = 'gold4'
player1_img = "../images/doge.png"
player1_img_dimensions = (60, 43)

player2_main_color = 'gray62'
player2_color = 'gray28'
player2_img = "../images/pusheen.png"
player2_img_dimensions = (60, 36)

x_max_velocity = 5.0
y_max_velocity = 7.0

# Rate by which a key press moves a player
x_acc_booster = 0.042
y_acc_booster = 0.038

# Background color
background_color = pygame.Color('black')

# Spacing in between walls, cookies and asteroids
gap_between_interactables = 40

key_held = None
interactables = []


class Main():
    def __init__(self):

        # Keeps track of explosion animations
        self.explosion_player1 = None
        self.explosion_player2 = None

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
        # Cookies
        self.cookie_list = pygame.sprite.Group()
        # Asteroids
        self.asteroid_list = pygame.sprite.Group()

        screensize = (window_width, window_height)
        self.surface = pygame.display.set_mode(screensize)
        pygame.display.set_caption("Turbo bounce")

        # ----- Making the WALLS
        self.make_the_walls()

        # ---- Making the players
        # Initial velocities
        initial_x_velocity = 0.4
        initial_y_velocity = 0.4

        # Player 1
        player1_initial_x = 50
        player1_initial_y = window_height - 100
        self.player1 = Player(1, player1_initial_x, player1_initial_y, initial_x_velocity, initial_y_velocity,
                              self.wall_list, player1_img, player1_img_dimensions)
        self.all_sprite_list.add(self.player1)

        # Player 2
        player2_initial_x = window_width - 110
        player2_initial_y = window_height - 91
        # Initial velocities
        self.player2 = Player(2, player2_initial_x, player2_initial_y, initial_x_velocity, initial_y_velocity,
                              self.wall_list, player2_img, player2_img_dimensions)
        self.all_sprite_list.add(self.player2)

        # ----- Making the cookies
        self.make_the_cookies()

        # ----- Making the asteroids
        self.make_the_asteroids()

        # ----- Hearts (representing player's lives
        self.make_hearts()

        quit_game = False
        key_held = []
        while not quit_game:

            self.surface.fill(background_color)
            # background_image = pygame.image.load("../images/background1.png").convert()
            # self.surface.blit(background_image, [0, 0])

            self.all_sprite_list.update()

            # Check for collisions
            self.check_for_collisions()

            self.all_sprite_list.draw(self.surface)

            # Show static text banners
            self.show_static_text_banners()

            # ----- Dynamically changing text banners
            self.show_dynamic_text_banners()

            # FPS
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # ----------- Event handlers ------------- #
            events = pygame.event.get()
            for e in events:
                if e.type is KEYUP:
                    if e.key == pygame.K_UP:
                        key_held.remove("UP")
                    if e.key == pygame.K_DOWN:
                        key_held.remove("DOWN")
                    if e.key == pygame.K_LEFT:
                        key_held.remove("LEFT")
                    if e.key == pygame.K_RIGHT:
                        key_held.remove("RIGHT")

                    if e.key == pygame.K_w:
                        key_held.remove("W")
                    if e.key == pygame.K_a:
                        key_held.remove("A")
                    if e.key == pygame.K_s:
                        key_held.remove("S")
                    if e.key == pygame.K_d:
                        key_held.remove("D")
                if e.type is KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        quit_game = True
                    if e.key == pygame.K_UP:
                        key_held.append("UP")
                    if e.key == pygame.K_DOWN:
                        key_held.append("DOWN")
                    if e.key == pygame.K_LEFT:
                        key_held.append("LEFT")
                    if e.key == pygame.K_RIGHT:
                        key_held.append("RIGHT")

                    if e.key == pygame.K_w:
                        key_held.append("W")
                    if e.key == pygame.K_a:
                        key_held.append("A")
                    if e.key == pygame.K_s:
                        key_held.append("S")
                    if e.key == pygame.K_d:
                        key_held.append("D")

                if e.type is QUIT:
                    # To quit when the close button is clicked
                    quit_game = True

    def make_the_cookies(self):
        global interactables

        # --- Random cookies
        for i in range(1, num_of_cookies):
            # While the wall generated is valid (not overlapping with anything else)
            is_invalid_cookie = True
            while is_invalid_cookie:
                # Random length
                wall_length = 20
                wall_height = 20

                # Random x and y coords
                wall_x_coord = random.randint(boundary_wall_padding + 50,
                                              window_width - (boundary_wall_padding * 2) - 30 - wall_length)
                wall_y_coord = random.randint(distance_from_top + 50, play_area_size)

                # Check if this cookie is valid
                is_invalid_cookie = Utils.is_overlapping(wall_x_coord, wall_y_coord, wall_height, wall_length,
                                                         interactables, gap_between_interactables)

                # Make the cookie
                if not is_invalid_cookie:
                    cookie = Cookie(wall_x_coord, wall_y_coord)
                    self.cookie_list.add(cookie)
                    self.all_sprite_list.add(cookie)
                    # self.make_horiz_wall(wall_x_coord, wall_y_coord, wall_height, wall_length)

                    # Add wall data to list
                    the_cookie = Interactable(wall_x_coord, wall_y_coord, wall_height, wall_length)
                    interactables.append(the_cookie)

    def make_the_asteroids(self):
        global interactables

        # --- Random asteroids
        for i in range(1, num_of_asteroids):
            # While the wall generated is valid (not overlapping with anything else)
            is_invalid_asteroid = True
            while is_invalid_asteroid:
                # Random length
                wall_length = 20
                wall_height = 20

                # Random x and y coords
                wall_x_coord = random.randint(boundary_wall_padding + 50,
                                              window_width - (boundary_wall_padding * 2) - 30 - wall_length)
                wall_y_coord = random.randint(distance_from_top + 50, play_area_size)

                # Check if this cookie is valid
                is_invalid_asteroid = Utils.is_overlapping(wall_x_coord, wall_y_coord, wall_height, wall_length,
                                                           interactables, gap_between_interactables)

                # Make the cookie
                if not is_invalid_asteroid:
                    asteroid = Asteroid(wall_x_coord, wall_y_coord)
                    self.asteroid_list.add(asteroid)
                    self.all_sprite_list.add(asteroid)
                    # self.make_horiz_wall(wall_x_coord, wall_y_coord, wall_height, wall_length)

                    # Add wall data to list
                    the_asteroid = Interactable(wall_x_coord, wall_y_coord, wall_height, wall_length)
                    interactables.append(the_asteroid)

    def make_the_walls(self):
        global interactables
        gap_from_bottom = 25

        # --- Boundaries
        # Format: x, y, height, width
        self.make_horiz_wall(boundary_wall_padding / 2, distance_from_top, 10,
                             window_width - (boundary_wall_padding * 2))
        self.make_horiz_wall(boundary_wall_padding / 2, window_height - (boundary_wall_padding * 1.5) - gap_from_bottom,
                             10,
                             window_width - (boundary_wall_padding))
        self.make_vertical_wall(boundary_wall_padding / 2, distance_from_top,
                                window_height - (boundary_wall_padding * 1.5) - distance_from_top - gap_from_bottom, 10)
        self.make_vertical_wall(window_width - (boundary_wall_padding * 2.5) + boundary_wall_padding, distance_from_top,
                                window_height - (boundary_wall_padding * 1.5) - distance_from_top - gap_from_bottom, 10)

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

    def make_hearts(self):
        # Hearts/lives
        heart_y = 15 + 28 + 28
        gap = 25
        heart_size = 20

        # --- Hearts for player 1
        heart_x = 50 + 60 - 15
        self.heart1_player1 = Heart(heart_x, heart_y, heart_size)
        self.heart2_player1 = Heart(heart_x + gap, heart_y, heart_size)
        self.heart3_player1 = Heart(heart_x + (gap * 2), heart_y, heart_size)
        self.all_sprite_list.add(self.heart1_player1)
        self.all_sprite_list.add(self.heart2_player1)
        self.all_sprite_list.add(self.heart3_player1)

        # --- Hearts for player 2
        heart_x = 660 + 60 - 15
        self.heart1_player2 = Heart(heart_x, heart_y, heart_size)
        self.heart2_player2 = Heart(heart_x + gap, heart_y, heart_size)
        self.heart3_player2 = Heart(heart_x + (gap * 2), heart_y, heart_size)
        self.all_sprite_list.add(self.heart1_player2)
        self.all_sprite_list.add(self.heart2_player2)
        self.all_sprite_list.add(self.heart3_player2)

    def show_static_text_banners(self):
        # Title
        self.show_title_text("TURBO BOUNCE", 28, pygame.Color('dodgerblue2'), None, 10, True)
        self.show_text("Created by Ankit Kapur", 14, pygame.Color('dodgerblue4'), None, 50, True)

        # Instructions
        instruc_y = window_height - 27
        self.show_text("Player 1 - Use WASD to move.", 14, pygame.Color(player1_color), 10, instruc_y, False)
        self.show_text("Player 2 - Use arrow keys to move", 14, pygame.Color(player2_color), 480, instruc_y, False)

    def show_dynamic_text_banners(self):
        # Player 1 information
        score_x_offset = 8
        score_x_location = 50
        score_y_location = 15
        self.show_text("PLAYER 1", 18, pygame.Color(player1_main_color), score_x_location, score_y_location, False)
        self.show_text("Score: %d" % self.player1.score, 16, pygame.Color(player1_color),
                       score_x_location + score_x_offset, score_y_location + 28, False)
        self.show_text("Lives: ", 16, pygame.Color(player1_color), score_x_location - 15, score_y_location + 28 + 28,
                       False)

        # Player 2 information
        score_x_location = 660
        score_y_location = 15
        self.show_text("PLAYER 2", 18, pygame.Color(player2_main_color), score_x_location, score_y_location, False)
        self.show_text("Score: %d" % self.player2.score, 16, pygame.Color(player2_color),
                       score_x_location + score_x_offset, score_y_location + 28, False)
        self.show_text("Lives: ", 16, pygame.Color(player2_color), score_x_location - 15, score_y_location + 28 + 28,
                       False)

        # Debugging information
        # info_xpos = 620
        # info_ypos = 150
        # x_vel = "x-veloc: %.3f" % self.player1.x_velocity
        # x_ori = "x-orien: %.3f" % self.player1.x_orientation
        # y_vel = "y-veloc: %.3f" % self.player1.y_velocity
        # y_ori = "y-orien: %.3f" % self.player1.y_orientation

        # self.show_text(x_vel, 13, pygame.Color('gray45'), info_xpos, info_ypos, False)
        # self.show_text(x_ori, 13, pygame.Color('gray45'), info_xpos, info_ypos + 23, False)
        # self.show_text(y_vel, 13, pygame.Color('gray45'), info_xpos, info_ypos + 23 + 33, False)
        # self.show_text(y_ori, 13, pygame.Color('gray45'), info_xpos, info_ypos + 23 + 33 + 23, False)

    def show_title_text(self, text, font_size, font_color, x, y, is_centered):
        font = pygame.font.Font("../fonts/minecraft.ttf", font_size)

        # Render text
        text_surf = Crystal_title.textCrystal(font, text, 2, font_color, 170)
        # text_surf = font.render(text, 1, font_color)

        if is_centered:
            textpos = text_surf.get_rect()
            textpos.centerx = self.surface.get_rect().centerx
            textpos.y = y
        else:
            textpos = (x, y)

        # Blit it
        self.surface.blit(text_surf, textpos)

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

        # Any cookies collected?
        for collec in self.cookie_list:
            if Utils.do_rects_intersect(self.player1.rect.x, self.player1.rect.y, self.player1.rect.h,
                                        self.player1.rect.w, collec.rect.x, collec.rect.y, collec.rect.h,
                                        collec.rect.w):
                # Increase the score
                self.player1.score += 10
                # Delete the cookie
                self.cookie_list.remove(collec)
                self.all_sprite_list.remove(collec)

            if Utils.do_rects_intersect(self.player2.rect.x, self.player2.rect.y, self.player2.rect.h,
                                        self.player2.rect.w, collec.rect.x, collec.rect.y, collec.rect.h,
                                        collec.rect.w):
                # Increase the score
                self.player2.score += 10
                # Delete the cookie
                self.cookie_list.remove(collec)
                self.all_sprite_list.remove(collec)

        # ------------ Asteroid collisions are handled here ------------- #
        # --- Player 1 --- #
        # If there's any explosions happening, make the next explosion frame
        if self.explosion_player1 is not None:
            are_we_done_yet = self.explosion_player1.explode()

            # If the explosion animation's done, reset the player on the screen
            if are_we_done_yet:
                # Reset the player to his initial position
                self.player1.reset_player_on_screen()
                self.all_sprite_list.add(self.player1)
                self.explosion_player1 = None

                # Reduce score & life
                self.player1.score -= 5
                self.player1.reduce_life()
        else:
            # Any asteroids hit?
            for collec in self.asteroid_list:
                if Utils.do_rects_intersect(self.player1.rect.x, self.player1.rect.y, self.player1.rect.h,
                                            self.player1.rect.w, collec.rect.x, collec.rect.y, collec.rect.h,
                                            collec.rect.w):
                    self.explosion_player1 = Explosion(self.player1.rect.x, self.player1.rect.y, self.surface)
                    self.all_sprite_list.remove(self.player1)

        # --- Player 2 --- #
        # If there's any explosions happening, make the next explosion frame
        if self.explosion_player2 is not None:
            are_we_done_yet = self.explosion_player2.explode()

            # If the explosion animation's done, reset the player on the screen
            if are_we_done_yet:
                # Reset the player to his initial position
                self.player2.reset_player_on_screen()
                self.all_sprite_list.add(self.player2)
                self.explosion_player2 = None

                # Reduce score & life
                self.player2.score -= 5
                self.player2.reduce_life()
        else:
            # Any asteroids hit?
            for collec in self.asteroid_list:
                if Utils.do_rects_intersect(self.player2.rect.x, self.player2.rect.y, self.player2.rect.h,
                                            self.player2.rect.w, collec.rect.x, collec.rect.y, collec.rect.h,
                                            collec.rect.w):
                    self.explosion_player2 = Explosion(self.player2.rect.x, self.player2.rect.y, self.surface)
                    self.all_sprite_list.remove(self.player2)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_num, x, y, initial_x_velocity, initial_y_velocity, wall_list, img_src, img_dimensions):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Score is initially zero
        self.score = 0

        # Initially the player has 3 lives
        self.lives = 3

        # Player number
        self.player_num = player_num

        # Load the image
        self.image = pygame.image.load(img_src)
        self.image = pygame.transform.scale(self.image, img_dimensions).convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        # Store the starting position and velocity of the player
        self.original_x = x
        self.original_y = y

        self.initial_x_velocity = initial_x_velocity
        self.initial_y_velocity = initial_y_velocity

        self.reset_player_on_screen()

        self.x_orientation = 1
        self.y_orientation = -1

        self.wall_list = wall_list

    def reduce_life(self):
        self.lives -= 1

        # TODO: Handle this game-over scenario
        if self.lives <= 0:
            print "Game over for player %d" % self.player_num

    def reset_player_on_screen(self):

        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.x_velocity = self.initial_x_velocity
        self.y_velocity = self.initial_y_velocity

    def deal_with_event(self):
        global key_held

        # While the key is held
        if key_held is not None:
            if ("UP" in key_held and self.player_num == 2) or ("W" in key_held and self.player_num == 1):
                if self.y_orientation == -1:
                    self.y_velocity += y_acc_booster
                else:
                    self.y_velocity -= y_acc_booster
            if ("DOWN" in key_held and self.player_num == 2) or ("S" in key_held and self.player_num == 1):
                if self.y_orientation == 1:
                    self.y_velocity += y_acc_booster
                else:
                    self.y_velocity -= y_acc_booster
            if ("LEFT" in key_held and self.player_num == 2) or ("A" in key_held and self.player_num == 1):
                if self.x_orientation == 1:
                    self.x_velocity -= x_acc_booster
                else:
                    self.x_velocity += x_acc_booster
            if ("RIGHT" in key_held and self.player_num == 2) or ("D" in key_held and self.player_num == 1):
                if self.x_orientation == -1:
                    self.x_velocity -= x_acc_booster
                else:
                    self.x_velocity += x_acc_booster

        # Restrict max velocities
        if self.y_velocity > y_max_velocity:
            self.y_velocity = y_max_velocity

        if self.x_velocity > x_max_velocity:
            self.x_velocity = x_max_velocity

        # TODO: Should I do this for y-direction as well?
        if self.x_velocity < 0.000:
            self.x_velocity = 0.000
            if ("LEFT" in key_held and self.player_num == 2) or ("A" in key_held and self.player_num == 1):
                self.x_orientation = -1
            elif ("RIGHT" in key_held and self.player_num == 2) or ("D" in key_held and self.player_num == 1):
                self.x_orientation = 1

                # Instead of letting acceleration go negative
                # in the y-direction, force it to be zero
                # if self.y_velocity < 0.000:
                # self.y_velocity = 0.000

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


class Cookie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Random cookie
        cookie_number = random.randint(1, 7)

        # Load the image
        self.image = pygame.image.load("../images/allcookies/cookie-%d.png" % cookie_number).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 29))

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.image = pygame.image.load("../images/asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Explosion():
    def __init__(self, x, y, surface):

        # Load the image
        self.image = pygame.image.load("../images/explosion_spritesheet.png").convert_alpha()

        # Re-scaled image
        self.height = 45
        self.width = self.image.get_rect().w / (self.image.get_rect().h / 45)

        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Number of frames in the spritesheet
        self.num_of_frames = 16

        self.x = x
        self.y = y

        self.explosion_frame = 0

        self.surface = surface

        self.wait = 0

    # Takes care of the explosion animation
    def explode(self):

        if self.explosion_frame >= (self.num_of_frames - 1):
            # We're done with the explosion animation
            return True
        else:
            self.surface.blit(self.image, [self.x, self.y], (
                (self.explosion_frame % self.num_of_frames) * self.width / self.num_of_frames, 0,
                self.width / self.num_of_frames, 45))
            if self.wait % 10 == 0:
                self.explosion_frame += 1
            self.wait += 1

            return False  # Not done yet


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, heart_size):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.heart_size = heart_size

        self.make_full_heart()

        # Set background color to be transparent
        self.image.set_colorkey(background_color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def make_full_heart(self):
        # Load the image
        self.image = pygame.image.load("../images/heart_full.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.heart_size, self.heart_size))

    def make_empty_heart(self):
        # Load the image
        self.image = pygame.image.load("../images/heart_empty.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.heart_size, self.heart_size))


# class New_game_button:
# def __init__(self, text):


Main()