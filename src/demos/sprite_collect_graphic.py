""" 
 Show how to use a sprite backed by a graphic.
  
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
import pygame
import random
 
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
 
# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # READ BEFORE USING:
    # This constructor lets you use any graphic:
    # my_sprite = Block("any_graphic.png")
    # But if you DON'T want any graphic, use the following instead:
    '''
    def __init__(self):
        super().__init__() 
 
        self.image = pygame.image.load("my_graphic.png").convert()
 
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey(BLACK)
 
        self.rect = self.image.get_rect()
    '''
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(filename).convert()
 
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey(BLACK)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    block = Block("../images/black_ball.png")
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    pygame.sprite.Sprite.__init__(block)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
     
# Create a RED player block
player = Block("../images/pokeball.png")
pygame.sprite.Sprite.__init__(player)
all_sprites_list.add(player)
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    # Clear the screen
    screen.fill(WHITE)
 
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()
     
    # Fetch the x and y out of the list, 
    # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    player.rect.x = pos[0]
    player.rect.y = pos[1]
     
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
     
    # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        print(score)
         
    # Draw all the spites
    all_sprites_list.draw(screen)
     
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()