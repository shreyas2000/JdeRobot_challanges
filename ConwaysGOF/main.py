from tkinter import *

import pygame
import numpy as np 
import random
import json 

from tkinter import *
from time import sleep
from basic_gui import GUI

config = {}
with open("config.json") as file:
	config = json.load(file)

class GameGUI(GUI):
	def __init__(self):
		self.labels = [('Width', IntVar, 50),
					   ('Height', IntVar, 50)]
		self.columns = 2
		self.title = 'Options'

		super().__init__(title=self.title, columns=self.columns, labels=self.labels)
		self.new_buttons = [('Go!', (lambda: Game(self.entries())))]
		self.buttons = self.new_buttons + self.buttons


class Game:
	def __init__(self, entries):
		try:
			if len(entries) > 2:
				print('Game error: too many entries!')
				return
			self.row_len, self.col_len = [ent for ent in entries if ent == int(ent) > 0]
		except ValueError:
			print('Game error: invalid entries.')
			return

		pygame.init()

		self.colours = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255), 'GRAY': (125, 125, 125)}
		self.cell_states = {'0': self.colours['WHITE'], '1': self.colours['BLACK']}

		self.zero_row = ['0' * self.row_len]
		self.blank_grid = self.zero_row * self.col_len
		self.first_life = list(self.blank_grid)
		self.grid = list(self.blank_grid)
		self.input_grid = self.zero_row + ['0{}0'.format(cell_row) for cell_row in self.grid] + self.zero_row

		self.max_width, self.max_height = 600, 600
		self.window_width = int(self.max_width * min(self.row_len / self.col_len, 1))
		self.window_height = int(self.max_height * min(1, self.col_len / self.row_len))
		self.menu_height = 50
		self.background_colour = self.colours['GRAY']
		self.window_surface = pygame.display.set_mode((self.window_width, self.window_height + self.menu_height), 0, 32)
		self.window_surface.fill(self.background_colour)

		self.rect_pos_x, self.rect_pos_y = 0.75, 0.75
		self.rect_width = (self.window_width - self.rect_pos_x) / self.row_len - self.rect_pos_x
		self.rect_height = (self.window_height - self.rect_pos_y) / self.col_len - self.rect_pos_y
		self.rects = []

		self.button_names = ['Start/Pause', 'Next Life', 'Start Over','Random','Clear', 'Erase/Draw']
		self.button_space = 5
		self.button_font = 'arialms'
		self.button_font_size = (self.window_width + self.button_space * (1 + len(self.button_names))) // 40
		self.buttons = {}

		self.paused = True
		self.eraser = False

		self.mouse_pos = pygame.mouse.get_pos()

		self.play()

	def draw_buttons(self):
		button_x, button_y = self.button_space, self.window_height + self.button_space
		button_w = (self.window_width - self.button_space) // len(self.button_names) - self.button_space
		button_h = self.menu_height - self.button_space * 2

		for button_name in self.button_names:
			dimensions = (button_x, button_y, button_w, button_h)
			self.buttons.setdefault(button_name, dimensions)

			pygame.draw.rect(self.window_surface, self.colours['WHITE'], dimensions)

			small_text = pygame.font.SysFont(self.button_font, self.button_font_size)
			text_surface = small_text.render(button_name, True, self.colours['BLACK'])
			text_rect = text_surface.get_rect()
			text_rect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))

			self.window_surface.blit(text_surface, text_rect)

			button_x += button_w + self.button_space

	def rand_Gen(self):
		a = []
		for i in range(self.col_len):
			res = ''.join(random.choices(["0","1"],k=self.row_len))
			a.append(res)	
		self.grid = a



	def update_grid(self):
		self.grid.clear()
		for j in range(1, len(self.input_grid) - 1):
			prev_row = self.input_grid[j - 1]
			row = self.input_grid[j]
			next_row = self.input_grid[j + 1]

			new_row = str()

			for i in range(len(row) - 2):
				cell_state = row[i + 1]
				cell_neighbours = ''.join([prev_row[i:i + 3],
										   row[i] + row[i + 2],
										   next_row[i:i + 3]])
				live_cells = cell_neighbours.count('1')

				if cell_state == '1':
					if live_cells < 2 or live_cells > 3:
						cell_state = '0'
				else:
					if live_cells == 3:
						cell_state = '1'

				new_row += cell_state
			self.grid.append(new_row)

	def manual_draw(self):
		for i in range(len(self.rects)):
			if self.rects[i].collidepoint(self.mouse_pos):
				clicked_rect = self.rects[i]
				grid_x, grid_y = i % len(self.grid[0]), i // len(self.grid[0])
				cell_state = self.grid[grid_y][grid_x]

				if (cell_state == '1' and self.eraser) or (cell_state == '0' and not self.eraser):
					rect_x, rect_y = clicked_rect.left, clicked_rect.top
					new_rect = pygame.Rect(rect_x, rect_y, self.rect_width, self.rect_height)
					new_cell_state = ('1' if cell_state == '0' else '0')
					new_cell_row = list(self.grid[grid_y])
					new_cell_row[grid_x] = new_cell_state

					self.grid[grid_y] = ''.join(new_cell_row)
					self.input_grid[grid_y + 1] = '0' + self.grid[grid_y] + '0'
					pygame.draw.rect(self.window_surface, self.cell_states[new_cell_state], new_rect)

					self.first_life = list(self.grid)

					return

	def draw_cells(self):
		self.input_grid[1:-1] = ['0{}0'.format(cell_row) for cell_row in self.grid]
		self.rects.clear()

		y_pos = self.rect_pos_y
		for cell_row in self.grid:
			x_pos = self.rect_pos_x
			for cell in cell_row:
				rect = pygame.Rect(x_pos, y_pos, self.rect_width, self.rect_height)
				pygame.draw.rect(self.window_surface, self.cell_states[cell], rect)
				self.rects.append(rect)
				x_pos += self.rect_width + self.rect_pos_x
			y_pos += self.rect_height + self.rect_pos_y

	def play(self):
		pygame.display.set_caption('Conways Game Of Life')

		self.draw_cells()
		self.draw_buttons()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.mouse_pos = pygame.mouse.get_pos()
					if self.mouse_pos[1] > self.window_height:
						for name, dimensions in self.buttons.items():
							x, y, w, h = dimensions
							if x + w > self.mouse_pos[0] > x and y + h > self.mouse_pos[1] > y:
								if name == 'Start/Pause':
									self.paused = (False if self.paused else True)
									config['game_conf'][0]['Row_len'] = self.row_len
									config['game_conf'][0]['Col_len'] = self.col_len
									with open('config.json', 'w') as outfile:
										json.dump(config, outfile)
									print(config)
								elif name == 'Next Life' and self.paused:
									self.update_grid()
								elif name == 'Start Over':
									self.grid = list(self.first_life)
									self.paused = True
								elif name == 'Erase/Draw':
									self.eraser = (False if self.eraser else True)
								elif name == 'Clear':
									self.grid = list(self.blank_grid)
									self.paused = True
								elif name == 'Random':
									self.rand_Gen()
								self.draw_cells()

			if not self.paused:
				self.update_grid()
				self.draw_cells()
				sleep(0.1)
			else:
				if pygame.mouse.get_pressed()[0]:
					self.mouse_pos = pygame.mouse.get_pos()
					if self.mouse_pos[0] <= self.window_width and self.mouse_pos[1] <= self.window_height:
						self.manual_draw()

			pygame.display.update()

if __name__ == '__main__':
	gui = GameGUI()
	gui.create()
