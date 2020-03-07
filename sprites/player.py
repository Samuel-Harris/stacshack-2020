import math

import pygame as pg
from util.load import load_image


class Player(pg.sprite.Sprite):
    """The player model"""

    def __init__(self, screen_width, screen_height, potion_list):
        self.sprite_img_radius = 50
        self.sprite_char_radius = 15
        self.hitbox_radius = 10
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player/player_default.png", -1)
        self.rect.x = 100
        self.rect.y = 100
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.dist = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = None
        self.health = 8    # there are 9 stages of health; starting from heart_0 to heart_8 (death)
        self.move = 9
        self.score = 0

        self.scroll_background = False  # toggles automatic movement due to scrolling background; not working
        self.bg_move = 1                # rate of movement; not a 1:1 ratio with background movement, for some reason

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

        self.potions = potion_list

        # healing animation
        self.heal = False
        self.heal_frame = 0
        self.heal_images = []
        for i in range(0, 3):
            filename = "art/player/heal_" + str(i) + ".png"
            self.heal_images.append(pg.image.load(filename))

        # damage animation
        self.damage = False
        self.damage_frame = 0
        self.damage_images = []
        for i in range(0, 3):
            filename = "art/player/hurt_" + str(i) + ".png"
            self.damage_images.append(pg.image.load(filename))

        # self.attack_ready_rect = self.attack_ready_bar.get_rect(topleft=(200, 100))


        # hurtbox data
        self.hurtbox = pg.Rect(self.rect.x + 40, self.rect.y + 40, 30, 30)
        self.damage_cooldown = 0

        self.char_box = pg.sprite.Sprite()
        self.char_box.rect = pg.Rect(self.rect.x, self.rect.y, 30, 30)

    def calc_hitboxes(self):
        self.attack_box = pg.Rect(self.rect.x + 25, self.rect.y, 50, 50)
        self.hurtbox = pg.Rect(self.rect.x + 40, self.rect.y + 40, 30, 30)
        self.char_box.rect = pg.Rect(self.rect.x + 40, self.rect.y + 40, 30, 30)

    def update(self):
        self.handle_keys()
        self.handle_damage()
        self.handle_attack()

        # movement due to scrolling background; doesn't work due to conflict with handle_keys
        if self.scroll_background:
            self.rect.y += self.bg_move

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
        """ Handles Keys for movement """
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

        # Did this update cause us to hit a potion?
        potion_hit_list = pg.sprite.spritecollide(self, self.potions, False)
        for potion in potion_hit_list:
            if self.hurtbox.colliderect(potion):
                potion.kill()
                self.potions.remove(potion)
                if self.health < 8:
                    self.health += 1

        self.calc_hitboxes()

    def start_attack(self):
        """ Starts an attack """
        if not self.attack and self.attack_cooldown == 0:
            self.attack = True
            self.attack_frame = 0
            self.attack_cooldown = 100

    def handle_damage(self):
        """ Handles sprite display upon recovering/healing damage """
        # check for showing damage before healing
        if self.damage:
            if self.damage_frame < 3:
                self.image = self.damage_images[math.floor(self.damage_frame)]
                self.damage_frame += 0.5
            else:  # where damage_frame == 3, so end attack_ready animation
                self.damage = False
                self.damage_frame = 0
                self.image = pg.image.load("art/player/player_default.png")
        elif self.heal:
            if self.heal_frame < 3:
                self.image = self.heal_images[math.floor(self.heal_frame)]
                self.heal_frame += 0.5
            else:  # where heal_frame == 3, so end attack_ready animation
                self.heal = False
                self.heal_frame = 0
                self.image = pg.image.load("art/player/player_default.png")

        pass

    def handle_health(self):
        """ Handles sprite display depending on health """  # TODO: Remove? Health is part of HUD, not player

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1


    def take_damage(self):
        self.health -= 1
        self.damage_cooldown = 500


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
