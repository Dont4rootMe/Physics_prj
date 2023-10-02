import pygame
import sys
from button import Button
from menu_screen import MenuScreen

class App:
    def __init__(self):
        pygame.init()
        print(pygame.font.get_fonts())
        self.screen = pygame.display.set_mode((1920, 1080))
        self.authors_button = Button(self, "Авторы", (520, 0), (200, 50))
        self.demonstration_button = Button(self, "Демонстрация", (210,0), (300, 50))
        self.screensaver_button = Button(self, "Заставка", (0, 0), (200, 50))
        self.menu_screen = MenuScreen(self)

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

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        if self.active_screen == AUTHORS_SCREEN:
            pass
        elif self.active_screen == MENU_SCREEN:
            self.menu_screen.draw()

        
    def _check_buttons(self, mouse_position):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_position):
                if button == self.screensaver_button:
                    self.active_screen = AUTHORS_SCREEN
                else:
                    self.active_screen = 1


if __name__ == '__main__':
    app = App()
    app.run()