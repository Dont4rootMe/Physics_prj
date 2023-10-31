import pygame
import sys
from button import Button
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen
class App:
    def __init__(self):
        pygame.init()
        self.scale = pygame.display.Info().current_w / 1920
        self.screen = pygame.display.set_mode((1920 * self.scale, 1080 * self.scale))
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.demo_screen = DemoScreen(self)

        self.active_screen = self.menu_screen
        print(pygame.display.get_surface().get_size())

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