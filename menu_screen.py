import pygame
import sys
from button import Button

class MenuScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)
        self.msu_name = "Московский Государственный Университет им. М.В. Ломоносова"
        self.faculty_name = "Факультет вычислительной математики и кибернетики"
        self.demonstration_label = "Компьютерная демонстрация по курсу"
        self.subject_name = "Статистическая физика"
        self.demonstration_name = "Построение распределения вероятностей"
        self.demonstration_name_2 = "суммы случайных величин"
        self.strings = [self.msu_name, self.faculty_name, self.demonstration_label, self.subject_name,
                        self.demonstration_name, self.demonstration_name_2]
        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(self.middle_font.render(string, False, (0, 0, 0)))
            elif index < 4:
                self.strings_surfaces.append(self.little_font.render(string, False, (0, 0, 0)))
            else:
                self.strings_surfaces.append(self.big_font.render(string, False, (0, 0, 0)))
        self.positions = [(400, 100), (500, 150), (700, 250), (800, 300), (550, 400), (670, 470)]
        self.cmc_logo = pygame.transform.scale(pygame.image.load("cmc_logo.jpg"), (140, 140))
        self.msu_logo = pygame.transform.scale(pygame.image.load("msu_logo.jpg"), (150, 150))
        self.buttons = [Button(app, "Демонстрация", (750, 600), (400, 80)), Button(app, "Теория", (750, 700), (400, 80)),
                        Button(app, "Авторы", (750, 800), (400, 80)), Button(app, "Выход", (750, 900), (400, 80))]
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.positions[index])
        self.screen.blit(self.cmc_logo, (1600, 80))
        self.screen.blit(self.msu_logo, (180, 80))
        for button in self.buttons:
            button.draw_button()
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
    
    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 2:
                    self.app.active_screen = self.app.authors_screen
                elif index == 3:
                    sys.exit()