"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import pygame
from pygame.sprite import Sprite


class Al_Bullet(Sprite):
    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 18)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        self.y = float(self.rect.y)
        self.color = (255, 0, 0)  # Display Color Red for the Alien Bullet
        self.speed = ai_settings.bullet_speed_factor / 2

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

