import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def start_game_in_cabin(screen):
    clock = pygame.time.Clock()

    background = pygame.image.load('assets/locations/ship_room.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    black_surface.fill((0, 0, 0))


    fade_duration = 3
    fade_ticks = fade_duration * 60
    alpha = 255

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if alpha > 0:
            alpha -= 255 / fade_ticks
            if alpha < 0:
                alpha = 0

        black_surface.set_alpha(alpha)
        screen.blit(black_surface, (0, 0))

        if alpha == 0:
            screen.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
