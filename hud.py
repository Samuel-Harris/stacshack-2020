import pygame as pg
from load import load_image
from player import Player


class HUD(pg.sprite.Sprite):
    """HUD that has a health bar."""
    def __init__(self, player: Player):
        self.player = player  # Hook a player into the HUD

        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/heart.png", -1)  # TODO: Add multiple hearts
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 500, 500

    def _update_hearts_display(self):
        pass

    def update(self):
        self._update_hearts_display()