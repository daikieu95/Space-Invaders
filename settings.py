"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_speed_factor = 1.5
        self.ship_limit = 2  # Though this value is 2, but player will have 3 lives.

        # Bullet settings.
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 4

        # Alien settings
        self.alien_speed_factor = 0.25
        self.alien_speed_factor_2 = 0.25
        self.alien_speed_factor_3 = 0.25
        self.alien_speed_factor_4 = 0.25
        self.fleet_drop_speed = 30
        self.im = 0

        # Fleet_direction of 1 represents right; -1 represents left.

        # For the direction to the right of aliens1
        self.fleet_direction_UFO = 1

        # For the direction to the right of aliens1
        self.fleet_direction_aliens_1 = 1

        # For the direction to the left of aliens2
        self.fleet_direction_aliens_2 = 1

        # For the direction to the right of aliens3
        self.fleet_direction_aliens_3 = 1

        # For the direction to the left of aliens4
        self.fleet_direction_aliens_4 = 1

        # How quickly the game speeds up.

        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3

        # Scoring.
        self.alien_points = 50
        self.alien_points_2 = 100
        self.alien_points_3 = 150

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

