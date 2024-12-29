import json
import pygame
class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, speed=5, scale_factor=0.5, health=100):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()


        new_width = int(self.image.get_width() * scale_factor - 50)
        new_height = int(self.image.get_height() * scale_factor - 60)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

    def render(self, screen):

        screen.blit(self.image, self.rect)

    def save_game(self, file_path="config/save_game.json"):

        game_data = {
            "character": {
                "x": self.rect.x,
                "y": self.rect.y,
                "health": self.health
            }
        }


        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(game_data, file, ensure_ascii=False, indent=4)

        print(f"Игра сохранена! Координаты персонажа: X={self.rect.x}, Y={self.rect.y}, Здоровье={self.health}")
