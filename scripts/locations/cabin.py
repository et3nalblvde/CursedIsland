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

    dialogue_box = DialogueBox(DEFAULT_FONT)
    menu = Menu()


    cursor_image = pygame.image.load('assets/images/cursor.png').convert_alpha()
    cursor_image = pygame.transform.scale(cursor_image, (14, 20))
    cursor_rect = cursor_image.get_rect()


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
                box_width = screen.get_width() - 40
                box_height = 200
                box_x = 20
                box_y = screen.get_height() - box_height - 20

                pygame.draw.rect(screen, (139, 69, 19), (box_x, box_y, box_width, box_height))
                pygame.draw.rect(screen, (255, 255, 255),
                                 (box_x + 5, box_y + 5, box_width - 10, box_height - 10))

                dialogue_box.update_text()

                words = dialogue_box.dialogue_text.split(' ')
                lines = []
                current_line = ''
                max_width = box_width - 40

                for word in words:
                    test_line = current_line + word + ' '
                    test_width, _ = dialogue_box.font.size(test_line)

                    if test_width <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + ' '

                if current_line:
                    lines.append(current_line)

                y_offset_text = box_y + 20
                for line in lines:
                    text_surface = dialogue_box.font.render(line, True, (0, 0, 255))
                    screen.blit(text_surface, (box_x + 20, y_offset_text))
                    y_offset_text += dialogue_box.font.get_height()


        if menu.show_pause_menu:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(30)
            screen.blit(fade_surface, (0, 0))
            menu.display(screen)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_rect.topleft = (mouse_x, mouse_y)


        screen.blit(cursor_image, cursor_rect)

        pygame.display.flip()
        clock.tick(60)
