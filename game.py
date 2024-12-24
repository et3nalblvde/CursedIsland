import pygame
from scripts import *
from __init__ import *
# Инициализация игры
pygame.init()

# Настройки экрана
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()

    # Создаем главное меню
    main_menu = MainMenu()

    # Игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Запускаем главное меню
        main_menu.display(DISPLAYSURF)

        # Обновляем экран
        pygame.display.update()

        # Поддерживаем 120 FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
