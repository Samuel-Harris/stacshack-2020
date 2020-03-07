# Import Modules
import random

import pygame as pg

from hud import HUD
from player import Player
from potion import Potion
from wall import Wall


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen_width = 800
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Bullet Hell Thing")
    pg.mouse.set_visible(0)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Put Text On The Background, Centered
    # if pg.font:
    #     font = pg.font.Font(None, 36)
    #     text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
    #     textpos = text.get_rect(centerx=background.get_width() / 2)
    #     background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    # pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    player = Player(screen_width, screen_height)
    hud = HUD(player)
    top_wall = Wall(0, 0, screen_width, 10)
    walls = pg.sprite.RenderPlain(top_wall)
    allsprites = pg.sprite.RenderPlain(player, walls, hud)
    player.walls = walls.sprites()

    # Main Loop
    going = True
    while going:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            # player attack
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.start_attack()

        if random.choice([True, False]):  # 50% chance to spawn a random HP bottle. TODO: Replace me with actual logic!
            allsprites.add(Potion())

        # player movement
        player.update()

        # draw
        # screen.fill((255, 255, 255))
        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

        clock.tick(60)

    pg.quit()


if __name__ == '__main__':
    main()
