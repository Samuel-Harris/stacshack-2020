import pygame
import pygame as pg
from sprites.player import Player


class ScoreText(pg.sprite.Sprite):
    """score text"""
    def __init__(self, player: Player):
        self.player = player  # Hook a player into the HUD

        pg.sprite.Sprite.__init__(self)  # call Sprite intializer

        self.font = pygame.font.SysFont("Arial", 30)
        self.textSurf = None

    def generate_surface(self, text):
        return self.font.render(text, 1, (128, 128, 128))