import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_FONT
from scripts.ui.dialog_box import DialogueBox
from scripts.ui.menu import Menu

def start_game_in_cabin(screen):
    clock = pygame.time.Clock()
    background = pygame.image.load('assets/locations/ship_room.png').convert()

    bg_width, bg_height = background.get_size()
    new_width = int(bg_width * 1.7)
    new_height = int(bg_height * 1.3)
    background = pygame.transform.scale(background, (new_width, new_height))
    x_offset = (SCREEN_WIDTH - new_width) // 2
    y_offset = (SCREEN_HEIGHT - new_height) // 2

    alpha_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(255)
    fade_duration = 0.1
    fade_ticks = fade_duration * 60
    alpha_step = 255 / fade_ticks

    menu = Menu()
    dialogue_box = DialogueBox(DEFAULT_FONT)

    cursor_image = pygame.image.load('assets/images/cursor.png').convert_alpha()
    cursor_image = pygame.transform.scale(cursor_image, (14, 20))
    cursor_rect = cursor_image.get_rect()

    cursor_x = 60
    cursor_y =-60

    pygame.mouse.set_visible(False)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            menu.handle_input(event)

        if menu.exit_game:
            running = False
            continue

        if alpha_surface.get_alpha() > 0:
            alpha_surface.set_alpha(alpha_surface.get_alpha() - alpha_step)

        screen.fill((0, 0, 0))
        screen.blit(background, (x_offset, y_offset))
        screen.blit(alpha_surface, (0, 0))

        if not menu.show_pause_menu:
            if dialogue_box.current_dialogue <= 6:
                dialogue_box.update_text()
                dialogue_box.render(screen)

        if menu.show_pause_menu:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(30)
            screen.blit(fade_surface, (0, 0))
            menu.display(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_x, cursor_y = mouse_x, mouse_y
        cursor_rect.topleft = (cursor_x, cursor_y)

        screen.blit(cursor_image, cursor_rect)

        pygame.display.flip()
        clock.tick(60)
