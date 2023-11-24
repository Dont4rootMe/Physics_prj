import pygame
import sys
from button import Button
from graph import Graph
import time
from option_box import OptionBox
from input_box import InputBox
import numpy as np

class DemoScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.scale = app.scale
        self.speed = 0.5
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, int(35 * self.app.scale))
        self.middle_font = pygame.font.SysFont(self.font, int(40 * self.app.scale), bold=True)
        self.big_font = pygame.font.SysFont(self.font, int(50 * self.app.scale))
        self.left_graph_position = (150 * self.app.scale, 150 * self.app.scale)
        self.right_graph_position = (1000 * self.app.scale, 150 * self.app.scale)
        self.graph_size = np.array((650, 300)) * self.scale
        self.left_graph = Graph(app, [i for i in range(10)], self.left_graph_position, self.graph_size, True, str(1), (0, 250, 0, 10))
        self.right_graph = Graph(app, [i for i in range(10)], self.right_graph_position, self.graph_size, True, str(2), (250, 0, 0, 10), right=True)
        self.result_graph = None
        self.active_summing = False
        self.step = 1
        self.limit = 100
        self.pause = False
        self.option_boxes_positions = ((500, 600), (1350, 600), (1600, 800))
        self.buttons = [Button(self.app, "Назад" if self.app.russian else "Back", (1300, 900), (250, 70), font_size=30), 
                        Button(self.app, "Следующий шаг" if self.app.russian else "Next step", (1300, 800), (250, 70), font_size=30),
                        Button(self.app, "Перезапустить" if self.app.russian else "Reload", (1600, 900), (250, 70), font_size=30),
                        Button(self.app, "Пауза" if self.app.russian else "Pause", (1600, 700), (250, 70), font_size=30),
                        Button(self.app, "Формула" if self.app.russian else "Formula", (1600, 600), (250, 70), font_size=30),
                        Button(self.app, "RUS/ENG", (1680, 1000), (170, 70), font_size=30)]
        self.option_boxes = [OptionBox(
                                        *self.option_boxes_positions[0], 200, 60, (240, 240, 240), (100, 200, 255), 25, 
                                        ["Шаблоны" if self.app.russian else "Templates", 
                                         "Равномерное" if self.app.russian else "Uniform",
                                         "Бернулли, p=0.1" if self.app.russian else "Bernulli, p=0.1",
                                         '"Полосатое"' if self.app.russian else '"Striped"', 
                                         '"Зубчатое"' if self.app.russian else '"toothed"'], app=self.app),
                                                        OptionBox(
                                        *self.option_boxes_positions[1], 200, 60, (240, 240, 240), (100, 200, 255), 25, 
                                        ["Шаблоны" if self.app.russian else "Templates", 
                                         "Равномерное" if self.app.russian else "Uniform",
                                         "Бернулли, p=0.1" if self.app.russian else "Bernulli, p=0.1",
                                         '"Полосатое"' if self.app.russian else '"Striped"', 
                                         '"Зубчатое"' if self.app.russian else '"toothed"'], app=self.app),
                                                        OptionBox(
                                        *self.option_boxes_positions[2], 250, 70, (240, 240, 240), (100, 200, 255), 30,
                                        ['Скорость' if self.app.russian else "Speed", 'x1', 'x2', 'x4', 'x8'], app=self.app, back=True)
                                    ]
        self.checkbox_text = self.little_font.render("Дублировать 1-е распределение:" if self.app.russian else "Duplicate 1-st distribution:", False, (0, 0, 0))
        self.checkbox2_text = self.little_font.render("Показать распределение Гаусса:" if self.app.russian else "Show Gauss distribution:", False, (0, 0, 0))
        self.input_boxes = [InputBox(700, 515, 140, 50, self.app) if self.app.russian else InputBox(600, 515, 140, 50, self.app), 
                InputBox(1550, 515, 140, 50, self.app) if self.app.russian else InputBox(1450, 515, 140, 50, self.app)]
        self.checkbox = Button(self.app, '✖', (1460, 685) if self.app.russian else (1330, 685), (60, 60), font_size=30, font='SegoeUISymbol')

        self.show_formula = False
        self.formula_image = pygame.transform.scale(pygame.image.load("CodeCogsEqn.png"), np.array((380, 100)) * self.scale)

        self.distr_text = self.little_font.render("Типовые распределения:" if self.app.russian else "Typical distributions:", False, (0, 0, 0))

        self.checkbox_2 = Button(self.app, '✖', (1100, 620), (60, 60), font_size=30, font='SegoeUISymbol')
        self.time_check = time.time()
        self.norm_img = pygame.transform.scale(pygame.image.load("norm.png"), np.array((420, 300)) * self.scale)
        self.show_norm = False

    def _update_screen(self):
        self.input_text_surface = self.little_font.render('Кол-во значений случайной величины:' if self.app.russian else "Number of random variable values:",  False, (0, 0, 0))
        self.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw_button()
        self.left_graph.draw_graph()
        if self.right_graph is not None:
            self.right_graph.draw_graph()
        if self.result_graph is not None:
            self.result_graph.draw_graph()

        if self.left_graph.active_filling:
            self.screen.blit(self.distr_text, np.array((100, 610)) * self.scale)
            self.screen.blit(self.input_text_surface, np.array((100, 520)) * self.scale)
            self.input_boxes[0].draw(self.app.screen)
        
        if self.right_graph.active_filling:
            self.screen.blit(self.distr_text, np.array((950, 610)) * self.scale)
            self.screen.blit(self.input_text_surface, np.array((950, 520)) * self.scale)
            self.screen.blit(self.checkbox_text, np.array((950, 700)) * self.scale)
            self.input_boxes[1].draw(self.app.screen)
            self.checkbox.draw_button()
        
        if self.result_graph:
            self.screen.blit(self.checkbox2_text, np.array((600, 630) if self.app.russian else (750, 630)) * self.scale)
            self.checkbox_2.draw_button()
        
        if self.show_formula:
            self.screen.blit(self.formula_image, np.array((1220, 585)) * self.scale)
        
        for index, graph in enumerate((self.left_graph, self.right_graph)):
            if graph.active_filling:
                self.option_boxes[index].draw(self.screen)
        self.step_text = self.little_font.render(f"Шаг: {self.step}" if self.app.russian else f"Step: {self.step}", False, (0, 0, 0))
        if (np.array(self.left_graph.columns_height) != 0).sum():
            self.limit = round(200 / (np.array(self.left_graph.columns_height) != 0).sum())
        self.step_left_text = self.little_font.render(f"Шагов доступно: {max(0, self.limit - self.step)}" if self.app.russian else f"Steps available: {max(0, 20 - self.step)}", False, (0, 0, 0))
        if self.result_graph:
            self.screen.blit(self.step_text, np.array((1600, 20)) * self.scale)
            self.screen.blit(self.step_left_text, np.array((1600, 60)) * self.scale)
        self.option_boxes[2].draw(self.screen)
        if self.show_norm:
            self.screen.blit(self.norm_img, np.array((440, 700)) * self.scale)

        if self.active_summing:
            self.summing_process()
        
    def _check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
                self._check_graphs(mouse_position)
                if self.right_graph.active_filling and self.checkbox.active:
                    self.right_graph.columns_height = self.left_graph.columns_height.copy()
                    self.right_graph._check_mousebutton(mouse_position)

            if self.left_graph.active_filling:
                response = self.input_boxes[0].handle_event(event)
                if response:
                    self.left_graph = Graph(self.app, [i for i in range(int(response))], self.left_graph_position, 
                                            self.graph_size, True, str(1), (0, 250, 0, 10))
                    if self.checkbox.active:
                        self.right_graph = Graph(self.app, [i for i in range(int(response))], self.right_graph_position, 
                                            self.graph_size, True, str(1), (250, 0, 0, 10), right=True)
                        self.right_graph._check_mousebutton((0, 0))

            if self.right_graph.active_filling:
                response = self.input_boxes[1].handle_event(event)
                if response:
                    self.right_graph = Graph(self.app, [i for i in range(int(response))], self.right_graph_position, 
                                            self.graph_size, True, str(1), (250, 0, 0, 10), right=True)
                    
                    
        self.speed = 1/4 if self.option_boxes[2].selected < 2 else (self.option_boxes[2].selected + 1) / 2 * (1.3 - self.step / self.limit)
        self.option_boxes[2].update(events)

        for index, graph in enumerate((self.left_graph, self.right_graph)):
            if graph.active_filling:
                self.option_boxes[index].update(events)
                if self.option_boxes[index].selected == 1:
                    graph.columns_height = [1 / len(graph.xticks) for i in range(len(graph.xticks))]
                    graph.active_filling = False
                elif self.option_boxes[index].selected == 2:
                    if index == 0:
                        self.left_graph = Graph(self.app, [0, 1], graph.position, graph.size, False, str(1), (0, 250, 0, 10))
                        self.left_graph.columns_height = [0.9, 0.1]
                        self.left_graph.active_filling = False
                    else:
                        self.right_graph = Graph(self.app, [0, 1], graph.position, graph.size, False, str(1), (250, 0, 0, 10), right=True)
                        self.right_graph.columns_height = [0.9, 0.1]
                        self.right_graph.active_filling = False
                elif self.option_boxes[index].selected == 3:
                    if index == 0:
                        self.left_graph = Graph(self.app, [i for i in range(10)], graph.position, graph.size, False, str(1), (0, 250, 0, 10))
                        self.left_graph.columns_height = [0.25, 0, 0, 0.25, 0, 0, 0.25, 0, 0, 0.25]
                        self.left_graph.active_filling = False
                    else:
                        self.right_graph = Graph(self.app, [i for i in range(10)], graph.position, graph.size, False, str(1), (250, 0, 0, 10), right=True)
                        self.right_graph.columns_height = [0.25, 0, 0, 0.25, 0, 0, 0.25, 0, 0, 0.25]
                        self.right_graph.active_filling = False
                elif self.option_boxes[index].selected == 4:
                    if index == 0:
                        self.left_graph = Graph(self.app, [i for i in range(4)], graph.position, graph.size, False, str(1), (0, 250, 0, 10))
                        self.left_graph.columns_height = [0.47, 0.03, 0.03, 0.47]
                        self.left_graph.active_filling = False
                    else:
                        self.right_graph = Graph(self.app, [i for i in range(4)], graph.position, graph.size, False, str(1), (250, 0, 0, 10), right=True)
                        self.right_graph.columns_height = [0.47, 0.03, 0.03, 0.47]
                        self.right_graph.active_filling = False
                if graph == self.left_graph and self.checkbox.active:
                    self.right_graph.xticks = self.left_graph.xticks
                    self.right_graph.columns_height = self.left_graph.columns_height.copy()
                    self.right_graph.active_filling = sum(self.right_graph.columns_height) < 0.999
        if self.result_graph is None and not self.left_graph.active_filling and not self.right_graph.active_filling:
            self.active_summing = True
        
    
    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
                if index == 1 and self.step < self.limit:
                    self.start_new_lap()
                if index == 2:
                    self.reset()
                if index == 3:

                    self.pause = not button.active
                    button.active = not button.active
                    if button.active:
                        button.button_color = (100, 200, 255)
                    else:
                        button.button_color = (230, 230, 230)
                    button._prep_msg('Пауза')
                if index == 4:
                    self.show_formula = not self.show_formula
                if index == 5:
                    self.app.russian = not self.app.russian
                    self.buttons = [Button(self.app, "Назад" if self.app.russian else "Back", (1300, 900), (250, 70), font_size=30), 
                        Button(self.app, "Следующий шаг" if self.app.russian else "Next step", (1300, 800), (250, 70), font_size=30),
                        Button(self.app, "Перезапустить" if self.app.russian else "Reload", (1600, 900), (250, 70), font_size=30),
                        Button(self.app, "Пауза" if self.app.russian else "Pause", (1600, 700), (250, 70), font_size=30),
                        Button(self.app, "Формула" if self.app.russian else "Formula", (1600, 600), (250, 70), font_size=30),
                        Button(self.app, "RUS/ENG", (1680, 1000), (170, 70), font_size=30)]
                    self.option_boxes = [OptionBox(
                                        *self.option_boxes_positions[0], 200, 60, (240, 240, 240), (100, 200, 255), 25, 
                                        ["Шаблоны" if self.app.russian else "Templates", 
                                         "Равномерное" if self.app.russian else "Uniform",
                                         "Бернулли, p=0.1" if self.app.russian else "Bernulli, p=0.1",
                                         '"Полосатое"' if self.app.russian else '"Striped"', 
                                         '"Зубчатое"' if self.app.russian else '"toothed"'], app=self.app),
                                                        OptionBox(
                                        *self.option_boxes_positions[1], 200, 60, (240, 240, 240), (100, 200, 255), 25, 
                                        ["Шаблоны" if self.app.russian else "Templates", 
                                         "Равномерное" if self.app.russian else "Uniform",
                                         "Бернулли, p=0.1" if self.app.russian else "Bernulli, p=0.1",
                                         '"Полосатое"' if self.app.russian else '"Striped"', 
                                         '"Зубчатое"' if self.app.russian else '"toothed"'], app=self.app),
                                                        OptionBox(
                                        *self.option_boxes_positions[2], 250, 70, (240, 240, 240), (100, 200, 255), 30,
                                        ['Скорость' if self.app.russian else "Speed", 'x1', 'x2', 'x4', 'x8'], app=self.app, back=True)
                                    ]
                    self.checkbox_text = self.little_font.render("Дублировать 1-е распределение:" if self.app.russian else "Duplicate 1-st distribution:", False, (0, 0, 0))
                    self.checkbox2_text = self.little_font.render("Показать распределение Гаусса:" if self.app.russian else "Show Gauss distribution:", False, (0, 0, 0))
                    self.input_boxes = [InputBox(700, 515, 140, 50, self.app) if self.app.russian else InputBox(600, 515, 140, 50, self.app), 
                            InputBox(1550, 515, 140, 50, self.app) if self.app.russian else InputBox(1450, 515, 140, 50, self.app)]
                    self.checkbox = Button(self.app, '✖', (1460, 685) if self.app.russian else (1330, 685), (60, 60), font_size=30, font='SegoeUISymbol')
                    self.distr_text = self.little_font.render("Типовые распределения:" if self.app.russian else "Typical distributions:", False, (0, 0, 0))

        if self.checkbox.rect.collidepoint(mouse_position):
            if not self.checkbox.active:
                self.checkbox._prep_msg("✓")
                self.right_graph.xticks = self.left_graph.xticks
                self.right_graph.columns_height = self.left_graph.columns_height
                self.right_graph.active_filling = sum(self.right_graph.columns_height) < 0.999
            else:
                self.checkbox._prep_msg("✖")
            self.checkbox.active = not self.checkbox.active
        
        
        if self.checkbox_2.rect.collidepoint(mouse_position):
            if not self.checkbox_2.active:
                self.checkbox_2._prep_msg("✓")
                self.show_norm = True
            else:
                self.checkbox_2._prep_msg("✖")
                self.show_norm = False
            self.checkbox_2.active = not self.checkbox_2.active
                    
    
    def _check_graphs(self, mouse_position):
        if self.left_graph.active_filling:
            self.left_graph._check_mousebutton(mouse_position)
        if self.right_graph.active_filling:
            self.right_graph._check_mousebutton(mouse_position)
        if self.result_graph is None and not self.left_graph.active_filling and not self.right_graph.active_filling:
            self.active_summing = True
            
    def summing_process(self):
        if time.time() - self.time_check < min(2, 1 / 4 / self.speed ** 2):
            return
        self.summed = set()
        if self.result_graph is None:
            col_height = max(max(self.left_graph.columns_height), max(self.right_graph.columns_height))
            for graph in (self.left_graph, self.right_graph):
                save_cols = graph.columns_height.copy()
                if graph == self.left_graph:
                    self.left_graph = Graph(self.app, graph.xticks.copy(), graph.position, graph.size,
                                        False, graph.name, graph.color, col_height)
                    self.left_graph.columns_height = save_cols
                else:
                    self.right_graph = Graph(self.app, graph.xticks.copy(), graph.position, graph.size,
                                        False, graph.name, graph.color, col_height, right=True)
                    self.right_graph.columns_height = save_cols
            self.result_graph = self.build_result_graph_plot()
            self._update_screen()
            pygame.display.flip()
            time.sleep(1)
        if not self.right_graph.reversed:
            self.right_graph.reverse()
        self.right_graph.move((self.right_graph.position[0] - self.speed * (not self.pause), self.right_graph.position[1]))
        self.left_graph.move((self.left_graph.position[0] + self.speed * (not self.pause), self.left_graph.position[1]))
        self.check_intersection()
        if self.right_graph.position[0] + self.right_graph.size[0] + 200 * self.scale < self.left_graph.position[0]:
            self.active_summing = False
    
    def build_result_graph_plot(self):
        distribution = self.build_distribution()
        return Graph(self.app, list(range(0, max(distribution.keys()) + 1)), 
                             np.array((150, 700)) * self.scale, np.array((1000, 300)) * self.scale, False, "суммы" if self.app.russian else "of sum", 
                             (100, 100, 100), height=max(distribution.values()), result=True)

    def build_distribution(self):
        distribution = dict()
        for i in self.left_graph.xticks:
            for j in self.right_graph.xticks:
                if self.left_graph.columns_height[i] * self.right_graph.columns_height[j] == 0:
                    continue
                if i + j in distribution.keys():
                    distribution[i + j] += self.left_graph.columns_height[i] * self.right_graph.columns_height[j]
                else:
                    distribution[i + j] = self.left_graph.columns_height[i] * self.right_graph.columns_height[j]
        return distribution

    def check_intersection(self):
        found = False
        for index1, x1 in enumerate(self.left_graph.columns_x):
            for index2, x2 in enumerate(self.right_graph.columns_x):
                real_index = self.right_graph.number_of_values - index2 - 1
                if abs(x2 - x1) <= self.speed and (index1, real_index) not in self.summed and \
                    self.left_graph.columns_height[index1] * self.right_graph.columns_height[real_index]:
                    found = True
                    delta = abs(x2 - x1)
                    self.result_graph.columns_height[self.left_graph.xticks[index1] + self.right_graph.xticks[real_index]] += \
                    self.left_graph.columns_height[index1] * self.right_graph.columns_height[real_index]
                    self.summed.add((index1, real_index))
        if found:
            self.left_graph.move((self.left_graph.position[0] + delta, self.left_graph.position[1]))
            self._update_screen()
            pygame.display.flip()
            self.time_check = time.time()


    def start_new_lap(self):
        if self.result_graph is None or sum(self.result_graph.columns_height) < 0.99:
            return
        self.step += 1
        self.right_graph = Graph(self.app, self.result_graph.xticks, self.right_graph_position, self.graph_size, False, "суммы" if self.app.russian else "of sum", (250, 0, 0, 10), right=True)
        self.right_graph.columns_height = self.result_graph.columns_height
        self.right_graph.move(self.right_graph_position)
        self.right_graph.size = self.graph_size
        save_columns = self.left_graph.columns_height
        save_xticks = self.left_graph.xticks
        self.left_graph = Graph(self.app, self.result_graph.xticks, self.left_graph_position, self.graph_size, False, 
                                "1", self.left_graph.color)
        for index, column in enumerate(save_columns):
            if column != 0:
                self.left_graph.columns_height[save_xticks[index]] = column
        self.result_graph = None
    
    def reset(self):
        self.step = 1
        self.left_graph = Graph(self.app, [i for i in range(10)], self.left_graph_position, self.graph_size, True, str(1), (0, 250, 0, 10))
        self.right_graph = Graph(self.app, [i for i in range(10)], self.right_graph_position, self.graph_size, True, str(2), (250, 0, 0, 10), right=True)
        self.result_graph = None
        self.active_summing = False
        for box in self.option_boxes:
            box.selected = 0
