# Import Modules
import pygame as pg

from player import Player


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((468, 60))
    pg.display.set_caption("Monkey Fever")
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
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    player = Player()
    allsprites = pg.sprite.RenderPlain(player)

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         going = False
        #     elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        #         going = False
        #     elif event.type == pg.MOUSEBUTTONDOWN:
        #         if fist.punch(chimp):
        #             punch_sound.play()  # punch
        #             chimp.punched()
        #         else:
        #             whiff_sound.play()  # miss
        #     elif event.type == pg.MOUSEBUTTONUP:
        #         fist.unpunch()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()
