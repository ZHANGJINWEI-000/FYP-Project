import pygame
from textBox import textBox
from settings import *

class Dialog(textBox):
	def __init__(self,game_status):
		super().__init__(game_status)
		self.initParam()

	def initParam(self):
		self.index = 0
		self.control_time = pygame.time.get_ticks() + 500
		self.can_move = False
		self.finish = False

	def setup(self, content):
		if len(content) > 0:
			self.content = content

			self.initParam()
			self.game_status.add("dialog")
			self.game_status.add("inchat")
			return True
		return False

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_z]:
			self.index += 1
			self.can_move = False
			self.control_time = pygame.time.get_ticks()

	def selection_cooldown(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.control_time >= 500:
			self.can_move = True

	def createRect(self):
		full_width = self.display_surface.get_size()[0]
		full_height = self.display_surface.get_size()[1]

		width = full_width - 100
		height = UI_FONT_SIZE * 8
		left = (full_width - width) / 2
		top = full_height - height - 20

		super().createRect(left, top, width, height)

	def update(self):
		if self.index < len(self.content):
			content = self.content[self.index]
			self.setText(content)

			if self.can_move:
				self.input()
			else:
				self.selection_cooldown()
		elif not self.finish:
				self.quit()
				self.finish = True
				self.game_status.remove("inchat")
		super().update()
			