"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import sys
import random
from time import sleep
import pygame

from bullet import Bullet
from alien1 import Alien1
from alien2 import Alien2
from alien3 import Alien3
from bunker import Bunker
from UFO import UFO
from al_bullet import Al_Bullet


def background_music():
    pygame.mixer.music.load("sounds/space invader.wav")
    pygame.mixer.music.play(-1)


def stop_music():
    """stop currently playing music"""
    pygame.mixer.music.stop()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        shootSound = pygame.mixer.Sound("sounds/shoot.wav")
        shootSound.play()
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb,
                              ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, ship,
                      aliens1, aliens2, aliens3, boss, bunkers, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""

    # When the player click button plays, then start the background music right away.
    background_music()
    if not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens1.empty()
        aliens2.empty()
        aliens3.empty()
        bullets.empty()
        bunkers.empty()
        boss.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets)

        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def alien_bullet(ai_settings,screen, aliens1, aliens2, aliens3, boss, a_bullets, stats):
    if stats.game_active:
        if len(a_bullets) == 0:
            #  Pick a random number between 1 and 3.
            # If it generates the correct number then the aliens will shoot bullets
            ran = random.randint(0, 3)
            i = 0
            for alien in aliens1:
                if i == ran:
                    new = Al_Bullet(ai_settings, screen, alien)
                    a_bullets.add(new)
                    alien_shoot_sound = pygame.mixer.Sound("sounds/shoot2.wav")
                    alien_shoot_sound.play()
                i += 1


def update_a_bullets(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets,
                     a_bullets, game_o):
    if stats.game_active:
        a_bullets.update()
        for bullet in a_bullets.copy():
            if bullet.rect.top >= ai_settings.screen_height:
                a_bullets.remove(bullet)
        check_b_b_collisions(a_bullets, bullets)
        if pygame.sprite.spritecollideany(ship, a_bullets):
            ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                     game_o)


def check_b_b_collisions(a_bullets, bullets):
    for ab in a_bullets:
        for bullet in bullets :
            if pygame.Rect.colliderect(ab.rect, bullet.rect):
                a_bullets.remove(ab)
                bullets.remove(bullet)


def update_screen(ai_settings, screen, stats, sb, ship, boss, aliens1, aliens2, aliens3, bullets, bunkers,
                  a_bullets):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for b in a_bullets.sprites():
        b.draw_bullet()

    ship.blitme()
    boss.draw(screen)
    aliens1.draw(screen)
    aliens2.draw(screen)
    aliens3.draw(screen)
    bunkers.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_bullet_alien_collisions_1(ai_settings, screen, stats, sb, ship, aliens1, boss, bunkers, bullets, a_bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.

    # This is collision between the bullets and the bunkers
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, True)
    if collisions:
        explosionSound1 = pygame.mixer.Sound("sounds/explosion.wav")
        explosionSound1.play()

    # This is collision between the alien_bullets and the bunkers
    alien_bullets_with_bunker_collision = pygame.sprite.groupcollide(a_bullets, bunkers, True, True)

    if alien_bullets_with_bunker_collision:
        explosionSound2 = pygame.mixer.Sound("sounds/explosion.wav")
        explosionSound2.play()

    # This is collision between the bullets and the alien 1
    collisions1 = pygame.sprite.groupcollide(bullets, aliens1, True, True)
    if collisions1:
        for aliens1 in collisions1.values():
            stats.score += ai_settings.alien_points * len(aliens1)
            stats.score += ai_settings.alien_points
            sb.prep_score()
            invader_killed_sound = pygame.mixer.Sound("sounds/invaderkilled.wav")
            invader_killed_sound.play()

        check_high_score(stats, sb)

    # This is collision between the bullets and the ufo(boss)
    bullet_collision_ufo = pygame.sprite.groupcollide(bullets, boss, True, True)

    # When the UFO is killed, the score would be 300 points
    if bullet_collision_ufo:
        for ufo in bullet_collision_ufo.values():
            stats.score += ai_settings.alien_points * len(ufo) # 100 * 1 = 100
            stats.score += ai_settings.alien_points + 900  # 100 + 900 = 1000.
            sb.prep_score()
            ufo_killed_sound = pygame.mixer.Sound("sounds/ufokilled.wav")
            ufo_killed_sound.play()

        check_high_score(stats, sb)


def update_bullets_1(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets):
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions_1(ai_settings, screen, stats, sb, ship, aliens1, boss, bunkers, bullets, a_bullets)
    if len(aliens1) == 0 and len(aliens2) == 0 and len(aliens3) == 0 and len(boss) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets)


def check_bullet_alien_collisions_2(ai_settings, screen, stats, sb, ship, aliens2, bunkers, bullets):
    """Update position of bullets, and get rid of old bullets."""

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.

    collisions2 = pygame.sprite.groupcollide(bullets, aliens2, True, True)
    if collisions2:
        for aliens2 in collisions2.values():
            stats.score += ai_settings.alien_points_2 * len(aliens2)
            stats.score += ai_settings.alien_points
            sb.prep_score()
            invader_killed_sound = pygame.mixer.Sound("sounds/invaderkilled.wav")
            invader_killed_sound.play()
        check_high_score(stats, sb)


def update_bullets_2(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bunkers, bullets):
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet2 in bullets.copy():
        if bullet2.rect.bottom <= 0:
            bullets.remove(bullet2)
    check_bullet_alien_collisions_2(ai_settings, screen, stats, sb, ship, aliens2, bunkers, bullets)


def check_bullet_alien_collisions_3(ai_settings, screen, stats, sb, ship, aliens3, bunkers, bullets):
    """Update position of bullets, and get rid of old bullets."""

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.

    collisions3 = pygame.sprite.groupcollide(bullets, aliens3, True, True)
    if collisions3:
        for aliens3 in collisions3.values():
            stats.score += ai_settings.alien_points_3 * len(aliens3)
            stats.score += ai_settings.alien_points
            sb.prep_score()
            invader_killed_sound = pygame.mixer.Sound("sounds/invaderkilled.wav")
            invader_killed_sound.play()
        check_high_score(stats, sb)


def update_bullets_3(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bunkers, bullets):
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet3 in bullets.copy():
        if bullet3.rect.bottom <= 0:
            bullets.remove(bullet3)
    check_bullet_alien_collisions_3(ai_settings, screen, stats, sb, ship, aliens3, bunkers, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def get_number_aliens_x1(ai_settings, alien_width1):
    """Determine the number of aliens that fit in a row."""
    available_space_x1 = ai_settings.screen_width - 5 * alien_width1
    number_aliens_x1 = int(available_space_x1 / (5 * alien_width1))
    return number_aliens_x1


def create_alien_1(ai_settings, screen, aliens1, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    alien1 = Alien1(ai_settings, screen)
    alien_width1 = alien1.rect.width
    alien1.x = alien_width1 + 5 * alien_width1 * alien_number1
    alien1.rect.x = alien1.x
    alien1.rect.y = alien1.rect.height + 2 * alien1.rect.height * row_number
    aliens1.add(alien1)


def create_alien_2(ai_settings, screen, aliens2, alien_number2, row_number):
    """Create an alien, and place it in the row."""
    alien2 = Alien2(ai_settings, screen)
    alien_width2 = alien2.rect.width
    alien2.x = 152 + 5 * alien_width2 * alien_number2
    alien2.rect.x = alien2.x
    alien2.rect.y = alien2.rect.height + 2 * alien2.rect.height * row_number
    aliens2.add(alien2)


def create_alien_3(ai_settings, screen, aliens3, alien_number3, row_number):
    """Create an alien, and place it in the row."""
    alien3 = Alien3(ai_settings, screen)
    alien_width3 = alien3.rect.width
    alien3.x = 250 + 5 * alien_width3 * alien_number3
    alien3.rect.x = alien3.x
    alien3.rect.y = alien3.rect.height + 2 * alien3.rect.height * row_number
    aliens3.add(alien3)


def create_ufo(ai_settings, screen, boss):
    """Create an alien, and place it in the row."""
    ufo = UFO(ai_settings, screen)
    ufo_width = ufo.rect.width
    ufo.x = 530
    ufo.rect.x = ufo.x
    ufo.rect.y = 170
    ufo.add(boss)


def create_bunker(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 55 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_2(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 75 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_3(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 95 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_4(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 115 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_5(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 135 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_6(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 155 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_bunker_7(ai_settings, screen, bunkers, alien_number1, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = 175 + 15 * bunker_width * alien_number1
    bunker.rect.x = bunker.x
    bunker.rect.y = 550 + 1 * bunker.rect.height * row_number
    bunker.add(bunkers)


def create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien1 = Alien1(ai_settings, screen)
    number_aliens_x1 = get_number_aliens_x1(ai_settings, alien1.rect.width)

    # Create the fleet of aliens.
    for row_number in range(4):
        for alien_number in range(number_aliens_x1):
            create_alien_1(ai_settings, screen, aliens1, alien_number, row_number)
            create_alien_2(ai_settings, screen, aliens2, alien_number, row_number)
            create_alien_3(ai_settings, screen, aliens3, alien_number, row_number)

    # Create Bunker 1
    for row_number in range(3): # 3 rows
        for alien_number in range(4): # 4 columns
            create_bunker(ai_settings, screen, bunkers, alien_number, row_number)

    # Create Bunker 2
    for row_number in range(3): # 3 rows
        for alien_number in range(4): # 4 columns
            create_bunker_2(ai_settings, screen, bunkers, alien_number, row_number)

    # Create Bunker 3
    for row_number in range(3): # 3 rows
        for alien_number in range(4): # 4 columns
            create_bunker_3(ai_settings, screen, bunkers, alien_number, row_number)

    # Create Bunker 4
    for row_number in range(3):  # 3 rows
        for alien_number in range(4):  # 4 columns
            create_bunker_4(ai_settings, screen, bunkers, alien_number, row_number)

    # Create Bunker 5
    for row_number in range(3):  # 3 rows
        for alien_number in range(4):  # 4 columns
            create_bunker_5(ai_settings, screen, bunkers, alien_number, row_number)

        # Create Bunker 6
    for row_number in range(3):  # 3 rows
        for alien_number in range(4):  # 4 columns
            create_bunker_6(ai_settings, screen, bunkers, alien_number, row_number)

        # Create Bunker 7
    for row_number in range(3):  # 3 rows
        for alien_number in range(4):  # 4 columns
            create_bunker_7(ai_settings, screen, bunkers, alien_number, row_number)

    # Create an UFO (Boss)
    for row_number in range(1):
        for alien_number in range(1):
            create_ufo(ai_settings, screen, boss)


def check_fleet_edges_UFO(ai_settings, ship, boss):
    """Respond appropriately if any aliens have reached an edge."""
    for ufo in boss.sprites():
        if ufo.check_edges():
            change_fleet_direction_UFO(ai_settings, boss)
            break


def check_fleet_edges_1(ai_settings, ship, aliens1):
    """Respond appropriately if any aliens have reached an edge."""
    for alien1 in aliens1.sprites():
        if alien1.check_edges_1():
            change_fleet_direction_1(ai_settings, aliens1)
            break


def check_fleet_edges_2(ai_settings, ship, aliens2):
    """Respond appropriately if any aliens have reached an edge."""
    for alien2 in aliens2.sprites():
        if alien2.check_edges_2():
            change_fleet_direction_2(ai_settings, aliens2)
            break


def check_fleet_edges_3(ai_settings, ship, aliens3):
    """Respond appropriately if any aliens have reached an edge."""
    for alien3 in aliens3.sprites():
        if alien3.check_edges_3():
            change_fleet_direction_3(ai_settings, aliens3)
            break


def check_fleet_edges_UFO(ai_settings, ship, boss):
    """Respond appropriately if any aliens have reached an edge."""
    for ufo in boss.sprites():
        if ufo.check_edges_ufo():
            change_fleet_direction_UFO(ai_settings, boss)
            break


def change_fleet_direction_UFO(ai_settings, boss):
    """Change the fleet's direction to the left when it hit the edge."""
    for ufo in boss.sprites():
        ufo.rect.y += ai_settings.fleet_drop_speed + 15
    ai_settings.fleet_direction_UFO *= -1


def change_fleet_direction_1(ai_settings, aliens1):
    """Change the fleet's direction to the left when it hit the edge."""
    for alien1 in aliens1.sprites():
        alien1.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction_aliens_1 *= -1


def change_fleet_direction_2(ai_settings, aliens2):
    """Change the fleet's direction to the right when it hit the edge."""
    for alien2 in aliens2.sprites():
        alien2.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction_aliens_2 *= -1


def change_fleet_direction_3(ai_settings, aliens3):
    """Change the fleet's direction to the left when it hit the edge."""
    for alien3 in aliens3.sprites():
        alien3.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction_aliens_3 *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets, game_o):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        ship_explosion_sound = pygame.mixer.Sound("sounds/ship explosion.wav")
        ship_explosion_sound.play()

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        Game_Over_sound = pygame.mixer.Sound("sounds/Game Over.wav")
        Game_Over_sound.play()
        stop_music()
        game_o.draw_button()
        pygame.display.flip()
        sleep(2)

    # Empty the list of aliens and bullets.
    aliens1.empty()
    aliens2.empty()
    aliens3.empty()
    bullets.empty()
    bunkers.empty()
    boss.empty()
    a_bullets.empty()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def update_aliens_1(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                    game_o):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens1 in the fleet.
    """
    check_fleet_edges_1(ai_settings, ship, aliens1)
    aliens1.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens1):
        print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                 game_o)


def update_aliens_2(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                    game_o):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens1 in the fleet.
    """
    check_fleet_edges_2(ai_settings, ship, aliens2)
    aliens2.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens2):
        print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                 game_o)


def update_aliens_3(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets, game_o):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens1 in the fleet.
    """
    check_fleet_edges_3(ai_settings, ship, aliens3)
    aliens3.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens3):
        print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, boss, bunkers, bullets, a_bullets,
                 game_o)


