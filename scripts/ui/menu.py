import pygame
import json
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_FONT, FONT_SIZE, IMAGES_DIR


class Menu:
    def __init__(self):
        self.language_settings = self.load_game_settings()
        self.language = self.language_settings.get("language", "ru")
        self.font = pygame.font.Font(DEFAULT_FONT, FONT_SIZE * 2)
        self.load_text()
        self.selected_button = 0
        self.show_pause_menu = False
        self.exit_game = False
        self.alpha_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.alpha_surface.fill((0, 0, 0, 180))
        self.button_background = pygame.image.load(IMAGES_DIR + "map.png").convert_alpha()
        self.button_background = pygame.transform.scale(self.button_background, (400, 80))

        pygame.mouse.set_visible(False)

        self.ignore_next_click = False
        self.show_options_menu = False
        self.x_offset = 0
        self.y_offset = 0
        self.last_click_time = 0
        self.click_delay = 200
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.mixer.init()
        self.load_music()

    def load_music(self):

        pygame.mixer.music.load("audio/music/menu_theme.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.language_settings["volume"])

    def load_game_settings(self):
        try:
            with open("config/game_settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                return settings
        except FileNotFoundError:
            return {"language": "ru", "volume": 1.0, "autosave": False, "difficulty": "Средне"}
        except json.JSONDecodeError:
            return {"language": "ru", "volume": 1.0, "autosave": False, "difficulty": "Средне"}

    def load_text(self):
        with open(f"localization/{self.language}.json", "r", encoding="utf-8") as file:
            self.text_data = json.load(file)

        volume_text = self.text_data["settings_menu"]["volume"].format(
            volume=int(self.language_settings.get('volume', 1.0) * 100))
        change_language_text = f"{self.text_data.get('change_language', 'Смена языка')}: {self.language.upper()}"

        autosave_status_list = ["Выключено", "Включено"]
        autosave_status = autosave_status_list[int(self.language_settings.get('autosave', False))]
        autosave_text = self.text_data["settings_menu"]["autosave"].format(status=autosave_status)

        difficulty_status_list = ["Легко", "Средне", "Трудно"]
        difficulty_status = difficulty_status_list.index(self.language_settings.get('difficulty', 'Средне'))

        difficulty_text = self.text_data["settings_menu"]["difficulty"].format(
            difficulty=difficulty_status_list[difficulty_status])

        self.option_texts = [
            volume_text,
            change_language_text,
            autosave_text,
            difficulty_text
        ]
        self.buttons = [
            self.text_data["main_menu"]["continue"],
            self.text_data["main_menu"]["settings"],
            self.text_data["main_menu"]["exit"]
        ]
        self.back_label_text = self.text_data["back"]

    def handle_input(self, event):
        if self.ignore_next_click:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_pause_menu = not self.show_pause_menu
                self.show_options_menu = False
            if self.show_pause_menu:
                if event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                if event.key == pygame.K_RETURN:
                    if self.buttons[self.selected_button] == self.text_data["main_menu"]["continue"]:
                        self.show_pause_menu = False
                    elif self.buttons[self.selected_button] == self.text_data["main_menu"]["settings"]:
                        self.show_options_menu = True
                        self.ignore_next_click = True
                    elif self.buttons[self.selected_button] == self.text_data["main_menu"]["exit"]:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Если открыто меню настроек, игнорировать клики по главному меню
                if self.show_options_menu:
                    return

                for i, button in enumerate(self.buttons):
                    button_x = SCREEN_WIDTH // 2 - self.button_background.get_width() // 2 + self.x_offset
                    button_y = SCREEN_HEIGHT // 2 - (
                            len(self.buttons) * self.button_background.get_height()) // 2 + i * (
                                       self.button_background.get_height() + 50) + self.y_offset
                    if (button_x <= mouse_x <= button_x + self.button_background.get_width() and
                            button_y <= mouse_y <= button_y + self.button_background.get_height()):
                        if button == self.text_data["main_menu"]["continue"]:
                            self.show_pause_menu = False
                        elif button == self.text_data["main_menu"]["settings"]:
                            self.show_options_menu = True
                            self.ignore_next_click = True
                        elif button == self.text_data["main_menu"]["exit"]:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def display(self, screen):
        if self.show_options_menu:
            self.display_options_menu(screen)
        elif self.show_pause_menu:
            screen.blit(self.alpha_surface, (0, 0))
            y_offset = SCREEN_HEIGHT // 2 - (
                    len(self.buttons) * self.button_background.get_height()) // 2 + self.y_offset
            for i, button in enumerate(self.buttons):
                button_x = SCREEN_WIDTH // 2 - self.button_background.get_width() // 2 + self.x_offset
                button_y = y_offset + i * (self.button_background.get_height() + 30)

                screen.blit(self.button_background, (button_x, button_y))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (button_x <= mouse_x <= button_x + self.button_background.get_width() and
                        button_y <= mouse_y <= button_y + self.button_background.get_height()):
                    button_color = (255, 255, 255)
                elif i == self.selected_button:
                    button_color = (0, 0, 255)
                else:
                    button_color = (0, 0, 255)
                button_text = self.font.render(button, True, button_color)
                text_x = button_x + (self.button_background.get_width() - button_text.get_width()) // 2
                text_y = button_y + (self.button_background.get_height() - button_text.get_height()) // 2
                screen.blit(button_text, (text_x, text_y))

                pygame.draw.rect(screen, (255, 0, 0), (
                    button_x, button_y, self.button_background.get_width(), self.button_background.get_height()), 3)

    def update(self, screen, event, clock):
        self.handle_input(event)
        self.display(screen)
        clock.tick(120)

    def display_options_menu(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        option_buttons = []

        for i, option_text in enumerate(self.option_texts):
            option_label = self.font.render(option_text, True, (0, 0, 255))
            text_width = option_label.get_width()
            text_height = option_label.get_height()
            bg_width = text_width + 40
            bg_height = text_height + 20

            option_bg_x = SCREEN_WIDTH // 2 - bg_width // 2
            option_bg_y = SCREEN_HEIGHT // 3 + i * (bg_height + 30) + 30

            option_buttons.append((option_bg_x, option_bg_y, bg_width, bg_height))
            button_bg = pygame.transform.scale(self.button_background, (bg_width, bg_height))
            surface.blit(button_bg, (option_bg_x, option_bg_y))

            if option_bg_x < mouse_x < option_bg_x + bg_width and option_bg_y < mouse_y < option_bg_y + bg_height:
                option_label = self.font.render(option_text, True, (255, 255, 255))
            surface.blit(option_label, (option_bg_x + 10, option_bg_y + 10))

            pygame.draw.rect(surface, (255, 0, 0), (option_bg_x, option_bg_y, bg_width, bg_height), 3)

        volume_up_label = self.font.render("+", True, (0, 0, 255))
        volume_down_label = self.font.render("-", True, (0, 0, 255))
        volume_button_width = volume_up_label.get_width() + 20
        volume_button_height = volume_up_label.get_height() + 20

        volume_down_x = SCREEN_WIDTH // 2 - 150 - volume_button_width
        volume_down_y = SCREEN_HEIGHT // 3 + 30
        volume_up_x = SCREEN_WIDTH // 2 + 150
        volume_up_y = SCREEN_HEIGHT // 3 + 30

        volume_down_bg = pygame.transform.scale(self.button_background, (volume_button_width, volume_button_height))
        volume_up_bg = pygame.transform.scale(self.button_background, (volume_button_width, volume_button_height))

        surface.blit(volume_down_bg, (volume_down_x, volume_down_y))
        surface.blit(volume_up_bg, (volume_up_x, volume_up_y))

        surface.blit(volume_down_label, (volume_down_x + 10, volume_down_y + 10))
        surface.blit(volume_up_label, (volume_up_x + 10, volume_up_y + 10))

        pygame.draw.rect(surface, (255, 0, 0),
                         (volume_down_x, volume_down_y, volume_button_width, volume_button_height), 3)
        pygame.draw.rect(surface, (255, 0, 0), (volume_up_x, volume_up_y, volume_button_width, volume_button_height), 3)

        back_label = self.font.render(self.back_label_text, True, (0, 0, 255))
        back_text_width = back_label.get_width()
        back_text_height = back_label.get_height()

        back_bg_width = back_text_width + 45
        back_bg_height = back_text_height + 20
        back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
        back_bg_y = SCREEN_HEIGHT - back_bg_height - 360

        button_bg = pygame.transform.scale(self.button_background, (back_bg_width, back_bg_height))
        surface.blit(button_bg, (back_bg_x, back_bg_y))

        surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))

        pygame.draw.rect(surface, (255, 0, 0), (back_bg_x, back_bg_y, back_bg_width, back_bg_height), 3)

        self.handle_options_menu_click(mouse_x, mouse_y)

    def handle_options_menu_click(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time < self.click_delay:
            return

        option_buttons = []

        for i, option_text in enumerate(self.option_texts):
            option_label = self.font.render(option_text, True, (0, 0, 255))
            text_width = option_label.get_width()
            text_height = option_label.get_height()
            bg_width = text_width + 40
            bg_height = text_height + 20

            option_bg_x = SCREEN_WIDTH // 2 - bg_width // 2
            option_bg_y = SCREEN_HEIGHT // 3 + i * (bg_height + 30) + 30

            option_buttons.append((option_bg_x, option_bg_y, bg_width, bg_height, i))

            pygame.draw.rect(self.screen, (255, 0, 0), (option_bg_x, option_bg_y, bg_width, bg_height), 2)

            if option_bg_x < mouse_x < option_bg_x + bg_width and option_bg_y < mouse_y < option_bg_y + bg_height:
                if pygame.mouse.get_pressed()[0]:
                    if current_time - self.last_click_time > self.click_delay:
                        if i == 0:
                            self.change_volume(0.1)
                        elif i == 1:
                            new_language = 'en' if self.language == 'ru' else 'ru'
                            self.change_language(new_language)
                        elif i == 2:
                            self.toggle_autosave()
                        elif i == 3:
                            self.change_difficulty()
                        self.last_click_time = current_time

        volume_button_width = 60
        volume_button_height = 40
        volume_down_x = SCREEN_WIDTH // 2 - 150 - volume_button_width
        volume_down_y = SCREEN_HEIGHT // 3 + 30
        volume_up_x = SCREEN_WIDTH // 2 + 150
        volume_up_y = SCREEN_HEIGHT // 3 + 30

        if volume_down_x < mouse_x < volume_down_x + volume_button_width and volume_down_y < mouse_y < volume_down_y + volume_button_height:
            if pygame.mouse.get_pressed()[0]:
                if current_time - self.last_click_time > self.click_delay:
                    self.change_volume(-0.1)
                    self.last_click_time = current_time

        if volume_up_x < mouse_x < volume_up_x + volume_button_width and volume_up_y < mouse_y < volume_up_y + volume_button_height:
            if pygame.mouse.get_pressed()[0]:
                if current_time - self.last_click_time > self.click_delay:
                    self.change_volume(0.1)
                    self.last_click_time = current_time

        back_label = self.font.render(self.back_label_text, True, (0, 0, 255))
        back_text_width = back_label.get_width()
        back_text_height = back_label.get_height()

        back_bg_width = back_text_width + 45
        back_bg_height = back_text_height + 20
        back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
        back_bg_y = SCREEN_HEIGHT - back_bg_height - 360

        pygame.draw.rect(self.screen, (255, 0, 0), (back_bg_x, back_bg_y, back_bg_width, back_bg_height), 2)

        if back_bg_x < mouse_x < back_bg_x + back_bg_width and back_bg_y < mouse_y < back_bg_y + back_bg_height:
            if pygame.mouse.get_pressed()[0]:
                if current_time - self.last_click_time > self.click_delay:
                    self.show_options_menu = False
                    self.show_pause_menu = True
                    self.ignore_next_click = False
                    self.last_click_time = current_time

    def change_volume(self, amount=0.1):
        self.language_settings["volume"] = max(0.0, min(1.0, self.language_settings["volume"] + amount))
        pygame.mixer.music.set_volume(self.language_settings["volume"])
        self.save_settings()
        self.load_text()

    def change_language(self, new_language):
        self.language = new_language
        self.language_settings["language"] = new_language
        self.load_text()
        self.save_settings()

    def toggle_autosave(self):
        self.language_settings["autosave"] = not self.language_settings["autosave"]
        self.save_settings()
        self.load_text()

    def change_difficulty(self):
        difficulties = ['Легко', 'Средне', 'Трудно']
        current_index = difficulties.index(self.language_settings["difficulty"])
        next_index = (current_index + 1) % len(difficulties)
        self.language_settings["difficulty"] = difficulties[next_index]
        self.save_settings()
        self.load_text()

    def save_settings(self):
        with open("config/game_settings.json", "w", encoding="utf-8") as file:
            json.dump(self.language_settings, file, ensure_ascii=False, indent=4)
