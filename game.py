# Import Modules
import os
import pygame as pg
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets")


# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound


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
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    # chimp = Chimp()
    # fist = Fist()
    # allsprites = pg.sprite.RenderPlain((fist, chimp))
    allsprites = pg.sprite.RenderPlain()

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
