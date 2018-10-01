"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import pygame
from pygame.sprite import Group

from settings import Settings

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship

import game_functions as gf
import menu_functions as mf
from screens import Info_Screen
from screens2 import Info_Screen2


def menu_music_play():
    pygame.mixer.music.load("sounds/Menu.wav")
    pygame.mixer.music.play(-1)


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invader")

    # Create a Menu for the Game
    black = (0, 0, 0)
    green = (0, 200, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    click = pygame.mixer.Sound('sounds/click.wav')
    ai_s = Settings()
    down = Button(ai_s, screen, '..more', 200, 40, 300, 300, green, blue, 40)    # The More button
    title = Button(ai_s, screen, 'SPACE INVADER', 600, 200, 0, -(ai_s.screen_height / 2) + 150, black, green, 120)
    game_o = Button(ai_s, screen, 'Game Over', 200, 40, 0, 0, blue, green, 60)
    info = Info_Screen(screen)
    info2 = Info_Screen2(screen)
    infos = Button(ai_s, screen, 'INFO', 200, 40, 0, 50, green, blue, 48)
    back = Button(ai_s, screen, '<-', 40, 40, 600, -330, green, blue, 48)
    play = Button(ai_s, screen, 'PLAY', 200, 40, 0, -50, green, red, 48)
    buttons = [play, infos, back]

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make the Menu playing Music
    menu_music_play()
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)

    # Make a group to store each type of aliens, bunkers, UFO, bullets, and alien_bullets in.
    bullets = Group()
    aliens1 = Group()
    aliens2 = Group()
    aliens3 = Group()
    bunkers = Group()
    boss = Group()
    a_bullets = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets)

    # Start the main loop for the game.
    while True:
        if not stats.game_active:
            mf.check_events(stats, buttons, info, click, down, info2)

            mf.update_screen(ai_settings, screen, buttons, info, title, down, info2)

        if stats.game_active:
            gf.check_events(ai_settings, screen, stats, sb, ship,
                            aliens1, aliens2, aliens3, boss, bunkers, bullets)
            ship.update()
            boss.update()
            gf.check_b_b_collisions(a_bullets, bullets)  # alien_bullets hit ship_bullets (destroy both)
            gf.alien_bullet(ai_settings, screen, aliens1, aliens2, aliens3, boss, a_bullets, stats)
            gf.update_a_bullets(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                                a_bullets, game_o)
            gf.update_bullets_1(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                                a_bullets)
            gf.update_bullets_2(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bunkers, bullets)
            gf.update_bullets_3(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bunkers, bullets)

            gf.update_aliens_1(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                               a_bullets, game_o)
            gf.update_aliens_2(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                               a_bullets, game_o)
            gf.update_aliens_3(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                               a_bullets, game_o)
            gf.update_screen(ai_settings, screen, stats, sb, ship, boss, aliens1, aliens2, aliens3, bullets, bunkers,
                             a_bullets)


run_game()
