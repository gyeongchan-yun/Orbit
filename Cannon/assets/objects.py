import pygame
import os
from random import randint
from math import sin, cos, pi, inf


CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def rotate(surface, angle, pivot, offset):
	"""Rotate the surface around the pivot point.

	Args:
					surface (pygame.Surface): The surface that is to be rotated.
					angle (float): Rotate by this angle.
					pivot (tuple, list, pygame.math.Vector2): The pivot point.
					offset (pygame.math.Vector2): This vector is added to the pivot.
	"""
	rotated_image = pygame.transform.rotozoom(
		surface, -angle, 1)  # Rotate the image.
	rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
	# Add the offset vector to the center/pivot point to shift the rect.
	rect = rotated_image.get_rect(center=pivot+rotated_offset)
	return rotated_image, rect  # Return the rotated image and shifted rect.


class Plank:
	"""base plank for the cannon"""
	PLANK_WIDTH = 150
	PLANK_HEIGHT = 30

	def __init__(self, win_width, win_height):
		self.WIN_WIDTH = win_width
		self.WIN_HEIGHT = win_height
		self.x_vel = 1
		self.rect = pygame.Rect(0, 0, self.PLANK_WIDTH, self.PLANK_HEIGHT)
		self.rect.center = (win_width / 2, win_height - 50)
		self.cannon = pygame.transform.scale(
			pygame.image.load(os.path.join(CUR_DIR, 'imgs', 'cannon.png')),
			(80, 110)
		)

	def move(self):
		if self.rect.right >= self.WIN_WIDTH or self.rect.left <= 0:
			if abs(self.x_vel) < 5:
				self.x_vel = -1.3 * self.x_vel
			else:
				self.x_vel = -self.x_vel
		self.rect.left += self.x_vel

	def draw(self, win, angle):
		self.move()
		pygame.draw.rect(win, (100, 100, 100), self.rect)
		x, y = self.rect.center
		rotated_img, new_rect = rotate(
			self.cannon, angle, (x, y), pygame.math.Vector2(0, -30))
		win.blit(rotated_img, new_rect.topleft)


class Ball:
	"""the target balls falling from top"""
	MAX_RADIUS = 25
	MIN_RADIUS = 5

	def __init__(self, win_width, max_y):
		self.WIN_WIDTH = win_width
		self.radius = 22
		self.center = [
			randint(self.MAX_RADIUS, win_width - self.MAX_RADIUS), randint(max_y - 100, max_y - 50)]
		self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
		pygame.draw.circle(self.surf, (153, 0, 255), (25, 25), self.radius)
		self.mask = pygame.mask.from_surface(self.surf)
		self.rect = self.surf.get_rect(center=self.center)
		self.y_vel = 5

	def move(self):
		self.rect.move_ip(0, self.y_vel)

	def draw(self, win):
		self.move()
		win.blit(self.surf, self.rect)


class Bullet:
	"""bullets fired from cannon"""
	VEL = 10

	def __init__(self, x, y, angle, win_width):
		self.WIN_WIDTH = win_width
		self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
		pygame.draw.circle(self.surf, (255, 51, 0), (10, 10), 10)
		self.mask = pygame.mask.from_surface(self.surf)
		x, y = x + 50 * sin(pi * (angle / 180)), y - 50 * cos(pi * (angle / 180))
		self.rect = self.surf.get_rect(center=(x, y))
		self.dx = self.VEL * sin(pi * (angle / 180))
		self.dy = -self.VEL * cos(pi * (angle / 180))

	def move(self):
		if self.rect.left <= 0 or self.rect.right >= self.WIN_WIDTH:
			self.dx = -self.dx
		self.rect.move_ip(self.dx, self.dy)

	def draw(self, win):
		self.move()
		win.blit(self.surf, self.rect)
