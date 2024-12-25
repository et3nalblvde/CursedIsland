import pygame

from __init__ import *
pygame.init()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)

def main():
    clock = pygame.time.Clock()


    main_menu = MainMenu()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        main_menu.display(DISPLAYSURF)


        pygame.display.update()


        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
