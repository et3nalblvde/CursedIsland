import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_FONT
from scripts.ui.dialog_box import DialogueBox

def start_game_in_cabin(screen):
    clock = pygame.time.Clock()

    background = pygame.image.load('assets/locations/ship_room.png')

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

    running = True
    dialogue_finished = False
    character = None
    paused = False  # Переменная для отслеживания состояния паузы

    # Создаем шрифт для надписи "Пауза"
    pause_font = pygame.font.Font(DEFAULT_FONT, 74)
    pause_text = pause_font.render("Пауза", True, (255, 255, 255))
    pause_text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Создаем шрифт для текста на кнопке
    button_font = pygame.font.Font(DEFAULT_FONT, 36)
    button_text = button_font.render("Вернуться в главное меню", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogue_box.skip_dialogue()
                elif event.key == pygame.K_ESCAPE:  # Обработка нажатия на Esc
                    paused = not paused  # Переключение состояния паузы
                elif event.key == pygame.K_RETURN and paused:  # Обработка нажатия на Enter во время паузы
                    return  # Возврат в главное меню

        if paused:
            screen.fill((0, 0, 0))
            screen.blit(pause_text, pause_text_rect)  # Отображение надписи "Пауза"

            # Рисуем кнопку
            pygame.draw.rect(screen, (139, 69, 19), button_rect.inflate(20, 10))
            screen.blit(button_text, button_rect)

            pygame.display.flip()
            clock.tick(60)
            continue  # Если игра на паузе, пропускаем обновление и рендеринг

        if alpha_surface.get_alpha() > 0:
            alpha_surface.set_alpha(alpha_surface.get_alpha() - alpha_step)

        screen.fill((0, 0, 0))
        screen.blit(background, (x_offset, y_offset))
        screen.blit(alpha_surface, (0, 0))

        if dialogue_box.current_dialogue < len(dialogue_box.dialogues):
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
        else:
            if not dialogue_finished:
                dialogue_finished = True

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
