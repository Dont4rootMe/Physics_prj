import pygame
import sys
from button import Button

AUTHORS_SCREEN = 1

class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        self.authors_button = Button(self, "Авторы", (520, 0), (200, 50))
        self.demonstration_button = Button(self, "Демонстрация", (210,0), (300, 50))
        self.screensaver_button = Button(self, "Заставка", (0, 0), (200, 50))

        self.buttons: list[Button] = [self.authors_button, self.demonstration_button, self.screensaver_button]

        self.bg_color = (230, 230, 230)

        self.cmc_logo = pygame.transform.scale(pygame.image.load("cmc_logo.jpg"), (50, 50))
        self.active_screen = None

    def run(self):
        """Запуск основного цикла игры."""
        while True:
        # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            self._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw_button()
        if self.active_screen == AUTHORS_SCREEN:
            self.screen.blit(self.cmc_logo, self.screen.get_rect().center)

        
    def _check_buttons(self, mouse_position):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_position):
                if button == self.screensaver_button:
                    self.active_screen = AUTHORS_SCREEN
                else:
                    self.active_screen = None


if __name__ == '__main__':
    app = App()
    app.run()