import pygame as pg


class Wall(pg.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pg.Surface([width, height])
        self.image.fill((0, 0, 0))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
