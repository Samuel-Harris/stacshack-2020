import pygame as pg
from load import load_image


class HUD(pg.sprite.Sprite):
    """HUD that has a health bar."""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/heart.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 500, 500
