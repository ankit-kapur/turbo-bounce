from pygame.locals import *
import pygame
import math

class Ball(pygame.sprite.Sprite):
    """ The ball """
    def __init__(self, image, gravity, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        self.gravity = gravity
        self.cap = 50
        self.bounce = 0.66
        self.friction = 0.99
        self.kick = 1.3
        self.x = x; self.y = y
        self.dx = 0; self.dy = 0
        self.on_ground = False
        self.spin = 0
        self.angle = 0

    def center(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.x += self.dx/2
        self.y += self.dy/2
        self.angle += self.spin
        if self.angle < 0: self.angle += 360
        if self.angle > 360: self.angle -= 360
        if not self.on_ground: self.dy += self.gravity
        if self.dy > self.cap: self.dy = self.cap
        if self.on_ground:
            self.dx *= self.friction
            self.spin = -self.dx
        if self.on_ground and abs(self.dx) - 0.5 < 0:
            self.dx = 0
            self.spin = -self.dx
        self.rect.x = self.x
        self.rect.y = self.y

def main(screen):
    pygame.display.set_caption('Ball-E')
    pygame.display.set_icon(pygame.image.load('./data/icon.png'))
    screen.fill((0,0,0)); screen.set_colorkey((0,0,0))

    ballimg = pygame.image.load('./data/ball.png')
    ballimg.set_colorkey(ballimg.get_at((0,0)))
    # pygame.mixer.music.load('./data/kick.ogg')
    screen_size = screen.get_size()
    center = (screen_size[0]/2, screen_size[1]/2)

    score = 0
    highscore = 0
    paused = False

    font1 = pygame.font.Font('./data/font.ttf', 40)
    font2 = pygame.font.Font('./data/font.ttf', 22)
    font3 = pygame.font.Font('./data/font.ttf', 52)
    font4 = pygame.font.Font('./data/font.ttf', 16)
    title = font3.render('Keep the ball in the air!', 1, (255,255,255))
    info1 = font4.render('Esc - Quit', 1, (255,255,255))
    info2 = font4.render('P - Pause', 1, (255,255,255))
    info3 = font3.render('Paused', 1, (255,255,255))
    score_text = font1.render(str(score), 1, (255,155,155))
    highscore_text = font2.render(str(highscore), 1, (255,255,255))

    score_rect = score_text.get_rect()
    highscore_rect = highscore_text.get_rect()
    highscore_rect.y = score_rect.bottom+5
    highscore_rect.x = 5
    score_rect.x = 20
    title_rect = title.get_rect()
    title_rect.y = score_rect.centery
    info1_rect = info1.get_rect()
    info1_rect.right = screen_size[0]-5
    info1_rect.y = 5
    info2_rect = info2.get_rect()
    info2_rect.x = info1_rect.x
    info2_rect.y = info1_rect.bottom+5
    title_rect.centerx = (screen_size[0]-score_rect.width-info1_rect.width)/2
    info3_rect = info3.get_rect()
    info3_rect.centerx = center[0]
    info3_rect.centery = center[1]

    ball = Ball(ballimg, 1, *center); ball.center()
    pointer = pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], 1,1)
    pointer_mask = pygame.Mask((1,1)); pointer_mask.set_at((0,0),1)
    subrect = ballimg.get_rect()
    subrect.width=84
    subrect.height=83

    clock = pygame.time.Clock()
    ball.update()
    screen.blit(ball.image, ball.rect)
    screen.blit(score_text, score_rect)
    screen.blit(highscore_text, highscore_rect)
    screen.blit(title, title_rect)
    screen.blit(info1, info1_rect)
    screen.blit(info2, info2_rect)
    pygame.display.flip()

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_p:
                    paused = not paused

        pointer.x, pointer.y = pygame.mouse.get_pos()

        if ball.rect.colliderect(pointer) and not paused:
            if ball.mask.get_at((int(pointer.x-ball.x), int(pointer.y-ball.y))):
                # pygame.mixer.music.play(0, 0.14) # there is a small silence right before the sound
                hit = ball.mask.overlap(pointer_mask, (int(pointer.x-ball.x), int(pointer.y-ball.y)))
                hit = (hit[0]-ball.rect.width/2, hit[1]-ball.rect.height/2)
                angle = math.degrees(math.atan2(hit[0], hit[1])) # angle at which we hit
                dx = 30*math.cos(math.radians(angle+90))
                dy = 30*math.sin(math.radians(angle-90))
                ball.dx = dx; ball.dy = dy
                ball.on_ground = False
                ball.spin = -dx/5
                score += 1
                score_text = font1.render(str(score), 1, (255,155,155))

        if ball.x > screen_size[0]-ball.rect.width:
            ball.x = screen_size[0]-ball.rect.width
            ball.dx = -ball.dx*ball.friction
            ball.spin = ball.dy
            # pygame.mixer.music.play(0,0.14)
        if ball.y > screen_size[1]-ball.rect.height:
            score = 0
            score_text = font1.render(str(score), 1, (255,155,155))
            ball.y = screen_size[1]-ball.rect.height
            if not ball.on_ground: ball.dx *= ball.friction
            ball.spin = -ball.dx
            if (ball.dy*ball.bounce)-5 > 0:
                ball.dy = -ball.dy*ball.bounce
            else:
                ball.dy = 0
                ball.on_ground = True
            # pygame.mixer.music.play(0,0.14)
        if ball.x < 0:
            ball.x = 0
            ball.dx = -ball.dx*ball.bounce
            ball.spin = -ball.dy
            # pygame.mixer.music.play(0,0.14)

        if score > highscore:
            highscore = score
            highscore_text = font2.render(str(highscore), 1, (255,255,255))

        ball.update()

        rotated = pygame.transform.rotate(ball.image, ball.angle)
        size = rotated.get_size()
        subrect.centerx = size[0]/2
        subrect.centery = size[1]/2
        newimg = rotated.subsurface(subrect)

        screen.fill((0,0,0))
        screen.blit(newimg, ball.rect)
        screen.blit(score_text, score_rect)
        screen.blit(highscore_text, highscore_rect)
        screen.blit(title, title_rect)
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
        if paused: screen.blit(info3, info3_rect)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700,600))
    main(screen)
    pygame.quit()
