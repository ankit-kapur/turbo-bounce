import sys, pygame

pygame.init()
size = width, height = 520, 540
speed = [1, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("src/black_ball.png")
ball_rect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] = -speed[0]
    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill((255,255,255))
    screen.blit(ball, ball_rect)
    pygame.display.flip()