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
        self.cursor = pygame.image.load(IMAGES_DIR + "cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (14, 20))
        self.cursor_width, self.cursor_height = self.cursor.get_size()
        self.ignore_next_click = False
        self.show_options_menu = False
        self.x_offset = 0
        self.y_offset = 0

    def load_game_settings(self):
        """Загружаем настройки игры, включая язык и другие параметры."""
        try:
            with open("config/game_settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                return settings
        except FileNotFoundError:
            return {"language": "ru", "volume": 1.0, "autosave": False, "difficulty": "Средне"}
        except json.JSONDecodeError:
            return {"language": "ru", "volume": 1.0, "autosave": False, "difficulty": "Средне"}

    def load_text(self):
        """Загружаем локализованные строки из JSON-файла."""
        try:
            with open(f"localization/{self.language}.json", "r", encoding="utf-8") as file:
                self.text_data = json.load(file)
            self.buttons = [
                self.text_data["main_menu"]["continue"],
                self.text_data["main_menu"]["settings"],
                self.text_data["main_menu"]["exit"]
            ]
        except FileNotFoundError:
            self.buttons = ["Continue", "Settings", "Exit"]
        except json.JSONDecodeError:
            self.buttons = ["Continue", "Settings", "Exit"]

    def handle_input(self, event):
        """Обрабатываем ввод с клавиатуры и мыши."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_pause_menu = not self.show_pause_menu
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
                    elif self.buttons[self.selected_button] == self.text_data["main_menu"]["exit"]:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    button_x = SCREEN_WIDTH // 2 - self.button_background.get_width() // 2 + self.x_offset
                    button_y = SCREEN_HEIGHT // 2 - (len(self.buttons) * self.button_background.get_height()) // 2 + i * (
                                self.button_background.get_height() + 50) + self.y_offset
                    if (button_x <= mouse_x <= button_x + self.button_background.get_width() and
                            button_y <= mouse_y <= button_y + self.button_background.get_height()):
                        if button == self.text_data["main_menu"]["continue"]:
                            self.show_pause_menu = False
                        elif button == self.text_data["main_menu"]["settings"]:
                            self.show_options_menu = True
                        elif button == self.text_data["main_menu"]["exit"]:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def display(self, screen):
        if self.show_options_menu:
            self.display_options_menu(screen)
        elif self.show_pause_menu:
            screen.blit(self.alpha_surface, (0, 0))
            y_offset = SCREEN_HEIGHT // 2 - (len(self.buttons) * self.button_background.get_height()) // 2 + self.y_offset
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

            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(self.cursor, (mouse_x - self.cursor_width // 2, mouse_y - self.cursor_height // 2))

    def update(self, screen, event, clock):

        self.handle_input(event)
        self.display(screen)
        clock.tick(120)

    def display_options_menu(self, surface):

        volume = self.language_settings.get("volume", 1.0)
        autosave = self.language_settings.get("autosave", False)
        difficulty = self.language_settings.get("difficulty", "Средне")


        option_texts = [
            f"Звук: {int(volume * 100)}%",
            f"{self.text_data.get('change_language', 'Смена языка')}: {self.language.upper()}",
            f"Автосохранение: {'Включено' if autosave else 'Выключено'}",
            f"Сложность: {difficulty}"
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
            button_bg = pygame.transform.scale(self.button_background, (bg_width, bg_height))
            surface.blit(button_bg, (option_bg_x, option_bg_y))


            if option_bg_x < mouse_x < option_bg_x + bg_width and option_bg_y < mouse_y < option_bg_y + bg_height:
                option_label = self.font.render(option_text, True, (255, 255, 255))
            surface.blit(option_label, (option_bg_x + 10, option_bg_y + 10))


        back_label = self.font.render(self.text_data["back"], True, (0, 0, 255))
        back_text_width = back_label.get_width()
        back_text_height = back_label.get_height()

        back_bg_width = back_text_width + 45
        back_bg_height = back_text_height + 20
        back_bg_x = SCREEN_WIDTH // 2 - back_bg_width // 2
        back_bg_y = SCREEN_HEIGHT - back_bg_height - 360

        button_bg = pygame.transform.scale(self.button_background, (back_bg_width, back_bg_height))
        surface.blit(button_bg, (back_bg_x, back_bg_y))

        surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))

        if back_bg_x < mouse_x < back_bg_x + back_bg_width and back_bg_y < mouse_y < back_bg_y + back_bg_height:
            back_label = self.font.render(self.text_data["back"], True, (255, 255, 255))
            surface.blit(back_label, (back_bg_x + 10, back_bg_y + 10))


        surface.blit(self.cursor, (mouse_x - self.cursor_width // 2, mouse_y - self.cursor_height // 2))

