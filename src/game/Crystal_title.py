import os, sys, pygame, pygame.font, pygame.image
from pygame.locals import *


def shadeColor(color, amount):
    """Brightens or darkens color by amount (-255 - 255)."""
    r = color[0] + amount
    g = color[1] + amount
    b = color[2] + amount
    if r > 255: r = 255
    if r < 0:   r = 0
    if g > 255: g = 255
    if g < 0:   g = 0
    if b > 255: b = 255
    if b < 0:   b = 0
    return (r, g, b)


def textCrystal(font, message, bevel=5, fontcolor=(64, 128, 255), contrast=70):
    """Renders text with a 'crystal' style apperance."""
    base = font.render(message, 0, fontcolor)
    size = base.get_width() + bevel * 2, base.get_height() + bevel * 2 + 2
    img = pygame.Surface(size, 16)

    tl = (-1, -1)
    tc = (0, -1)
    tr = (1, -1)
    cr = (1, 0)
    br = (1, 1)
    bc = (0, 1)
    bl = (-1, 1)
    cl = (-1, 0)

    for x in range(-bevel, 1, 1):
        for position in (tl, tr, br, bl, tc, cr, bc, cl):
            for location in (tl, tr, br, bl, tc, cr, bc, cl):
                shade = ((-location[0]) - location[1]) * contrast
                img.blit(font.render(message, 1, shadeColor(fontcolor, shade)),
                         (bevel + location[0] + (x * position[0]), bevel + location[1] + (x * position[1])))
        img.blit(font.render(message, 1, fontcolor), (bevel, bevel))
    return img


entry_info = 'Turbo bounce'


# this code will display our work, if the script is run...
if __name__ == '__main__':
    pygame.init()

    #create our fancy text
    white = 255, 255, 255
    grey = 100, 100, 100
    bigfont = pygame.font.Font("../fonts/minecraft.ttf", 30)
    text = textCrystal(bigfont, entry_info, 4, (64, 128, 255), 170)

    #create a window the correct size
    win = pygame.display.set_mode(text.get_size())
    winrect = win.get_rect()
    win.blit(text, (0, 0))
    pygame.display.flip()

    #wait for the finish
    while 1:
        event = pygame.event.wait()
        if event.type is KEYDOWN and event.key == K_s:  #save it
            name = os.path.splitext(sys.argv[0])[0] + '.bmp'
            print 'Saving image to:', name
            pygame.image.save(win, name)
        elif event.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
            break