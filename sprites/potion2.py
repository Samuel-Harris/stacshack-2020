from random import randint

import pygame as pg
from util.load import load_image


class Potion2(pg.sprite.Sprite):
    """ 2nd potion sprite """
    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("powerup/potion2_0.png", -1)

        self.frame = 0
        self.images = []
        for i in range(0, 10):
            filename = "potion2_" + str(i) + ".png"
            self.images.append(pg.image.load(filename))

        # hitbox debug
        self.hitbox_debug = True

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = randint(10, screen_width-34), randint(10, screen_height-34)

        # auto move down
        self.auto_move = True
        self.move_x = 0
        self.move_y = 1

    def update(self):
        if self.hitbox_debug:
            screen = pg.display.get_surface()
            pg.draw.rect(screen, (255, 0, 0), self.rect, 2)

        if self.auto_move:
            self.rect.x += self.move_x
            self.rect.y += self.move_y

        # update sprite image
        self.frame += 1
        self.image = self.images[self.frame]
