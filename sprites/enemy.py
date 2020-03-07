from random import randint

import pygame as pg
from util.load import load_image


class Enemy(pg.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        # hitbox debug
        self.hitbox_debug = True

        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy/enemy1_big.png", -1)

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 15
        self.rect.x = screen_width / 2 - self.radius / 2
        self.rect.y = screen_height / 2 - self.radius / 2
        self.dist = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = None
        self.rect.topleft = randint(0, screen_width - 80), randint(0, screen_height - 80)
        self.health = 1
        self.move = 9

        self.hurtbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)

    def calc_hitboxes(self):
        self.hurtbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)

    def kill_enemy(self, player):
        player.score += 1
        topleft = self.rect.topleft
        self.image, self.rect = load_image("enemy/enemy1x_big.png", -1)
        self.rect.topleft = topleft

    def update(self):
        if self.hitbox_debug:
            screen = pg.display.get_surface()
            pg.draw.rect(screen, (255, 0, 0), self.hurtbox, 2)