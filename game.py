# Import Modules
from collections import defaultdict

import pygame
import pygame as pg
import random
import time

from sprites.enemy2 import Enemy2
from sprites.hud import HUD
from sprites.inventory import Inventory
from sprites.knife2 import Knife2
from sprites.player import Player
from sprites.potion import Potion
from sprites.potion2 import Potion2
from sprites.wall import Wall
from sprites.enemy import Enemy
from util.spawning import chance_spawn
from sprites.score_text import ScoreText

screen_width = 800
screen_height = 600


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    # Initialize Everything
    pg.mixer.init()
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Bullet Hell Thing")
    pg.mouse.set_visible(0)

    # Create The Background
    bg = pg.image.load("art/background/background.png")
    bg_offset = 0

    # Display The Background
    screen.blit(bg, (0, 0))
    # pg.display.flip()

    #
    pg.mixer.music.load('sound/music.wav')
    pg.mixer_music.play(-1)

    # Prepare Game Objects
    clock = pg.time.Clock()
    potion_list = []
    player = Player(screen_width, screen_height, potion_list)
    hud = HUD(player)
    inv = Inventory(player)

    invisible_top_wall = Wall(0, -35, screen_width, 10)
    invisible_bottom_wall = Wall(0, screen_height + 25, screen_width, 10)
    invisible_left_wall = Wall(-35, 0, 10, screen_height)
    invisible_right_wall = Wall(screen_width + 25, 0, 10, screen_height)
    top_wall = Wall(0, 0, screen_width, 10)
    bottom_wall = Wall(0, screen_height - 10, screen_width, 10)
    left_wall = Wall(0, 0, 10, screen_height)
    right_wall = Wall(screen_width - 10, 0, 10, screen_height)
    walls = pg.sprite.RenderPlain(top_wall, bottom_wall, left_wall, right_wall)
    collision_walls = pg.sprite.RenderPlain(invisible_top_wall, invisible_bottom_wall, invisible_left_wall,
                                            invisible_right_wall)
    allsprites = pg.sprite.RenderPlain(player, walls, collision_walls, hud, inv)
    player.walls = collision_walls.sprites()

    bullet_list = []

    enemy_list = []
    for enemy in enemy_list:
        allsprites.add(enemy)

    # Tracker
    item_count = defaultdict(lambda: 0)

    # Tracker specifically for special potion; and whether player holds it
    bomb_inuse = False
    bomb_counter = 0
    bomb_delay = 330

    # Shows the introduction screen
    story = "THE STORY SO FAR:"
    story2 = "In a world filled with swords, you are a superhero with a bow."
    story3 = "Swing your bow, kill enemies and eliminate swords."
    story4 = "Pick up health and a special potion along the way to make swords disappear!"
    story5 = "<TAB> to begin."

    start_game = False
    while not start_game:
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(story, 1, (0, 0, 0))
        text2 = font.render(story2, 1, (0, 0, 0))
        text3 = font.render(story3, 1, (0, 0, 0))
        text4 = font.render(story4, 1, (0, 0, 0))
        text5 = font.render(story5, 1, (0, 0, 0))

        text_pos = text.get_rect(centerx=screen.get_width() / 2, centery=100)
        text_pos2 = text2.get_rect(centerx=screen.get_width() / 2, centery=200)
        text_pos3 = text3.get_rect(centerx=screen.get_width() / 2, centery=300)
        text_pos4 = text4.get_rect(centerx=screen.get_width() / 2, centery=400)
        text_pos5 = text5.get_rect(centerx=screen.get_width() / 2, centery=500)

        screen.blit(text, text_pos)
        screen.blit(text2, text_pos2)
        screen.blit(text3, text_pos3)
        screen.blit(text4, text_pos4)
        screen.blit(text5, text_pos5)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                start_game = True
            else:
                continue

    # Main Loop
    going = True
    while going:
        # print(item_count[Enemy], item_count[Enemy2], item_count[Potion])

        # draw two backgrounds, slowly moving down
        screen.blit(bg, (0, bg_offset))
        screen.blit(bg, (0, bg_offset - screen_height))
        if bg_offset < screen_height:
            bg_offset += 1
        else:  # once offset goes off the screen, reset it
            bg_offset = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            # player attack
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.start_attack()

            # player bomb
            if player.bomb_ready and event.type == pg.KEYDOWN and event.key == pg.K_c:
                pg.mixer.Sound('sound/tactical-nuke.wav').play()
                bomb_inuse = True
                player.bomb_ready = False

        if bomb_inuse:
            if bomb_counter < bomb_delay:
                bomb_counter += 1
            else:
                player.bomb_count = 0
                print("BOOM")
                bomb_inuse = False
                bomb_counter = 0

                # remove all bullets
                for bullet in bullet_list:
                    bullet.kill()
                bullet_list.clear()
                allsprites.remove(bullet_list)

                # remove all enemies?
                for enemy in enemy_list:
                    enemy.kill()
                enemy_list.clear()
                allsprites.remove(enemy_list)
                item_count[Enemy] = 0
                item_count[Enemy2] = 0

        if random.random() < chance_spawn(item_count[Potion]):
            potion = Potion(screen_width, screen_height)
            potion_list.append(potion)
            allsprites.add(potion)
            item_count[Potion] = item_count[Potion] + 1

        if random.random() < chance_spawn(item_count[Enemy]):
            enemy = Enemy(screen_width, screen_height)
            enemy_list.append(enemy)
            allsprites.add(enemy)
            item_count[Enemy] = item_count[Enemy] + 1

        if item_count[Enemy2] <= 5 and random.random() < chance_spawn(item_count[Enemy2]):
            enemy = Enemy2(screen_width, screen_height)
            enemy_list.append(enemy)
            allsprites.add(enemy)
            item_count[Enemy2] = item_count[Enemy2] + 1

        # a special potion; if you need to collect 4, may as well have them spawn randomly
        if random.random() < 0.003:
            potion = Potion2(screen_width, screen_height)
            potion_list.append(potion)
            allsprites.add(potion)

        # update player (movement, attack frame, health)
        if not player.update():
            end_screen(screen, bg, player)

        if clock.get_time() % 5:
            for enemy in enemy_list:
                if player.attack and player.attack_box.colliderect(enemy.hurtbox):
                    enemy.kill_enemy(player)
                    enemy_list.remove(enemy)

                    if isinstance(enemy, Enemy):
                        item_count[Enemy] = item_count[Enemy] - 1
                    elif isinstance(enemy, Enemy2):
                        item_count[Enemy2] = item_count[Enemy2] - 1
                    allsprites.remove(enemy)  # TODO: Make enemies stay a while before being removed

                if player.hurtbox.colliderect(enemy.hurtbox):
                    if player.damage_cooldown == 0:
                        player.get_hurt()

                # remove if off screen; after calling 'implode' first on Enemy though
                if enemy.rect.y + 50 > screen_height:
                    if isinstance(enemy, Enemy):
                        bullets = enemy.implode(player.rect.x, screen_height)
                        for bullet in bullets:
                            bullet_list.append(bullet)
                            allsprites.add(bullet)

                    if isinstance(enemy, Enemy):
                        item_count[Enemy] = item_count[Enemy] - 1
                    elif isinstance(enemy, Enemy2):
                        item_count[Enemy2] = item_count[Enemy2] - 1

                    allsprites.remove(enemy)
                    enemy_list.remove(enemy)
                    enemy.kill()

                # get each enemy to go through a 'shoot' cycle; returns None if no bullet generated
                # bullet = None
                # if isinstance(enemy, Enemy):
                bullet = enemy.shoot(player.rect.x, player.rect.y)
                # elif isinstance(enemy, Enemy2):
                #     bullet = enemy.shoot(player.h)
                if bullet:
                    bullet_list.append(bullet)
                    allsprites.add(bullet)

            for bullet in bullet_list:
                remove = False
                # bigger hitbox collides with player attack
                if player.attack and player.attack_box.colliderect(bullet.rect):
                    remove = True
                # smaller hitbox collides with player
                elif player.hurtbox.colliderect(bullet.hurtbox):
                    if player.damage_cooldown == 0:
                        player.get_hurt()
                    remove = True
                # off screen; add 20 to coordinates to centre it (knife is 40x40 px)
                elif bullet.rect.x + 20 < 10 or bullet.rect.x + 20 > screen_width - 10 \
                        or bullet.rect.y + 20 < 10 or bullet.rect.y + 20 > screen_height - 10:
                    remove = True

                # cheeky bodge: homing
                if isinstance(bullet, Knife2):
                    xdist = abs(player.rect.x - bullet.rect.x)
                    if bullet.rect.x+40 < player.rect.x+50 - 20:
                        bullet.true_x += bullet.xspeed * xdist
                    elif bullet.rect.x+40 > player.rect.x+50 + 20:
                        bullet.true_x -= bullet.xspeed * xdist

                if remove:
                    bullet_list.remove(bullet)
                    allsprites.remove(bullet)
                    bullet.kill()

            # remove potions going off screen
            for potion in potion_list:
                if potion.rect.y > screen_height - 30:
                    if isinstance(potion, Potion2):
                        potion2_present = False
                    allsprites.remove(potion)
                    item_count[Potion] = item_count[Potion] - 1
                    potion_list.remove(potion)
                    potion.kill()

        # draw
        allsprites.update()

        # Draw Everything
        allsprites.draw(screen)
        # text_surface = score_text.generate_surface('Health: ')
        # screen.blit(text_surface,
        #             (screen_width - text_surface.get_width() - 100, screen_height - text_surface.get_height() - 45))
        pg.display.flip()

        clock.tick(60)

    pg.quit()


# when the player dies, this is called
def end_screen(screen, background, player):
    displaying_score = True
    final_score = player.score

    while displaying_score:
        pg.time.delay(100)

        screen.blit(background, (0, 0))
        font = pg.font.SysFont('Cambria', 80)
        final_score = font.render("Score:" + str(player.score), 1, (0, 0, 0))
        screen.blit(final_score, (screen_width / 2 - final_score.get_width(), 150))
        final_score = font.render("Try again! <Space>", 1, (0, 0, 0))
        screen.blit(final_score, ((screen_width / 2) - 200, 450))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                displaying_score = False
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                displaying_score = False
                player = None
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                displaying_score = False
                player = None
                break

    main()


if __name__ == '__main__':
    main()
