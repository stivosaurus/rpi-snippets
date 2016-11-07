import pygame
from pygame.locals import *
import time

if __name__ == "__main__":
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont('Impact',20,16)

    title = font.render(('SQUASH!'), True, (255,255,255))
    play = font.render(('PLAY'), True, (255,255,255))
    play_r = play.get_rect()
    play_r.x, play_r.y = 300,300

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,255,0,))
        screen.blit(title, (400, 400))
        screen.blit(play, (300,300))
        if play_r.collidepoint(pygame.mouse.get_pos()):
            print 'Detected'
        else:
            print 'notdet'
        time.sleep(0.000000000000000000000000000000000000000000000000000000001)
        pygame.display.flip()
