import pygame as pg
from load import load_image


class Player(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/player_default.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.attack_cooldown = 0
        self.attack_box = (self.rect.x + 10, self.rect.y + 10, 10, 10)

    def calc_hitbox(self):
        self.attack_box = (self.rect.x + 10, self.rect.y + 10, 10, 10)

    def handle_keys(self):
        """ Handles Keys """
        key = pg.key.get_pressed()
        dist = 5  # distance moved in 1 frame, try changing it to 5
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
        self.calc_hitbox()

        if keys[pg.K_SPACE]:
            self.attack()


    def attack(self):
        if not self.attack_cooldown:
            self.attack_cooldown = 10


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
