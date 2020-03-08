import os
from os import path
from random import randint, choice

import pygame as pg

from sprites.knife import Knife
from util.load import load_image


class Enemy(pg.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy/enemy1_big.png", -1)

        # hitbox debug
        self.hitbox_debug = False

        self.radius = 15
        self.rect.x = screen_width / 2 - self.radius / 2
        self.rect.y = screen_height / 2 - self.radius / 2

        # spawn only from top of screen
        self.rect.topleft = randint(0, screen_width - 80), 0

        # spawn randomly in top half of screen
        # self.rect.topleft = randint(0, screen_width - 80), randint(0, screen_height//2 - 80 )
        # while distance.euclidean(self.rect.topleft, player_coordinates) < 200:
        #     self.rect.topleft = randint(0, screen_width - 80), randint(0, screen_height//2 - 80)

        self.hurtbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)

        # automatic movement (to reflect map movement)
        self.auto_move = True
        self.move_x = 0
        self.move_y = 1

        # bullet generation
        self.shoot_delay = 100      # pause between bursts
        self.burst_delay = 20       # pause between shots in a burst
        self.burst_count = 3        # number of shots per burst
        self.bullet_counter = 0
        # generate frames at which enemy shoots
        self.bullet_counter_reset = self.shoot_delay + self.burst_delay * self.burst_count
        self.bullet_frames = range(self.shoot_delay, self.bullet_counter_reset, self.burst_delay)

        # sound effect
        num =randint(1, 101)
        if num != 69:
            index = randint(1, 10)
        elif num > 95:
            index = 11
        else:
            index = 13
        self.pew_sound = pg.mixer.Sound('sound/pew_' + str(index) + '.wav')

    def calc_hitboxes(self):
        self.hurtbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)

    def kill_enemy(self, player):
        player.score += 1
        topleft = self.rect.topleft
        self.image, self.rect = load_image("enemy/enemy1x_big.png", -1)
        self.rect.topleft = topleft
        pg.mixer.Sound('sound/pew_12.wav').play()

    def shoot(self, player_x, player_y):
        """ Create a knife object and throw it at the player """
        self.bullet_counter += 1
        self.bullet_counter %= self.bullet_counter_reset    # modulo

        if self.bullet_counter in self.bullet_frames:
            self.pew_sound.play()
            return Knife(self.rect.x, self.rect.y, player_x+50, player_y+50)
        else:
            return None

    def implode(self, player_x, screen_height):
        """ Create a number of knife objects and fire them in a circular pattern;
            called upon reaching the bottom of the screen """
        bullets = []
        for i in range(10):
            bullets.append(Knife(self.rect.x, self.rect.y, player_x, screen_height * i/10))
        return bullets

    def update(self):
        if self.hitbox_debug:
            screen = pg.display.get_surface()
            pg.draw.rect(screen, (255, 0, 0), self.hurtbox, 2)
        if self.auto_move:
            self.rect.x += self.move_x
            self.rect.y += self.move_y
            self.hurtbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)


