import math

import pygame as pg
from load import load_image


class Player(pg.sprite.Sprite):
    """The player model"""

    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/player_default.png", -1)

        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 0
        self.radius = 15
        self.rect.x = screen_width / 2 - self.radius / 2
        self.rect.y = screen_height / 2 - self.radius / 2
        self.dist = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = None
        self.rect.topleft = 10, 10
        self.health = 5
        self.move = 9
        self.attack_cooldown = 0
        self.attack_box = (self.rect.x, self.rect.y + 30, 30, 30)
        # for attack animation
        self.attack = False
        self.attack_frame = 0
        self.attack_images = []
        for i in range(0, 5):
            filename = "art/player/attack_" + str(i) + ".png"
            self.attack_images.append(pg.image.load(filename))

    def calc_hitbox(self):
        self.attack_box = (self.rect.x + 25, self.rect.y, 50, 50)



    def update(self):
        self.handle_keys()
        if self.attack_cooldown > 0:
            self.attack_cooldown = self.attack_cooldown - 1
            print(self.attack_cooldown)
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
        x_change = 0
        y_change = 0
        if keys[pg.K_UP]:
            y_change -= self.dist
        if keys[pg.K_DOWN]:
            y_change += self.dist
        if keys[pg.K_LEFT]:
            x_change -= self.dist
        if keys[pg.K_RIGHT]:
            x_change += self.dist
        # self.rect.x += x_change
        # self.rect.y += y_change

        self.rect.x += x_change

        # Did this update cause us to hit a wall?
        block_hit_list = pg.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if x_change > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += y_change

        # Check and see if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if y_change > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def start_attack(self):
        if not self.attack and self.attack_cooldown == 0:
            self.attack = True
            self.attack_frame = 0
            self.attack_cooldown = 100

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
