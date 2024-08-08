import pygame
from pygame.sprite import Sprite
# * A class to manage ship
class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # * Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # * Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # * Store a float for ship's exact horizontal position.
        self.x = float(self.rect.x)

        # * Movement flag, start with the ship that's not moving.
        self.moving_right = False
        self.moving_left = False

        # * Initialize an instance of settings for accessing ship's settings
        self.settings = ai_game.settings

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x


    def blitme(self):
        # * Draw the ship at its current location.
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)