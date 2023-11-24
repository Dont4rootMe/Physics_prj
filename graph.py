import pygame
import numpy as np
class Graph:
    def __init__(self, app, values, position, size, active_filling, name, color, height=1, right=False, result=False) -> None:
        self.app = app
        self.color = color
        self.screen = app.screen
        self.scale = app.scale
        self.position = position
        self.font = 'Corbel'
        self.graph_font = pygame.font.SysFont('couriernew', int(30 * self.scale), bold=True)
        self.size = size
        self.number_of_values = len(values)
        self.active_filling = active_filling
        self.active_moving = False
        self.name = name
        self.reversed = False
        if right:
            self.xticks_color = (150, 0, 0)
        elif result:
            self.xticks_color = (0, 0, 0)
        else:
            self.xticks_color = (0, 150, 0)
        self.little_font = pygame.font.SysFont(self.font, int(40 * self.scale))
        self.middle_font = pygame.font.SysFont(self.font, int(50 * self.scale), bold=True)
        self.y_axis_coords = (self.position[0], self.position[1] - 20)
        self.x_axis_coords = (self.position[0], self.position[1] + self.size[1])
        self.vertical_delimeters_coords = [(self.position[0] + i * self.size[0] / self.number_of_values, self.position[1]) 
                                           for i in range(1, self.number_of_values + 1)]
        
        self.y_axis = pygame.Rect(*self.y_axis_coords, 5, self.size[1] + 20)
        self.x_axis = pygame.Rect(*self.x_axis_coords, self.size[0] + 50, 5)
        self.xticks = values
        self.height = height
        self.yticks = []
        for i in range(6):
            self.yticks.append(str(round(i * (height / 5), 2)))
        self.number_of_labels = 20
        self.step = max(1, self.number_of_values // self.number_of_labels + (self.number_of_values % self.number_of_labels != 0))
        self.labels = [ i for i in range(0, self.number_of_values, self.step)]
        self.xticks_surfaces = [pygame.transform.rotate(self.graph_font.render(str(self.xticks[i]), False, self.xticks_color), -90)
                                for i in self.labels]
        self.yticks_surfaces = [self.little_font.render(str(tick) + '-', False, (0, 0, 0)) for tick in self.yticks]
        self.arrow_surfaces = [self.middle_font.render(arrow, False, (0, 0, 0)) for arrow in ['>', '^']]
        self.vertical_delimeters = []
        self.horizontal_delimeters = []
        self.text_positions = [(self.position[0], self.position[1] - 70)]
        self.columns_height = [0] * self.number_of_values
        for i in range(self.number_of_values):
            self.vertical_delimeters.append(pygame.Rect(*self.vertical_delimeters_coords[i], 1, self.size[1]))
        self.yticks_position = [self.position[0] - (65 if len(tick) == 3 else 80) * self.scale for tick in self.yticks]
        self.arrows_position = [(self.position[0] + self.size[0] + 30 / self.scale, self.position[1] + self.size[1] - 21.25 * self.scale), (self.position[0] - 11 * self.scale, self.position[1] - 30 * self.scale)]
        self.columns_x = [self.position[0] + index * self.size[0] / self.number_of_values for index in range(self.number_of_values)]

    def draw_graph(self):
        strings_surfaces = []
        strings = []
        if self.active_filling:
            strings.append(f"Гистограмма {self.name}. Задайте распределение" if self.app.russian else f"Histogram {self.name}. Enter distribution:")
        else:
            strings.append(f"Гистограмма {self.name}." if self.app.russian else f"Histogram {self.name}")
        for string in strings:
            strings_surfaces.append(self.little_font.render(string, False, (0, 0, 0)))
        for index, surface in enumerate(strings_surfaces):
            self.screen.blit(surface, self.text_positions[index])
        for index, surface in enumerate(self.xticks_surfaces if not self.reversed else reversed(self.xticks_surfaces)):
            self.screen.blit(surface, (self.columns_x[index * self.step] + 0.5 * (self.size[0] / self.number_of_values - surface.get_rect().w), 
                                       self.position[1] + self.size[1] + 15 + (40) * (self.color == (250, 0, 0, 10) and self.app.active_screen.active_summing) * self.scale))

        for index, surface in enumerate(self.yticks_surfaces):
            self.screen.blit(surface, (self.yticks_position[index], self.position[1] + self.size[1] - 15 - index * self.size[1] // 5))
        
        for index, surface in enumerate(self.arrow_surfaces):
            self.screen.blit(surface, self.arrows_position[index])

        self.screen.fill((230, 230, 230), pygame.Rect(*(self.position[0], self.position[1] + sum(self.columns_height) * self.size[1]), self.size[0], (1 - sum(self.columns_height)) * self.size[1]))
        
        if self.active_filling:
            for delimiter in self.vertical_delimeters:
                self.screen.fill((200, 200, 200), delimiter)
        
        for index, column_height in enumerate(self.columns_height if not self.reversed else reversed(self.columns_height)):
            position = (self.columns_x[index], self.position[1] + self.size[1] - column_height * self.size[1] / self.height)
            size = (self.size[0] / self.number_of_values, column_height * self.size[1] / self.height)
            self.screen.fill(self.color, pygame.Rect(*position, *size), pygame.BLEND_RGBA_MULT)
            pygame.draw.rect(self.app.screen, (0, 0, 0), [*position, *size], 1)
        
        self.screen.fill((0,0,0),self.x_axis)
        self.screen.fill((0,0,0),self.y_axis)

    
    def _check_mousebutton(self, mouse_position):
        if self.position[0] < mouse_position[0] < self.position[0] + self.size[0] and \
               self.position[1] < mouse_position[1] < self.position[1] + self.size[1]:
                column_index = (mouse_position[0] - self.position[0]) // (self.size[0] // self.number_of_values)
                self.columns_height[int(column_index)] = min(1 - (mouse_position[1] - self.position[1]) / self.size[1], 1 - sum(self.columns_height))
        self.active_filling = sum(self.columns_height) < 1
                
    def move(self, position):
        delta = (position[0] - self.position[0], position[1] - self.position[1])
        self.position = position
        self.update_coords(delta)
        self.y_axis = pygame.Rect(*self.y_axis_coords, 5, self.size[1] + 20)
        self.x_axis = pygame.Rect(*self.x_axis_coords, self.size[0] + 50, 5)
        self.vertical_delimeters = []
        self.horizontal_delimeters = []
        self.text_positions = [(self.position[0], self.position[1] - 70)]
        for i in range(self.number_of_values):
            self.vertical_delimeters.append(pygame.Rect(*self.vertical_delimeters_coords[i], 2, self.size[1]))

    def __add__(self, graph):
        result_graph = Graph(self.app, sorted(list(set([i + j for i in self.xticks for j in graph.xticks]))), 
                             (150, 600), (1000, 300), False, "суммы" if self.app.russian else "of sum", 
                             [(self.color[i] + graph.color[i]) // 2 for i in range(4)])
        for i in range(self.number_of_values):
            for j in range(graph.number_of_values):
                result_graph.columns_height[self.xticks[i] + graph.xticks[j]] += \
                self.columns_height[self.xticks[i]] * graph.columns_height[graph.xticks[j]]
        return result_graph
    
    def reverse(self):
        self.y_axis_coords = (self.position[0] + self.size[0] - 5, self.position[1] - 20)
        self.x_axis_coords = (self.position[0] - 50, self.position[1] + self.size[1])
        self.vertical_delimeters_coords = [(self.position[0] + i * self.size[0] / self.number_of_values, self.position[1])
                                           for i in range(self.number_of_values)]
        self.y_axis = pygame.Rect(*self.y_axis_coords, 5, self.size[1] + 20)
        self.x_axis = pygame.Rect(*self.x_axis_coords, self.size[0] + 50, 5)
        self.yticks_surfaces = [self.little_font.render('-' + str(tick), False, (0, 0, 0)) for tick in self.yticks]
        self.yticks_position = [self.position[0] + self.size[0] for i in range(len(self.yticks_position))]
        self.reversed = True
        self.arrow_surfaces = [self.middle_font.render(arrow, False, (0, 0, 0)) for arrow in ['<', '^']]
         #[(self.position[0] + self.size[0] + 30 / self.scale, self.position[1] + self.size[1] - 21.25 * self.scale), (self.position[0] - 11 * self.scale, self.position[1] - 23 * self.scale)]
        self.arrows_position = [(self.position[0] - 55, self.position[1] + self.size[1] - 21.25 * self.scale), 
                                (self.position[0] + self.size[0] - 15 * self.scale, self.position[1] - 29 * self.scale)]
        self.vertical_delimeters = []
        for i in range(self.number_of_values):
            self.vertical_delimeters.append(pygame.Rect(*self.vertical_delimeters_coords[i], 2, self.size[1]))
    
    def update_coords(self, delta):
        self.y_axis_coords = (self.y_axis_coords[0] + delta[0], self.y_axis_coords[1] + delta[1])
        self.x_axis_coords = (self.x_axis_coords[0] + delta[0], self.x_axis_coords[1] + delta[1])
        self.columns_x = [self.columns_x[index] + delta[0] for index in range(self.number_of_values)]
        self.arrows_position = [(self.arrows_position[0][0] + delta[0], self.arrows_position[0][1] + delta[1]), 
                                (self.arrows_position[1][0] + delta[0], self.arrows_position[1][1] + delta[1])]
        self.yticks_position = [self.yticks_position[i] + delta[0] for i in range(len(self.yticks_position))]
        self.vertical_delimeters_coords = [(self.vertical_delimeters_coords[i][0] + delta[0], self.vertical_delimeters_coords[i][1] + delta[1])
                                           for i in range(self.number_of_values)]