import math

import pygame as pg
from load import load_image


class Player(pg.sprite.Sprite):
    """The player model"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/player_default.png", -1)

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.health = 5

        # for attack animation
        self.attack = False
        self.attack_frame = 0
        self.attack_images = []
        for i in range(0, 5):
            filename = "art/player/attack_" + str(i) + ".png"
            self.attack_images.append(pg.image.load(filename))

    def update(self):
        self.handle_keys()
        # check if attacking
        if self.attack:
            if self.attack_frame < 5:   # get attack frame; show attack + advance attack frame
                self.image = self.attack_images[math.floor(self.attack_frame)]
                self.attack_frame += 0.25
            else:   # where attack_frame == 5, so end attack
                self.attack = False
                self.attack_frame = 0
                self.image = pg.image.load("art/player/player_default.png")

    def handle_keys(self):
        """ Handles Keys """
        dist = 3  # distance moved in 1 frame, try changing it to 5
        x, y = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            y -= dist
        if keys[pg.K_DOWN]:
            y += dist
        if keys[pg.K_LEFT]:
            x -= dist
        if keys[pg.K_RIGHT]:
            x += dist
        self.rect.x += x
        self.rect.y += y

    def start_attack(self):
        if not self.attack:
            self.attack = True
            self.attack_frame = 0

    # def update(self):
    #     """walk or spin, depending on the monkeys state"""
    #     if self.dizzy:
    #         self._spin()
    #     else:
    #         self._walk()
    #
    # def _walk(self):
    #     """move the monkey across the screen, and turn at the ends"""
    #     newpos = self.rect.move((self.move, 0))
    #     if not self.area.contains(newpos):
    #         if self.rect.left < self.area.left or self.rect.right > self.area.right:
    #             self.move = -self.move
    #             newpos = self.rect.move((self.move, 0))
    #             self.image = pg.transform.flip(self.image, 1, 0)
    #         self.rect = newpos
    #
    # def _spin(self):
    #     """spin the monkey image"""
    #     center = self.rect.center
    #     self.dizzy = self.dizzy + 12
    #     if self.dizzy >= 360:
    #         self.dizzy = 0
    #         self.image = self.original
    #     else:
    #         rotate = pg.transform.rotate
    #         self.image = rotate(self.original, self.dizzy)
    #     self.rect = self.image.get_rect(center=center)
    #
    # def punched(self):
    #     """this will cause the monkey to start spinning"""
    #     if not self.dizzy:
    #         self.dizzy = 1
    #         self.original = self.image
