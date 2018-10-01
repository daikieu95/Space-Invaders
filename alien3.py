"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import pygame
from pygame.sprite import Sprite


class Alien3(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien3, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image 3  and set its rect attribute.
        self.image = pygame.image.load('images/alien3.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges_3(self):
        """Return True if alien is at edge of screen."""

        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the fleet to the right."""
        self.x += (self.ai_settings.alien_speed_factor_3 *
                   self.ai_settings.fleet_direction_aliens_3)
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
