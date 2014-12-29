import pygame
from pygame.locals import *

# Boundary wall padding
boundary_wall_padding = 20

# Window dimensions
window_height = 600
window_width = 800

x_max_velocity = 3
y_max_velocity = 1.5

# Rate by which a key press moves a ball
x_acc_booster = 0.003
y_acc_booster = 0.001

# Colors
wall_color = pygame.Color('darkred')
text_color = pygame.Color('gray45')
# Background color
background_color = pygame.Color('white')

x_orientation = 1
y_orientation = 1

key_held = None


class Main():

    def __init__(self):
        pygame.init()
        global key_held

        clock = pygame.time.Clock()

        # List to hold all the sprites
        self.all_sprite_list = pygame.sprite.Group()

        # Make the walls. (x_pos, y_pos, width, height)
        self.wall_list = pygame.sprite.Group()

        screensize = (window_width, window_height)
        self.surface = pygame.display.set_mode(screensize)
        pygame.display.set_caption("Turbo bounce")

        # ---- Making the balls
        ball1_initial_x = 5
        ball1_initial_y = 5
        # Initial velocities
        initial_x_velocity = 0.2
        initial_y_velocity = 0.1
        ball1 = Ball(ball1_initial_x, ball1_initial_y, initial_x_velocity, initial_y_velocity)
        self.all_sprite_list.add(ball1)

        # ----- Making the WALLS
        self.make_the_walls()

        done = False
        key_held = False
        while not done:

            # msElapsed = clock.tick(30)

            self.surface.fill(background_color)

            self.all_sprite_list.update()
            # box2.update(x_velocity, y_velocity)
            # box3.update(x_velocity, y_velocity)

            self.all_sprite_list.draw(self.surface)
            # box2.draw(self.surface)
            # box3.draw(self.surface)

            # ----- Text banners
            self.showTextBanners()

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

    def make_the_walls(self):
        distance_from_top = 120
        boundary_wall1 = Wall(boundary_wall_padding, distance_from_top, 10, window_width - (boundary_wall_padding * 2), wall_color)
        boundary_wall2 = Wall(boundary_wall_padding, window_height - (boundary_wall_padding * 1.5), 10, window_width - (boundary_wall_padding * 2), wall_color)
        boundary_wall3 = Wall(boundary_wall_padding, distance_from_top, window_height - (boundary_wall_padding * 1.5) - distance_from_top, 10, wall_color)
        boundary_wall4 = Wall(window_width - (boundary_wall_padding * 2.5) + boundary_wall_padding, distance_from_top, window_height - (boundary_wall_padding * 1.5) - distance_from_top, 10, wall_color)

        self.wall_list.add(boundary_wall1)
        self.wall_list.add(boundary_wall2)
        self.wall_list.add(boundary_wall3)
        self.wall_list.add(boundary_wall4)
        self.all_sprite_list.add(boundary_wall1)
        self.all_sprite_list.add(boundary_wall2)
        self.all_sprite_list.add(boundary_wall3)
        self.all_sprite_list.add(boundary_wall4)


    def showTextBanners(self):
        self.showText("TURBO BOUNCE", 28, pygame.Color('darkred'), None, 10, True)
        self.showText("Created by Ankit Kapur", 14, pygame.Color('gray36'), None, 50, True)
        self.showText("Player 1: 0", 16, text_color, 600, 100, False)

    def showText(self, text, font_size, font_color, x, y, is_centered):
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


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, initial_x_velocity, initial_y_velocity):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.image = pygame.image.load("../images/pokeball.png").convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.x_velocity = initial_x_velocity
        self.y_velocity = initial_y_velocity

        # def draw(self, self.surface):

        # ball = pygame.image.load("../images/black_ball.png")
        # ball_rect = ball.get_rect()
        # self.surface.blit(ball, [self.rect.x, self.rect.y])

    def dealWithEvent(self):
        global key_held

        # While the key is held
        if key_held is not None:
            if key_held == "UP":
                self.y_velocity += y_acc_booster
            elif key_held == "DOWN":
                self.y_velocity -= y_acc_booster
            elif key_held == "LEFT":
                self.x_velocity -= x_acc_booster
            elif key_held == "RIGHT":
                self.x_velocity += x_acc_booster

        # Instead of letting acceleration go negative
        # in the y-direction, force it to be zero
        if self.y_velocity < 0.000:
            y_velocity = 0.1
        elif self.y_velocity > y_max_velocity:
            y_velocity = y_max_velocity
            # if x_velocity < 0.000:
            # x_velocity = 0.04

    def update(self):
        global x_orientation
        global y_orientation

        self.dealWithEvent()

        self.rect.x += self.x_velocity * x_orientation
        self.rect.y += self.y_velocity * y_orientation
        if self.rect.x >= window_width:
            x_orientation = -1
        elif self.rect.x <= 0:
            x_orientation = 1
        if self.rect.y >= window_height:
            y_orientation = -1
        elif self.rect.y <= 0:
            y_orientation = 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, obj_color):
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

        # Make a blue wall, of the size specified in the parameters
        # self.image = pygame.Surface([width, height])
        # self.image.fill(obj_color)

        # Make our top-left corner the passed-in location.
        # self.rect = self.image.get_rect()
        # self.rect.y = y
        # self.rect.x = x


Main()