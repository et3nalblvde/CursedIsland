import pygame
from PIL import Image
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, DEFAULT_FONT
import time
import json
import os
from scripts.locations.cabin import start_game_in_cabin
from settings import DISPLAYSURF


class MainMenu:
    def __init__(self):
        self.settings = Settings(self)
        self.font = pygame.font.Font(DEFAULT_FONT, 60)
        self.title_text = self.settings.get_text('title')
        self.start_text = self.settings.get_text('press_enter')
        self.fullscreen = False
        self.language = 'ru'
        self.button_texts = ['Продолжить', 'Начать игру', 'Настройки', 'Выход']
        self.buttons = [self.font.render(text, True, (0, 0, 255)) for text in self.button_texts]

        self.button_width = max(button.get_width() for button in self.buttons)
        self.button_height = self.buttons[0].get_height()
 # Экран, передаваемый в конструктор
        self.x_offset = 0  # Переменная для смещения по оси X
        self.y_offset = -110
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

        pygame.mixer.init()
        self.menu_music_path = "audio/music/menu_theme.mp3"
        self.music_playing = False
        self.music_delay = 100
        self.show_main_menu = False
        self.show_options_menu = False
        self.music_start_time = None
        self.selected_button = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.last_text_update = pygame.time.get_ticks()
        self.text_speed = 60
        self.text_displayed = ""

        self.last_back_click_time = 0
        self.back_click_delay = 200

        self.last_click_time = pygame.time.get_ticks()  # Инициализация времени последнего клика
        self.click_delay = 200  # Задержка между кликами

        self.game_started = False

        self.settings = Settings(self)
        self.update_button_texts()

    def load_gif(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = pygame.image.fromstring(gif.convert('RGB').tobytes(), gif.size, 'RGB')
            frames.append(frame_image)
        return frames

    def play_menu_music(self):
        current_time = pygame.time.get_ticks()
        if self.music_start_time is None:
            self.music_start_time = current_time

        if current_time - self.music_start_time >= self.music_delay:
            if not self.music_playing:
                pygame.mixer.music.load(self.menu_music_path)
                pygame.mixer.music.play(-1)
                self.music_playing = True

    def stop_menu_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def update_button_texts(self):
        self.button_texts = [
            self.settings.get_text('continue'),
            self.settings.get_text('start_game'),
            self.settings.get_text('settings'),
            self.settings.get_text('exit')
        ]
        self.buttons = [self.font.render(text, True, (0, 0, 255)) for text in self.button_texts]

    def handle_mouse_click(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time < 500:
            return

        if not self.game_started:
            return

        if current_time - self.last_click_time < 200:
            return

        if self.show_options_menu:
            option_texts = [
                f"Звук: {int(self.settings.volume * 100)}%",
                f"Смена языка: {self.settings.language}",
                f"Автосохранение: {'Включено' if self.settings.autosave else 'Выключено'}",
                f"Сложность: {self.settings.difficulty}"
            ]

            option_buttons = []
            for i, option_text in enumerate(option_texts):
                option_label = self.font.render(option_text, True, (0, 0, 255))

                text_width = option_label.get_width()
                text_height = option_label.get_height()

                bg_width = text_width + 40
                bg_height = text_height + 20

                # Управляем позициями кнопок в меню настроек с учетом смещения
                option_bg_x = SCREEN_WIDTH // 2 - bg_width // 2 + self.x_offset  # Центр по оси X с учетом смещения
                option_bg_y = SCREEN_HEIGHT // 3 + i * (
                            bg_height + 30) + 400 + self.y_offset  # Позиция по оси Y с учетом смещения

                option_buttons.append((option_bg_x, option_bg_y, bg_width, bg_height, i))

                # Отображение прямоугольника для отладки
                pygame.draw.rect(self.screen, (255, 0, 0), (option_bg_x, option_bg_y, bg_width, bg_height),
                                 2)  # Красный контур

                # Проверка клика на кнопку настроек
                if option_bg_x < mouse_x < option_bg_x + bg_width and option_bg_y < mouse_y < option_bg_y + bg_height:
                    if pygame.mouse.get_pressed()[0]:
                        if current_time - self.last_click_time > self.click_delay:
                            if i == 0:
                                self.settings.change_volume(0.1)
                            elif i == 1:
                                new_language = 'en' if self.settings.language == 'ru' else 'ru'
                                self.settings.change_language(new_language)
                            elif i == 2:
                                self.settings.toggle_autosave()
                            elif i == 3:
                                self.settings.change_difficulty()
                            self.last_click_time = current_time  # Обновляем время последнего клика

            # Кнопка "Назад" в меню настроек
            back_label = self.font.render('Назад', True, (0, 0, 255))
            back_text_width = back_label.get_width()
            back_text_height = back_label.get_height()

            back_bg_width = back_text_width + 45
            back_bg_height = back_text_height + 20

            # Управление позицией кнопки "Назад" с учетом смещения
            back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2 + self.x_offset  # Центр по оси X с учетом смещения
            back_bg_y = SCREEN_HEIGHT - back_bg_height - 360 + self.y_offset  # Позиция по оси Y с учетом смещения

            # Отображение прямоугольника для отладки
            pygame.draw.rect(self.screen, (255, 0, 0), (back_bg_x, back_bg_y, back_bg_width, back_bg_height),
                             2)  # Красный контур

            # Проверка клика на кнопку "Назад"
            if back_bg_x < mouse_x < back_bg_x + back_bg_width and back_bg_y < mouse_y < back_bg_y + back_bg_height:
                if pygame.mouse.get_pressed()[0]:
                    if current_time - self.last_click_time > self.click_delay:
                        self.show_options_menu = False
                        self.last_click_time = current_time  # Обновляем время последнего клика
                    return

        else:
            button_coords = []
            button_y_offset = 40

            for i, button_text in enumerate(self.button_texts):
                # Управление позицией кнопок главного меню с учетом смещения
                button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - self.background.get_width() // 2 + self.x_offset,
                    # Центр по оси X с учетом смещения
                    SCREEN_HEIGHT // 2 + i * (self.button_height + 20) + button_y_offset + self.y_offset,
                    # Позиция по оси Y с учетом смещения
                    self.background.get_width(),
                    self.background.get_height()
                )

                button_coords.append((button_rect, button_text))

                # Отображение прямоугольника для отладки
                pygame.draw.rect(self.screen, (255, 0, 0), button_rect, 2)  # Красный контур

            for button_rect, button_text in button_coords:
                if button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    if current_time - self.last_click_time > self.click_delay:
                        self.last_click_time = current_time  # Обновляем время последнего клика

                        # Обработчик команды для кнопки
                        if button_text == 'Продолжить':
                            pass
                        elif button_text == 'Начать игру':
                            self.start_game()
                        elif button_text == 'Выход':
                            self.quit_game()

                        self.execute_action(button_text)
                        return
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
        if not self.music_playing and not self.game_started:
            self.play_menu_music()
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


                    y_offset = 70

                    for i, button in enumerate(self.buttons):
                        surface.blit(self.background, (SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                                                       SCREEN_HEIGHT // 2 + i * (self.button_height + 20) - y_offset))

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for i, button in enumerate(self.buttons):
                        button_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - self.background.get_width() // 2,
                            SCREEN_HEIGHT // 2 + i * (self.button_height + 20) - y_offset,
                            self.background.get_width(),
                            self.background.get_height()
                        )

                        button_color = (255, 255, 255) if button_rect.collidepoint(mouse_x, mouse_y) else (0, 0, 255)
                        button_text = self.font.render(self.button_texts[i], True, button_color)
                        surface.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2,
                                                   SCREEN_HEIGHT // 2 + i * (self.button_height + 20) - y_offset))

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

        if button_text == self.button_texts[0]:  # Кнопка "Продолжить"
            pass  # Добавьте метод продолжения игры
        elif button_text == self.button_texts[1]:  # Кнопка "Начать игру"
            self.start_game()
        elif button_text == self.button_texts[2]:  # Кнопка "Настройки"
            self.show_options_menu = True
        elif button_text == self.button_texts[3]:  # Кнопка "Выход"
            self.quit_game()

    def update_button_texts(self):
        self.button_texts = [
            self.settings.get_text('continue'),
            self.settings.get_text('start_game'),
            self.settings.get_text('settings'),
            self.settings.get_text('exit')
        ]
        self.buttons = [self.font.render(text, True, (0, 0, 255)) for text in self.button_texts]

    def quit_game(self):
        pygame.quit()
        quit()

    def start_game(self):
        self.stop_menu_music()
        start_game_in_cabin(DISPLAYSURF)

    def display_options_menu(self, surface):
        option_texts = [
            self.settings.get_text('volume', volume=int(self.settings.volume * 100)),
            self.settings.get_text('change_language') + f": {self.settings.language.upper()}",
            self.settings.get_text('autosave', status='Включено' if self.settings.autosave else 'Выключено'),
            self.settings.get_text('difficulty', difficulty=self.settings.difficulty)
        ]

        mouse_x, mouse_y = pygame.mouse.get_pos()
        option_buttons = []

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

            if option_bg_x < mouse_x < option_bg_x + bg_width and option_bg_y < mouse_y < option_bg_y + bg_height:
                option_label = self.font.render(option_text, True, (255, 255, 255))
            surface.blit(option_label, (option_bg_x + 10, option_bg_y + 10))

        back_label = self.font.render(self.settings.get_text('back'), True, (0, 0, 255))
        back_text_width = back_label.get_width()
        back_text_height = back_label.get_height()

        back_bg_width = back_text_width + 45
        back_bg_height = back_text_height + 20
        back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
        back_bg_y = SCREEN_HEIGHT - back_bg_height - 360

        button_bg = pygame.transform.scale(self.background, (back_bg_width, back_bg_height))
        surface.blit(button_bg, (back_bg_x, back_bg_y))

        surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))

        if back_bg_x < mouse_x < back_bg_x + back_bg_width and back_bg_y < mouse_y < back_bg_y + back_bg_height:
            back_label = self.font.render(self.settings.get_text('back'), True, (255, 255, 255))
            surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))

    def set_language(self, language):
        self.settings.language = language

    def update_title_text(self):
        self.title_text = self.settings.get_text('title')


class Settings:
    def __init__(self, main_menu_instance):
        self.volume = 1.0
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fullscreen = False
        self.language = 'ru'
        self.autosave = True
        self.difficulty = 'Легко'

        self.settings_file = 'config/game_settings.json'
        self.text_file = f'localization/{self.language}.json'
        self.main_menu = main_menu_instance

        self.load_settings_from_json()
        self.load_texts_from_json()

    def load_texts_from_json(self):
        if os.path.exists(self.text_file):
            with open(self.text_file, mode='r', encoding='utf-8') as file:
                self.text_data = json.load(file)
        else:
            raise FileNotFoundError(f"Текстовый файл для языка {self.language} не найден.")

    def get_text(self, key, **kwargs):

        text = self.text_data.get(key, "")

        if 'status' in kwargs:
            if self.language == 'ru':
                status = 'Включено' if self.autosave else 'Выключено'
            else:
                status = 'Enabled' if self.autosave else 'Disabled'
            kwargs['status'] = status

        if 'difficulty' in kwargs:
            if self.language == 'ru':
                difficulty = self.difficulty
            else:
                difficulty_mapping = {
                    'Легко': 'Easy',
                    'Средне': 'Medium',
                    'Трудно': 'Hard'
                }
                difficulty = difficulty_mapping.get(self.difficulty, self.difficulty)
            kwargs['difficulty'] = difficulty

        return text.format(**kwargs)

    def save_settings_to_json(self):
        settings_data = {
            'volume': self.volume,
            'autosave': self.autosave,
            'difficulty': self.difficulty,
            'language': self.language
        }
        with open(self.settings_file, mode='w', encoding='utf-8') as file:
            json.dump(settings_data, file, ensure_ascii=False, indent=4)

    def load_settings_from_json(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, mode='r', encoding='utf-8') as file:
                settings_data = json.load(file)
                self.volume = settings_data.get('volume', 1.0)
                self.autosave = settings_data.get('autosave', True)
                self.difficulty = settings_data.get('difficulty', 'Легко')
                self.language = settings_data.get('language', 'ru')
                self.text_file = f'localization/{self.language}.json'
                self.load_texts_from_json()

    def change_language(self, new_language):
        self.language = new_language
        self.text_file = f'localization/{self.language}.json'
        self.load_texts_from_json()
        self.save_settings_to_json()
        self.main_menu.update_button_texts()
        self.main_menu.update_title_text()
        self.main_menu.show_main_menu = True

    def update_main_menu_button_texts(self):
        if hasattr(self, 'main_menu'):
            self.main_menu.update_button_texts()

    def change_volume(self, amount=0.1):
        self.volume = max(0.0, min(1.0, self.volume + amount))
        pygame.mixer.music.set_volume(self.volume)
        self.save_settings_to_json()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        pygame.display.set_mode(self.resolution, pygame.FULLSCREEN if self.fullscreen else 0)
        self.save_settings_to_json()

    def toggle_autosave(self):
        self.autosave = not self.autosave
        self.save_settings_to_json()

    def change_difficulty(self):
        difficulties = ['Легко', 'Средне', 'Трудно']
        current_index = difficulties.index(self.difficulty)
        next_index = (current_index + 1) % len(difficulties)
        self.difficulty = difficulties[next_index]
        self.save_settings_to_json()
