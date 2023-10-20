import pygame
import sys
from button import Button
from graph import Graph
import time

class DemoScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.speed = 0.5
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)
        self.left_graph_position = (150, 150)
        self.right_graph_position = (1000, 150)
        self.graph_size = (650, 300)
        self.left_graph = Graph(app, [i for i in range(10)], self.left_graph_position, self.graph_size, True, str(1), (0, 250, 0, 10))
        self.right_graph = Graph(app, [i for i in range(10)], self.right_graph_position, self.graph_size, True, str(2), (250, 0, 0, 10))
        self.result_graph = None
        self.active_summing = False
        self.buttons = [Button(app, "Назад", (1300, 900), (300, 80)), Button(app, "Следующий шаг", (1300, 700), (300, 80))]
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw_button()
        if self.left_graph is not None:
            self.left_graph.draw_graph()
        if self.right_graph is not None:
            self.right_graph.draw_graph()
        if self.result_graph is not None:
            self.result_graph.draw_graph()
        
        if self.active_summing:
            self.summing_process()
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
                self._check_graphs(mouse_position)

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
                if index == 1:
                    self.start_new_lap()
                    
    
    def _check_graphs(self, mouse_position):
        if self.left_graph.active_filling:
            self.left_graph._check_mousebutton(mouse_position)
        if self.right_graph.active_filling:
            self.right_graph._check_mousebutton(mouse_position)
        if self.result_graph is None and not self.left_graph.active_filling and not self.right_graph.active_filling:
            self.active_summing = True
            
    def summing_process(self):
        if self.result_graph is None:
            #self.result_graph = self.left_graph + self.right_graph
            self.result_graph = Graph(self.app, sorted(list(set([i + j for i in self.left_graph.xticks for j in self.right_graph.xticks]))), 
                             (150, 600), (1000, 300), False, "суммы", 
                             (0, 0, 210))
        if not self.right_graph.reversed:
            self.right_graph.reverse()
        self.right_graph.move((self.right_graph.position[0] - self.speed, self.right_graph.position[1]))
        self.left_graph.move((self.left_graph.position[0] + self.speed, self.left_graph.position[1]))
        self.check_intersection()
        if self.right_graph.position[0] + self.right_graph.size[0] + 200 < self.left_graph.position[0]:
            self.active_summing = False
    
    def check_intersection(self):
        for index1, x1 in enumerate(self.left_graph.columns_x):
            for index2, x2 in enumerate(self.right_graph.columns_x):
                real_index = self.right_graph.number_of_values - index2 - 1
                if abs(x2 - x1) < self.speed and self.left_graph.columns_height[index1] * self.right_graph.columns_height[real_index]:
                    self.result_graph.columns_height[self.left_graph.xticks[index1] + self.right_graph.xticks[real_index]] += \
                    self.left_graph.columns_height[index1] * self.right_graph.columns_height[real_index]
                    time.sleep(0.5)
    
    def start_new_lap(self):
        if self.result_graph is None or sum(self.result_graph.columns_height) < 0.99:
            return
        self.right_graph = Graph(self.app, self.result_graph.xticks, self.right_graph_position, self.graph_size, False, "Новый", (250, 0, 0, 10))
        self.right_graph.columns_height = self.result_graph.columns_height
        self.right_graph.move(self.right_graph_position)
        self.right_graph.size = self.graph_size
        save_columns = self.left_graph.columns_height
        save_xticks = self.left_graph.xticks
        self.left_graph = Graph(self.app, self.result_graph.xticks, self.left_graph_position, self.graph_size, False, 
                                "1", self.left_graph.color)
        for index, column in enumerate(save_columns):
            self.left_graph.columns_height[save_xticks[index]] = column
        self.result_graph = None
    

                
