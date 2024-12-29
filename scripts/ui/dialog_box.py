import pygame
import json


class DialogueBox:
    def __init__(self, font, display_dialogues=True):
        self.font = pygame.font.Font(font, 48)
        self.display_dialogues = display_dialogues

        self.language = self.load_language_setting()
        self.dialogues = self.load_dialogues()

        self.current_dialogue = -1
        self.text_speed = 2

        self.text_progress = 0
        self.dialogue_text = ""
        self.is_typing = False
        self.typewriter_sound = pygame.mixer.Sound('audio/sounds/typewriter.wav')

        self.dialogue_box_sprite = pygame.image.load('assets/images/dialog_box.png')
        self.original_width, self.original_height = self.dialogue_box_sprite.get_size()
        self.new_width = 1730
        self.new_height = 400
        self.dialogue_box_sprite = pygame.transform.scale(
            self.dialogue_box_sprite, (self.new_width, self.new_height)
        )
        self.dialogue_box_rect = self.dialogue_box_sprite.get_rect()
        self.dialogue_box_rect.topleft = (415, 1175)

        self.character_name_position = (self.dialogue_box_rect.x + 110, self.dialogue_box_rect.y + 40)
        self.text_position = (self.dialogue_box_rect.x + 30, self.dialogue_box_rect.y + 120)

        self.character_name_x = self.character_name_position[0]
        self.character_name_y = self.character_name_position[1]
        self.text_x = self.text_position[0]
        self.text_y = self.text_position[1]

        self.character_name_displayed = False

        self.max_text_width = self.new_width - 130

    def set_character_name_position(self, x, y):
        self.character_name_x = x
        self.character_name_y = y

    def set_text_position(self, x, y):
        self.text_x = x
        self.text_y = y

    def load_language_setting(self):
        with open('config/game_settings.json', 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)
        return settings.get("language", "ru")

    def load_dialogues(self):
        if self.language == "en":
            return self.load_dialogues_from_file("eng.json")
        else:
            return self.load_dialogues_from_file("ru.json")

    def load_dialogues_from_file(self, file_name):
        with open(f'dialogues/{file_name}', 'r', encoding='utf-8') as f:
            dialogues = json.load(f)["dialogs"]
        return dialogues

    def update_text(self):
        if self.is_typing:
            if self.text_progress < len(self.dialogues[self.current_dialogue]["text"]):
                self.dialogue_text += self.dialogues[self.current_dialogue]["text"][self.text_progress]
                self.text_progress += 1
                if self.text_progress % self.text_speed == 0:
                    self.typewriter_sound.play()
            else:
                self.is_typing = False
        else:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.is_typing = True
                self.text_progress = 0
                self.dialogue_text = ""
                self.current_dialogue += 1
                self.character_name_displayed = False

    def render(self, screen):
        if self.display_dialogues and self.current_dialogue >= 0:
            screen.blit(self.dialogue_box_sprite, self.dialogue_box_rect)

            character_name = self.dialogues[self.current_dialogue]['character']
            character_name_surface = self.font.render(character_name, True, (255, 255, 0))
            screen.blit(character_name_surface, (self.character_name_x, self.character_name_y))
            self.character_name_displayed = True

            words = self.dialogue_text.split(" ")
            lines = []
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                text_surface = self.font.render(test_line, True, (255, 255, 255))
                if text_surface.get_width() <= self.max_text_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            current_y = self.text_y
            for line in lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (self.text_x, current_y))
                current_y += self.font.get_height()
