import pygame as pg
from util.load import load_image
from sprites.player import Player


class Inventory(pg.sprite.Sprite):
    """ Inventory that keeps track of player bomb count """
    def __init__(self, player: Player):
        self.player = player  # Hook a player into the HUD

        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.rect = load_image("powerup/potion2_ready_0.png", -1)[1]
        self.potions = [load_image(f"powerup/potion2_ready_{n}.png", -1)[0] for n in range(0, 5)]
        self.image = self.potions[0]
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 705, 430

    def update(self):
        self.image = self.potions[self.player.bomb_count]


