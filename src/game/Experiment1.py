import pygame
import threading
# import random
# import math

# --------- Config --------- #

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 119, 0)

# Window config
background_color = black
window_height = 400
window_width = 800

# Player ball config
ball_width = 20
ball_height = 20

# By how much the acceleration increases/decreases
x_acc_booster = 0.05
y_acc_booster = 0.02


# -------- Global variables -------- #

# Exit when this is true
time_to_exit = False

# Acceleration values
x_acceleration = 0.0
y_acceleration = 0.0

# Thread for key press events
class getKeyPress(threading.Thread):
    def run(self):
        global x_acceleration
        global y_acceleration
        global time_to_exit

        pygame.init()

        events = pygame.event.get()
        for e in events:
            if e.type is pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    time_to_exit = True
                elif e.key == pygame.K_UP:
                    y_acceleration += y_acc_booster
                elif e.key == pygame.K_DOWN:
                    y_acceleration -= y_acc_booster
                elif e.key == pygame.K_LEFT:
                    x_acceleration -= x_acc_booster
                elif e.key == pygame.K_RIGHT:
                    x_acceleration += x_acc_booster

                # Instead of letting acceleration go negative
                # in the y-direction, force it to be zero
                if y_acceleration < 0.000:
                    y_acceleration = 0.000

            if e.type is pygame.QUIT:
                # To quit when the close button is clicked
                time_to_exit = True


# Ball is a subclass of the Sprite class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        # Call the super class's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make an image of the ball
        self.image = pygame.Surface([ball_width, ball_height])
        # Fill it up
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Set the initial x and y co-ords
        self.rect.x = x
        self.rect.y = y

        # Orientation: 1 means the x/y coord is increasing, -1 means its decreasing
        self.x_orientation = 1
        self.y_orientation = 1

    def update(self):
        global x_acceleration
        global y_acceleration
        global window_height
        global window_width

        self.rect.x += x_acceleration * self.x_orientation
        self.rect.y += y_acceleration * self.y_orientation
        if self.rect.x >= window_width:
            self.x_orientation = -1
        elif self.rect.x <= 0:
            self.x_orientation = 1
        if self.rect.y >= window_height:
            self.y_orientation = -1
        elif self.rect.y <= 0:
            self.y_orientation = 1


class Main(threading.Thread):
    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    ball_list = pygame.sprite.Group()

    # This is a list of every sprite.
    # All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()

    # This is the background on which everything will be drawn
    background = None

    # The player balls
    ball1 = None

    def make_balls(self):
        self.ball1 = Ball(red, window_height - 20, 20)

        # Add the balls to the lists
        self.all_sprites_list.add(self.ball1)


    def __init__(self):
        threading.Thread.__init__(self)

        pygame.init()

        # Make the background
        screensize = (window_width, window_height)
        self.background = pygame.display.set_mode(screensize)

        # Make balls
        self.make_balls()


        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def run(self):
        # Clear up the screen
        self.background.fill(background_color)

        # --- Change stuff here --- #
        self.all_sprites_list.update()

        # --- Update/draw the changed stuff --- #
        self.all_sprites_list.draw(self.background)

        # Display everything
        pygame.display.flip()

        # Limit to 60 frames per second
        self.clock.tick(60)

# --- Making 2 threads --- #
# 1st thread is for listening to keypress events
#  2nd for running the actual code

# Make the threads
keyListenerThread = getKeyPress()
mainThread = Main()

# Start the threads
# ---- Main program loop ---- #
while not time_to_exit:
    keyListenerThread.run()
    mainThread.run()