import math

import pygame as pg
from util.load import load_image


class Knife2(pg.sprite.Sprite):

    def __init__(self, start_x, start_y, player_x):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet/knife2.png", -1)

        # hitbox debug
        self.hitbox_debug = True

        self.rect.x = start_x
        self.rect.y = start_y
        # 'true' coordinates to hold decimal coordinates
        self.true_x = start_x * 1.0
        self.true_y = start_y * 1.0

        # hitbox
        self.size_x = 32
        self.size_y = 32
        self.offset_x = 64 - self.size_x/2   # offset_x of 64 leads to centre x
        self.offset_y = 96 - self.size_y/2    # offset_y of 64 leads to centre y; offset_y of 96 for lower portion
        self.hurtbox = pg.Rect(self.rect.x, self.rect.y, 0, 0)  # initialises hitbox; not actual size

        self.player_x = player_x
        self.xspeed = 0.03  # proportion of distance covered in a frame
        self.yspeed = 8

        # # memes - doesn't work
        # self.auto_rotate = True
        # self.auto_rotate_angle = 10

    def update(self):
        screen = pg.display.get_surface()

        if self.hitbox_debug:
            pg.draw.rect(screen, (0, 0, 255), self.hurtbox, 2)
            pg.draw.rect(screen, (0, 0, 255), self.rect, 2)

        # update true positions + reflect them in rect positions;
        # # change x by slight homing; doesn't work
        # if self.true_x > self.player_x + 20:
        #     self.true_x -= self.xspeed
        # elif self.true_x > self.player_x + 20:
        #     self.true_x += self.xspeed

        self.true_y += self.yspeed

        self.rect.x = round(self.true_x)
        self.rect.y = round(self.true_y)
        self.hurtbox = pg.Rect(self.rect.x+self.offset_x, self.rect.y+self.offset_y,
                               self.size_x, self.size_y)

