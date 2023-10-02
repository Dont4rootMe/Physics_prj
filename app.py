import pygame
import sys
from button import Button
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.authors_button = Button(self, "Авторы", (520, 0), (200, 50))
        self.demonstration_button = Button(self, "Демонстрация", (210,0), (300, 50))
        self.screensaver_button = Button(self, "Заставка", (0, 0), (200, 50))
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.buttons: list[Button] = [self.authors_button, self.demonstration_button, self.screensaver_button]

        self.active_screen = self.menu_screen

    def run(self):
        """Запуск основного цикла игры."""
        while True:
        # Отслеживание событий клавиатуры и мыши.
            self.active_screen._check_events()
            self.active_screen._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()