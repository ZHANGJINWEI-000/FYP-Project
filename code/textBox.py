import pygame
from settings import *

class textBox:
	def __init__(self,game_status):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
		self.color = TEXT_COLOR

		self.createRect()

		self.resetText()

		self.game_status = game_status

	def createRect(self, left=0, top=0, width=0, height=0):
		self.rect = pygame.Rect(left,top,width,height)

	def resetText(self):
		self.setText()

	def setText(self, content = {}):
		self.text = content.get("text", "")
		self.char_name = content.get("char_name", "")

	def action(self, type, content = None):
		if type == "setup":
			return self.setup(content)
		elif type == "gettext":
			return self.getText()

	def setup(self, content = None):
		return True

	def getText(self):
		return self.text

	def input(self):
		pass

	def update(self):
		self.display()

	def display(self):
		self.display_ui()
		self.display_text()
		
	def display_ui(self):
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,self.rect,4)

	def display_text(self):
		text_rect = self.rect.copy()
		text_rect = text_rect.move(UI_FONT_SIZE, -UI_FONT_SIZE / 2)
		
		text_list = self.text.split("\n")

		if self.char_name:
			text = self.char_name + ":"
			text_rect = text_rect.move(0, UI_FONT_SIZE)
			text_surf = self.font.render(text, False, self.color)
			self.display_surface.blit(text_surf,text_rect)

			text_rect = text_rect.move(UI_FONT_SIZE / 2, 0)

		for text in text_list:
			text_rect = text_rect.move(0, UI_FONT_SIZE * 3 / 2)
			text_surf = self.font.render(text, False, self.color)

			# draw 
			self.display_surface.blit(text_surf,text_rect)

	def quit(self):
		if not self.game_status.exist("action"):
			self.game_status.add("implement")