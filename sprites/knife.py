from random import randint

import pygame as pg
from util.load import load_image


class Knife(pg.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy/enemy1_big.png", -1)

        # hitbox debug
        self.hitbox_debug = True

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 10
        self.rect.x = screen_width / 2 - self.radius / 2
        self.rect.y = screen_height / 2 - self.radius / 2
        self.dist = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = None
        self.rect.topleft = randint(0, 800), randint(0, 600)
        self.health = 1
        self.move = 9
