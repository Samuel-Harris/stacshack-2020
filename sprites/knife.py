import math
from random import randint

import pygame as pg
from util.load import load_image


class Knife(pg.sprite.Sprite):

    def __init__(self, start_x, start_y, player_x, player_y):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet/knife1.png", -1)

        # hitbox debug
        self.hitbox_debug = True

        self.rect.x = start_x
        self.rect.y = start_y

        # hitbox
        self.size_x = 10
        self.size_y = 10
        self.offset_x = 10   # offset_x of 10 leads to centre x
        self.offset_y = 20   # offset_y of 20 leads to centre y
        self.hurtbox = pg.Rect(self.rect.x, self.rect.y, 0, 0)

        self.speed = 5

        # aim towards player
        self.dx, self.dy, self.angle = self.face_to_player(start_x, start_y, player_x, player_y)
        self.image = pg.transform.rotate(self.image, self.angle)
        # self.hurtbox = self.hurtbox(center=rect.center)


    def update(self):
        screen = pg.display.get_surface()

        if self.hitbox_debug:
            pg.draw.rect(screen, (0, 0, 255), self.hurtbox, 2)  # green to distinguish from others

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        self.hurtbox = pg.Rect(self.rect.x+self.offset_x, self.rect.y+self.offset_y,
                               self.size_x, self.size_y)

    def face_to_player(self, x, y, px, py):
        """ Given current position (x, y) and player position (px, py), gives a dx/dy to follow
        'dx' and 'dy' should be multiplied by self.speed in order to give the change in x and y. """
        Dx = px - x     # total difference in x
        Dy = py - y     # total difference in y
        D = math.sqrt(math.pow(Dx, 2) + math.pow(Dy, 2))    # total distance

        dx = Dx / D
        dy = Dy / D

        angle = 90 - (math.atan2(Dy, Dx) * 180/math.pi)    # convert to degrees; negate + 90 due to knife orientation

        return dx, dy, angle

    def rot_center(self, image, rect, angle):
        """ Used to rotate an image while keeping its center """
        rot_image = pg.transform.rotate(image, angle)   # angle degrees, anti-clockwise
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
