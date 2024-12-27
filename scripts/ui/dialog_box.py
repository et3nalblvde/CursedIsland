import pygame
import json


class DialogueBox:
    def __init__(self, font, display_dialogues=True):
        self.font = pygame.font.Font(font, 48)
        self.display_dialogues =display_dialogues

        self.language = self.load_language_setting()

        self.dialogues = self.load_dialogues()

        self.current_dialogue = -1
        self.text_speed = 2

        self.text_progress = 0
        self.dialogue_text = ""
        self.is_typing = False
        self.typewriter_sound = pygame.mixer.Sound('audio/sounds/typewriter.wav')

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
                self.dialogue_text = f"{self.dialogues[self.current_dialogue]['character']}: "
                self.dialogue_text += ""
                self.current_dialogue += 1
