import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_FONT
from scripts.ui.dialog_box import DialogueBox
from scripts.ui.menu import Menu
from scripts.characters.player import Character
from scripts.scenes.save_load import save_game

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_FONT
from scripts.ui.dialog_box import DialogueBox
from scripts.ui.menu import Menu
from scripts.characters.player import Character
from scripts.scenes.save_load import save_game

class CollisionZone:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def check_collision(self, character_rect):

        if character_rect.colliderect(self.rect):
            if character_rect.bottom > self.rect.top and character_rect.top < self.rect.top:

                character_rect.bottom = self.rect.top
            elif character_rect.top < self.rect.bottom and character_rect.bottom > self.rect.bottom:

                character_rect.top = self.rect.bottom
            elif character_rect.right > self.rect.left and character_rect.left < self.rect.left:

                character_rect.right = self.rect.left
            elif character_rect.left < self.rect.right and character_rect.right > self.rect.right:

                character_rect.left = self.rect.right

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)

def start_game_in_cabin(screen, character_x=510, character_y=660, inventory=None, current_dialogue=0):
    clock = pygame.time.Clock()
    background = pygame.image.load('assets/locations/ship_room.png').convert()

    bg_width, bg_height = background.get_size()
    new_width = int(bg_width * 1.7)
    new_height = int(bg_height * 1.3)
    background = pygame.transform.scale(background, (new_width, new_height))
    x_offset = (SCREEN_WIDTH - new_width) // 2
    y_offset = (SCREEN_HEIGHT - new_height) // 2

    character = Character('assets/characters/character_sprite.png', character_x, character_y)


    bed_zone = CollisionZone(x_offset + 60, y_offset + 700, 290, 150, color=(255, 0, 0))
    table_zone = CollisionZone(x_offset + 1, y_offset + 30, 1800, 300, color=(0, 255, 0))
    crates_zone = CollisionZone(x_offset + 1375, y_offset + 700, 325, 325, color=(0, 0, 255))


    door_zone = CollisionZone(x_offset + 910, y_offset + 320, 90, 90, color=(255, 255, 0))
    shelf_zone = CollisionZone(x_offset + 1750, y_offset + 0, 420, 1700, color=(255, 165, 0))
    window_zone = CollisionZone(x_offset +20, y_offset +1450, 1725, 50, color=(0, 255, 255))
    cabinet_zone = CollisionZone(x_offset-400, y_offset + 0, 420, 1700, color=(255, 255, 255))

    alpha_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(255)
    fade_duration = 0.1
    fade_ticks = fade_duration * 60
    alpha_step = 255 / fade_ticks

    menu = Menu()
    dialogue_box = DialogueBox(DEFAULT_FONT, character)

    cursor_image = pygame.image.load('assets/images/cursor.png').convert_alpha()
    cursor_image = pygame.transform.scale(cursor_image, (14, 20))
    cursor_rect = cursor_image.get_rect()

    cursor_x = 60
    cursor_y = -60

    pygame.mouse.set_visible(False)

    if inventory is None:
        inventory = []
    if current_dialogue is None:
        current_dialogue = 1

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

        keys = pygame.key.get_pressed()
        character.update(keys)


        bed_zone.check_collision(character.rect)
        table_zone.check_collision(character.rect)
        crates_zone.check_collision(character.rect)
        door_zone.check_collision(character.rect)
        shelf_zone.check_collision(character.rect)
        window_zone.check_collision(character.rect)
        cabinet_zone.check_collision(character.rect)


        bed_zone.render(screen)
        table_zone.render(screen)
        crates_zone.render(screen)
        door_zone.render(screen)
        shelf_zone.render(screen)
        window_zone.render(screen)
        cabinet_zone.render(screen)

        character.render(screen)

        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {character.rect.x}, Y: {character.rect.y}", True, (255, 255, 255))
        screen.blit(coordinates_text, (10, 10))

        pygame.draw.circle(screen, (255, 0, 0), (character.rect.centerx, character.rect.centery), 5)

        if not menu.show_pause_menu:
            if current_dialogue <= 6:
                dialogue_box.update_text()
                dialogue_box.render(screen)

                if dialogue_box.current_dialogue == 6:
                    current_dialogue += 1

        if menu.show_pause_menu:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(30)
            screen.blit(fade_surface, (0, 0))
            menu.display(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_x, cursor_y = mouse_x, mouse_y
        cursor_rect.topleft = (cursor_x, cursor_y)

        screen.blit(cursor_image, cursor_rect)

        pygame.display.flip()
        clock.tick(60)
