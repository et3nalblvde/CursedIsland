import pygame
pygame.init()
GAME_TITLE = "Проклятый остров"
FPS = 120

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

FULLSCREEN = False


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


ASSETS_DIR = "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
AUDIO_DIR = ASSETS_DIR + "audio/"
FONTS_DIR = ASSETS_DIR + "fonts/"
VIDEOS_DIR = ASSETS_DIR + "videos/"

DEFAULT_FONT = FONTS_DIR + "Main_menu.ttf"
FONT_SIZE = 24
