import sys
import pygame

win = pygame.display.set_mode((100, 100))
c = pygame.time.Clock()

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        
    pygame.display.flip()
    c.tick(60)