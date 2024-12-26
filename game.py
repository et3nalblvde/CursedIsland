import pygame
from settings import *
from __init__ import *
pygame.init()


pygame.display.set_caption("Cursed Island")
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
