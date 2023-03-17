import pygame
from textBox import textBox
from settings import *

class Input(textBox):
	def __init__(self, game_status):
		super().__init__(game_status)
		self.keyRepeatWait = 17 * 20 #1000/60=16.666

	def setup(self, content = None):
		self.resetText()
		pygame.key.set_repeat(self.keyRepeatWait, 17*5)
		self.game_status.add("input")
		self.game_status.remove("entered")
		return True
	
	def getText(self):
		self.game_status.remove("entered")
		return super().getText()

	def update(self):
		#self.input()
		self.display()

	def display_text(self):
		text_rect = self.rect.copy()
		text_rect = text_rect.move(UI_FONT_SIZE, UI_FONT_SIZE)

		text = self.text + "|"

		text_surf = self.font.render(text, False, self.color)
		self.display_surface.blit(text_surf,text_rect)

	def input(self, event):
		if event.type == pygame.KEYDOWN:
			key = event.key
			if key == pygame.K_RETURN:
				self.quit()
			elif key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			elif len(self.text) < 50:
				self.text = self.text + event.unicode

	def createRect(self):
		full_width = self.display_surface.get_size()[0]
		full_height = self.display_surface.get_size()[1]

		width = full_width - 100 * 5
		height = UI_FONT_SIZE * 3
		
		left = full_width - width - 50
		top = full_height - height * 4 - 20

		super().createRect(left,top,width,height)

	def quit(self):
		pygame.key.set_repeat(0)
		self.game_status.remove("input")
		self.game_status.add("entered")
		super().quit()