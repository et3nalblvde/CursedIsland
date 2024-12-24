import pygame
from PIL import Image
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, DEFAULT_FONT

class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(DEFAULT_FONT, 60)
        self.title_text = self.font.render('Проклятый остров', True, WHITE)
        self.start_text = self.font.render('Нажмите Enter для продолжения', True, WHITE)

        self.button_texts = ['Начать игру', 'Настройки', 'Выход']
        self.buttons = [self.font.render(text, True, (0, 0, 255)) for text in self.button_texts]

        self.button_width = max(button.get_width() for button in self.buttons)
        self.button_height = self.buttons[0].get_height()

        self.background = pygame.image.load("assets/images/map.png")
        self.background = pygame.transform.scale(self.background, (self.button_width + 30, self.button_height + 10))
        self.frames = self.load_gif("assets/videos/sea.gif")
        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_delay = 0.05
        self.last_update = pygame.time.get_ticks()

        self.alpha = 255
        self.fade_duration = 2000
        self.fade_start_time = pygame.time.get_ticks()

        self.cursor = pygame.image.load("assets/images/cursor.png")
        self.cursor = pygame.transform.scale(self.cursor, (14, 20))
        self.cursor_rect = self.cursor.get_rect()

        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        self.show_main_menu = False

        self.selected_button = 0

    def load_gif(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = pygame.image.fromstring(gif.convert('RGB').tobytes(), gif.size, 'RGB')
            frames.append(frame_image)
        return frames

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
            if not self.show_main_menu:
                surface.blit(self.start_text, (SCREEN_WIDTH // 2 - self.start_text.get_width() // 2, SCREEN_HEIGHT // 2))
            else:
                surface.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, SCREEN_HEIGHT // 3))
                for i, button in enumerate(self.buttons):
                    surface.blit(self.background, (SCREEN_WIDTH // 2 - self.background.get_width() // 2, SCREEN_HEIGHT // 2 + i * self.button_height))

                for i, button in enumerate(self.buttons):
                    button_color = (0, 0, 255)
                    button_text = self.font.render(self.button_texts[i], True, button_color)
                    surface.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + i * self.button_height))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cursor_rect.topleft = (mouse_x, mouse_y)
        surface.blit(self.cursor, self.cursor_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.show_main_menu:
                        self.show_main_menu = True
                    else:
                        self.execute_action()
                elif event.key == pygame.K_DOWN and self.show_main_menu:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_UP and self.show_main_menu:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)

        if current_time - self.last_update > self.frame_delay * 1000:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % self.frame_count

        self.clock.tick(120)

        self.handle_mouse_click(mouse_x, mouse_y)

    def handle_mouse_click(self, mouse_x, mouse_y):
        for i, button in enumerate(self.buttons):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - self.button_width // 2, SCREEN_HEIGHT // 2 + i * self.button_height, self.button_width, self.button_height)
            if button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.selected_button = i
                    self.execute_action()

    def execute_action(self):
        if self.selected_button == 0:
            print("Начинаем игру...")
            self.start_game()
        elif self.selected_button == 1:
            print("Открываются настройки...")
            self.open_settings()
        elif self.selected_button == 2:
            print("Выход из игры...")
            self.quit_game()

    def quit_game(self):
        # Выход из игры
        print("Закрытие игры...")
        pygame.quit()
        quit()

    def start_game(self):
        pass # Пока не реализовано

    def open_settings(self):
        pass # Пока не реализовано
