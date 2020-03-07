import pygame
import pygame as pg
from util.load import load_image
from sprites.player import Player


class HUD(pg.sprite.Sprite):
    """HUD that has a health bar."""
    def __init__(self, player: Player):
        self.player = player  # Hook a player into the HUD

        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.rect = load_image("player/heart_0.png", -1)[1]
        self.hearts = [load_image(f"player/heart_{n}.png", -1)[0] for n in range(0, 9)]
        self.image = self.hearts[0]
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 700, 500

        self.font = pygame.font.SysFont("Arial", 100)
        self.textSurf = self.font.render(str(self.player.score), 1, (128, 128, 128))
        self.image = pygame.Surface((800, 600))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [800 / 2 - W / 2, 600 / 2 - H / 2])

    def _update_hearts_display(self):
        if self.player.health < 0:
            self.player.health = 8  # TODO: Add death mechanics
        self.image = self.hearts[8 - self.player.health]

    def update(self):
        self._update_hearts_display()
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [800 / 2 - W / 2, 600 / 2 - H / 2])
