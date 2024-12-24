import pygame
from PIL import Image
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, DEFAULT_FONT
import time


class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(DEFAULT_FONT, 60)
        self.title_text = 'Проклятый остров'
        self.start_text = 'Нажмите Enter для продолжения'

        self.button_texts = ['Начать игру', 'Настройки', 'Выход']
        self.buttons = [self.font.render(text, True, (0, 0, 255)) for text in self.button_texts]

        self.button_width = max(button.get_width() for button in self.buttons)
        self.button_height = self.buttons[0].get_height()

        self.background = pygame.image.load("assets/images/map.png")
        self.background = pygame.transform.scale(self.background, (self.button_width + 30, self.button_height + 10))
        self.frames = self.load_gif("assets/videos/sea.gif")
        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_delay = 0.1
        self.last_update = pygame.time.get_ticks()

        self.alpha = 255
        self.fade_duration = 10
        self.fade_start_time = pygame.time.get_ticks()

        self.cursor = pygame.image.load("assets/images/cursor.png")
        self.cursor = pygame.transform.scale(self.cursor, (14, 20))
        self.cursor_rect = self.cursor.get_rect()

        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        self.show_main_menu = False
        self.show_options_menu = False

        self.selected_button = 0

        self.volume = 1.0
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fullscreen = False
        self.autosave = True
        self.difficulty = 'Легко'

        self.last_text_update = pygame.time.get_ticks()
        self.text_speed = 60
        self.text_displayed = ""

        self.last_back_click_time = 0
        self.back_click_delay = 200

        self.last_click_time = 0
        self.click_delay = 200

        self.game_started = False

    def load_gif(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = pygame.image.fromstring(gif.convert('RGB').tobytes(), gif.size, 'RGB')
            frames.append(frame_image)
        return frames

    def handle_mouse_click(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()

        if not self.game_started:
            return

        if current_time - self.last_click_time < self.click_delay:
            return

        if self.show_options_menu:
            back_label = self.font.render('Назад', True, WHITE)
            back_text_width = back_label.get_width()
            back_text_height = back_label.get_height()

            back_bg_width = back_text_width + 40
            back_bg_height = back_text_height + 20
            additional_spacing = 80

            back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
            back_bg_y = SCREEN_HEIGHT // 3 + 5 * (self.button_height + 20) + additional_spacing

            back_button_rect = pygame.Rect(
                back_bg_x, back_bg_y, back_bg_width, back_bg_height
            )

            if back_button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                self.last_click_time = current_time
                self.show_options_menu = False
                return

            option_rects = [
                pygame.Rect(
                    SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                    SCREEN_HEIGHT // 3 + i * (self.button_height + 20),
                    self.background.get_width(),
                    self.background.get_height()
                )
                for i in range(5)
            ]

            for i, option_rect in enumerate(option_rects):
                if option_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    self.last_click_time = current_time
                    if i == 0:
                        self.change_volume(0.1)
                    elif i == 2:
                        self.toggle_fullscreen()
                    elif i == 3:
                        self.toggle_autosave()
                    elif i == 4:
                        self.change_difficulty()
        else:
            for i, button_text in enumerate(self.button_texts):
                button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                    SCREEN_HEIGHT // 2 + i * (self.button_height + 20),
                    self.background.get_width(),
                    self.background.get_height()
                )
                if button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    self.last_click_time = current_time
                    self.execute_action(button_text)

    def display(self, surface):
        surface.fill((0, 0, 0))

        current_frame_resized = pygame.transform.scale(self.frames[self.current_frame], (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(current_frame_resized, (0, 0))

        current_time = pygame.time.get_ticks()
        fade_elapsed = current_time - self.fade_start_time
        if fade_elapsed < self.fade_duration:
            self.alpha = 255 - (fade_elapsed / self.fade_duration) * 255
        else:
            self.alpha = 0

        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(self.alpha)
        surface.blit(fade_surface, (0, 0))

        if self.alpha <= 0:
            if not self.game_started:
                if current_time - self.last_text_update > self.text_speed:
                    if len(self.text_displayed) < len(self.start_text):
                        self.text_displayed += self.start_text[len(self.text_displayed)]
                        self.last_text_update = current_time
                surface.blit(self.font.render(self.text_displayed, True, WHITE),
                             (SCREEN_WIDTH // 2 - self.font.size(self.text_displayed)[0] // 2, SCREEN_HEIGHT // 2))
            else:
                if not self.show_main_menu and not self.show_options_menu:
                    self.show_main_menu = True

                if self.show_options_menu:
                    self.display_options_menu(surface)
                else:
                    surface.blit(self.font.render(self.title_text, True, WHITE),
                                 (SCREEN_WIDTH // 2 - self.font.size(self.title_text)[0] // 2, SCREEN_HEIGHT // 3))

                    for i, button in enumerate(self.buttons):
                        surface.blit(self.background, (SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                                                       SCREEN_HEIGHT // 2 + i * (self.button_height + 20)))

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for i, button in enumerate(self.buttons):
                        button_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                            SCREEN_HEIGHT // 2 + i * (self.button_height + 20),
                            self.background.get_width(),
                            self.background.get_height()
                        )

                        button_color = (255, 255, 255) if button_rect.collidepoint(mouse_x, mouse_y) else (0, 0, 255)
                        button_text = self.font.render(self.button_texts[i], True, button_color)
                        surface.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2,
                                                   SCREEN_HEIGHT // 2 + i * (self.button_height + 20)))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cursor_rect.topleft = (mouse_x, mouse_y)
        surface.blit(self.cursor, self.cursor_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.show_options_menu:
                    self.quit_game()

            if event.type == pygame.KEYDOWN:
                if not self.game_started:
                    if event.key == pygame.K_RETURN:
                        self.game_started = True
                        print("Игра начинается...")
                        self.show_main_menu = True
                    return

                if self.show_main_menu:
                    if event.key == pygame.K_DOWN:
                        self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    elif event.key == pygame.K_UP:
                        self.selected_button = (self.selected_button - 1) % len(self.buttons)

                    if event.key == pygame.K_RETURN:
                        self.execute_action(self.button_texts[self.selected_button])
                    elif event.key == pygame.K_ESCAPE and self.show_options_menu:
                        self.show_options_menu = False

        if current_time - self.last_update > self.frame_delay * 1000:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % self.frame_count

        self.clock.tick(120)

        self.handle_mouse_click(mouse_x, mouse_y)

    def execute_action(self, button_text=None):
        if button_text is None:
            button_text = self.button_texts[self.selected_button]

        if button_text == 'Начать игру':
            print("Начинаем игру...")
            self.start_game()
        elif button_text == 'Настройки':
            print("Открываются настройки...")
            self.show_options_menu = True
        elif button_text == 'Выход':
            print("Выход из игры...")
            self.quit_game()

    def quit_game(self):
        print("Закрытие игры...")
        pygame.quit()
        quit()

    def start_game(self):
        pass

    def change_volume(self, amount):
        self.volume = max(0.0, min(1.0, self.volume + amount))
        pygame.mixer.music.set_volume(self.volume)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        pygame.display.set_mode(self.resolution, pygame.FULLSCREEN if self.fullscreen else 0)

    def toggle_autosave(self):
        self.autosave = not self.autosave

    def change_difficulty(self):
        difficulties = ['Легко', 'Средне', 'Трудно']
        current_index = difficulties.index(self.difficulty)
        print(f"Текущая сложность: {self.difficulty} (Индекс: {current_index})")
        next_index = (current_index + 1) % len(difficulties)
        self.difficulty = difficulties[next_index]
        print(f"Новая сложность: {self.difficulty}")

    def display_options_menu(self, surface):
        option_texts = [
            f"Звук: {int(self.volume * 100)}%",
            f"Полный экран: {'Да' if self.fullscreen else 'Нет'}",
            f"Автосохранение: {'Включено' if self.autosave else 'Выключено'}",
            f"Сложность: {self.difficulty}"
        ]


        option_buttons = []
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, option_text in enumerate(option_texts):
            option_label = self.font.render(option_text, True, (0, 0, 255))

            text_width = option_label.get_width()
            text_height = option_label.get_height()

            bg_width = text_width + 40
            bg_height = text_height + 20

            option_bg_x = SCREEN_WIDTH // 2 - bg_width // 2
            option_bg_y = SCREEN_HEIGHT // 3 + i * (bg_height + 30) + 30

            option_buttons.append((option_bg_x, option_bg_y, bg_width, bg_height))

            button_bg = pygame.transform.scale(self.background, (bg_width, bg_height))
            surface.blit(button_bg, (option_bg_x, option_bg_y))
            surface.blit(option_label, (option_bg_x + 10, option_bg_y + 10))

        back_label = self.font.render('Назад', True, (0, 0, 255))
        back_text_width = back_label.get_width()
        back_text_height = back_label.get_height()

        back_bg_width = back_text_width + 45
        back_bg_height = back_text_height + 20
        back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
        back_bg_y = SCREEN_HEIGHT - back_bg_height - 360

        if back_bg_x < mouse_x < back_bg_x + back_bg_width and back_bg_y < mouse_y < back_bg_y + back_bg_height:
            back_label = self.font.render('Назад', True, (255, 255, 255))
        else:
            back_label = self.font.render('Назад', True, (0, 0, 255))

        button_bg = pygame.transform.scale(self.background, (back_bg_width, back_bg_height))
        surface.blit(button_bg, (back_bg_x, back_bg_y))
        surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))

        option_buttons.append((back_bg_x, back_bg_y, back_bg_width, back_bg_height))
        last_click_time = 0
        delay = 300

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                current_time = pygame.time.get_ticks()

                if current_time - last_click_time >= delay:
                    last_click_time = current_time

                    for i, button in enumerate(option_buttons):
                        x, y, width, height = button
                        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                            if i == len(option_buttons) - 1:
                                self.show_options_menu = False
                            elif i == 0:
                                self.volume += 0.1
                                if self.volume > 1:
                                    self.volume = 0
                            elif i == 1:
                                self.toggle_fullscreen()
                            elif i == 2:
                                self.toggle_autosave()

                                self.change_difficulty()


        pygame.display.update()
