import pygame
from settings import *

class Input:
	def __init__(self,change_game_status):
		#["A","s","D","f","G","h","J","k","L"]
		# general setup
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		# item creation
		self.width = self.display_surface.get_size()[0] - 100
		self.height = self.display_surface.get_size()[1] / 4
		self.create_rect()

		# selection system 
		self.control_time = pygame.time.get_ticks() + 2000
		self.can_move = False

		self.change_game_status = change_game_status

	def setup_text(self, text_list):
		if len(text_list) > 0:
			self.text = text_list
			self.index = 0
			self.change_game_status("dialog")

	def input(self):
		keys = pygame.key.get_pressed()

		if self.can_move:
			print("cm")
			if keys[pygame.K_z]:
				self.index += 1
				self.can_move = False
				self.control_time = pygame.time.get_ticks()

	def selection_cooldown(self):
		if not self.can_move:
			current_time = pygame.time.get_ticks()
			print(current_time-self.control_time)
			if current_time - self.control_time >= 500:
				self.can_move = True

	def create_rect(self):
		# horizontal position
		full_width = self.display_surface.get_size()[0]
		left = (full_width - self.width) / 2
		
		# vertical position 
		full_height = self.display_surface.get_size()[1]
		top = full_height - self.height - 20

		self.rect = pygame.Rect(left,top,self.width,self.height)

	def display(self):
		self.input()
		self.selection_cooldown()
		# get attributes
		if self.index < len(self.text):
			text = self.text[self.index]
			
			pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.rect)
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,self.rect,4)

			self.display_text(self.display_surface,text)
		else:
			self.change_game_status()

	def display_text(self,surface,text):
		color = TEXT_COLOR
		text_rect = self.rect.copy()
		text_rect = text_rect.move(UI_FONT_SIZE, 0)
		
		text_list = text.split("\n")

		is_first_line = True
		for t in text_list:
			text_rect = text_rect.move(0, UI_FONT_SIZE)
			text_surf = self.font.render(t,False,color)

			# draw 
			surface.blit(text_surf,text_rect)

			if is_first_line:
				text_rect = text_rect.move(UI_FONT_SIZE / 2, UI_FONT_SIZE / 2)
				is_first_line = False
			