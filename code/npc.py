import pygame
from settings import *
from support import import_folder
from entity import Entity

class NPC(Entity):
	def __init__(self,pos,groups,col,action):
		super().__init__(groups)
		self.sprite_type = 'npc'

		self.data = npc_data[col]

		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

		self.import_assets()
		self.status = "down"

		self.actionA = action

	def import_assets(self):
		character_path = '../graphics/{}/'.format(self.data["image"])
		self.animations = {'up': [],'down': [],'left': [],'right': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)
	
	def action(self, char):
		print(char.status, self.status)
		self.turnof(char.status)
		
		self.actionA.get_list(self.data["action"])

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def turnof(self, direction):
		if "left" in direction:
			self.status = "right"
		elif "right" in direction:
			self.status = "left"
		elif "down" in direction:
			self.status = "up"
		else:
			self.status = "down"
		self.image = self.animations[self.status][0]


	def update(self):
		pass