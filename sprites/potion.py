from random import randint

import pygame as pg
from util.load import load_image


class Potion(pg.sprite.Sprite):
    """HUD that has a health bar."""
    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("powerup/potion1.png", -1)

        # hitbox debug
        self.hitbox_debug = True

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = randint(10, screen_width-34), randint(10, screen_height-34)

    def update(self):
        if self.hitbox_debug:
            screen = pg.display.get_surface()
            pg.draw.rect(screen, (255, 0, 0), self.rect, 2)
