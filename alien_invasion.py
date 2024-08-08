import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:  #  * """This is main class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()

        self.game_active = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # print(self.settings.screen_width, self.settings.scree_height)
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.play_button = Button(self, "Play")
        self._create_fleet()

        #* Instance of Game Stats:
        self.stats = GameStats(self)
        
        self.sb = Scoreboard(self)

    def run_game(self): # * Start the main loop for the game.
        while True:
            # * Watch for keyboard and mous events.
            self._check_events()

            if self.game_active:
            # * Update the movement of the ship according to key presses
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            # * Redraw the screen during each pass throught the loop.
            # self.screen.fill(self.settings.bg_color)
            # self.ship.blitme()

            # * Make the most recently drawn screen visible.
            # pygame.display.flip()
            self.clock.tick(60)

            self._update_screen()  
              
    def _check_events(self): # * A helper method for checking for an event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # print(len(self.bullets))
        self._check_alien_bullet_collision()

    def _check_alien_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            
            self.sb.prep_score()
            self.sb.check_high_score()
         
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.sb.prep_level()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_bullet()
            else:
                self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self): # * A helper method for updating the game's screen
        
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        #* Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            print("Ship Hit!!!")
            self._ship_hit()
        
        self._check_alien_bottom()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        i = 0
        # while current_y < (self.settings.scree_height - 8 * alien_height):
        while i < 3:
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
                
            current_x = alien_width
            current_y += 2 * alien_height
            i += 1 

    def _create_alien(self, current_x, current_y):
        new_alien = Alien(self)
        new_alien.rect.x = current_x
        new_alien.x = current_x
        new_alien.rect.y = current_y
        new_alien.y = current_y
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            self.bullets.empty()
            self.aliens.empty()
            self.sb.prep_ship()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.scree_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.sb.prep_ship()
            self._start_game()

    def _start_game(self):
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.game_active = True
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()