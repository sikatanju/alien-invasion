class Settings: # * A class to store all settings for Alien Invasion.
    def __init__(self):
        # * Screen settings
        self.screen_width = 1600
        self.scree_height = 900
        self.bg_color = (230, 230, 230)
        
        # * Ship Settings
        self.ship_speed = 2.5
        self.ship_limit = 3

        # * Bullet Settings
        self.bullet_speed = 2.5
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10   

        # * Alien Settings
        self.fleet_drop_speed = 15

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # self.alien_speed = 1.0
        # self.fleet_direction = 1


    def initialize_dynamic_settings(self):
        # * """ Initialize settings taht change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
        
