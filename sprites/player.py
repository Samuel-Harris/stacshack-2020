import math

import pygame as pg
from util.load import load_image


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
        self.health = 8    # there are 9 stages of health; starting from heart_0 to heart_8 (death)
        self.move = 9

        # attack data
        self.attack_cooldown = 0
        self.attack_box = (self.rect.x, self.rect.y + 30, 30, 30)
        # attack animation
        self.attack = False
        self.attack_frame = 0
        self.attack_images = []
        for i in range(0, 5):
            filename = "art/player/attack_" + str(i) + ".png"
            self.attack_images.append(pg.image.load(filename))

        # attack_ready animation
        self.attack_ready = False
        self.attack_ready_frame = 0
        self.attack_ready_images = []
        for i in range(0, 3):
            filename = "art/player/ready_" + str(i) + ".png"
            self.attack_ready_images.append(pg.image.load(filename))

        # attack_ready progress bar
        self.attack_ready_bar = pg.Surface((10, 50))
        for x in range(self.attack_ready_bar.get_width()):
            for y in range(self.attack_ready_bar.get_height()):
                self.attack_ready_bar.set_at((x, y), pg.Color(100, 100, 100))

        # self.attack_ready_rect = self.attack_ready_bar.get_rect(topleft=(200, 100))


        # hurtbox data
        self.hurtbox = (self.rect.x, self.rect.y, 20, 20)

    def calc_hitboxes(self):
        self.attack_box = (self.rect.x + 25, self.rect.y, 50, 50)
        self.hurtbox = (self.rect.x + 40, self.rect.y + 40, 20, 20)

    def update(self):
        self.handle_keys()
        self.handle_health()
        self.handle_attack()

    def handle_attack(self):
        """ Checks if attacking/on cooldown; continues/updates it as necessary"""

        if self.attack_cooldown > 0:
            self.attack_cooldown = self.attack_cooldown - 1
            if self.attack_cooldown == 0:   # play the 'ready' animation upon cooldown decreasing to 0
                self.attack_ready = True

        # check if attacking
        if self.attack:
            if self.attack_frame < 5:   # get attack frame; show attack + advance attack frame
                self.image = self.attack_images[math.floor(self.attack_frame)]
                self.attack_frame += 0.25
            else:   # where attack_frame == 5, so end attack
                self.attack = False
                self.attack_frame = 0
                self.image = pg.image.load("art/player/player_default.png")
        # if not attacking, check if ready
        elif self.attack_ready:
            if self.attack_ready_frame < 3:
                self.image = self.attack_ready_images[math.floor(self.attack_ready_frame)]
                self.attack_ready_frame += 0.5
            else:  # where attack_ready_frame == 3, so end attack_ready animation
                self.attack_ready = False
                self.attack_ready_frame = 0
                self.image = pg.image.load("art/player/player_default.png")

        # handle progress bar for attack_ready
        screen = pg.display.get_surface()
        screen.blit(self.attack_ready_bar, (self.rect.x+80, self.rect.y+25), area=(0, 0, 10, self.attack_cooldown//2))

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

        self.calc_hitboxes()

    def start_attack(self):
        """ Starts an attack """
        if not self.attack and self.attack_cooldown == 0:
            self.attack = True
            self.attack_frame = 0
            self.attack_cooldown = 100

    def handle_health(self):
        """ Handles sprite display depending on health """  # TODO: Remove? Health is part of HUD, not player
        pass

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
