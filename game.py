# Import Modules
from collections import defaultdict

import pygame
import pygame as pg
import random

from sprites.hud import HUD
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

    # Prepare Game Objects
    clock = pg.time.Clock()
    potion_list = []
    player = Player(screen_width, screen_height, potion_list)
    hud = HUD(player)
    score_text = ScoreText(player)

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
    allsprites = pg.sprite.RenderPlain(player, walls, collision_walls, hud)
    player.walls = collision_walls.sprites()

    bullet_list = []

    enemy_list = []
    for enemy in enemy_list:
        allsprites.add(enemy)

    # Tracker
    item_count = defaultdict(lambda: 0)

    # Tracker specifically for special potion; and whether player holds it
    potion2_present = False

    # Shows the introduction screen
    story = """THE STORY SO FAR: \n
In a world of swords and sorcery, you are the only superhero with a bow. Now, you must swing your bow to defeat the \n
incoming bandits."""

    start_game = False
    while not start_game:
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(story, 1, (0, 0, 0))
        text_pos = text.get_rect(centerx=screen.get_width() / 2, centery=screen.get_height()/2)
        screen.blit(text, text_pos)
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
                potion2_present = False
                player.bomb_ready = False
                player.bomb_count = 0
                print("BOOM")

                # remove all bullets
                for bullet in bullet_list:
                    bullet.kill()
                bullet_list.clear()
                allsprites.remove(bullet_list)

                # # remove all enemies?
                # for enemy in enemy_list:
                #     enemy.kill()
                # enemy_list.clear()
                # allsprites.remove(enemy_list)
                # item_count[Enemy] = 0

        if random.random() < chance_spawn(item_count[Potion]):
            potion = Potion(screen_width, screen_height)
            potion_list.append(potion)
            allsprites.add(potion)
            item_count[Potion] = item_count[Potion] + 1

        if random.random() < chance_spawn(item_count[Enemy]):
            enemy = Enemy(screen_width, screen_height, player.rect.center)
            enemy_list.append(enemy)
            allsprites.add(enemy)
            item_count[Enemy] = item_count[Enemy] + 1

        # a special potion; if you need to collect 4, may as well have them spawn randomly
        if random.random() < 0.003:
            potion = Potion2(screen_width, screen_height)
            potion_list.append(potion)
            allsprites.add(potion)
            potion2_present = True
            print("bomb spawned")

        # update player (movement, attack frame, health)
        if not player.update():
            end_screen(screen, bg, player)

        if clock.get_time() % 5:
            for enemy in enemy_list:
                if player.attack and player.attack_box.colliderect(enemy.hurtbox):
                    enemy.kill_enemy(player)
                    enemy_list.remove(enemy)
                    item_count[Enemy] = item_count[Enemy] - 1
                    allsprites.remove(enemy)  # TODO: Make enemies stay a while before being removed

                if player.hurtbox.colliderect(enemy.hurtbox):
                    if player.damage_cooldown == 0:
                        player.get_hurt()

                # remove if off screen; after calling 'implode' first though
                if enemy.rect.y + 50 > screen_height:
                    if isinstance(enemy, Enemy):
                        bullets = enemy.implode(player.rect.x, screen_height)
                        for bullet in bullets:
                            bullet_list.append(bullet)
                            allsprites.add(bullet)

                    enemy_list.remove(enemy)
                    item_count[Enemy] = item_count[Enemy] - 1
                    allsprites.remove(enemy)
                    enemy.kill()

                # get each enemy to go through a 'shoot' cycle; returns None if no bullet generated
                bullet = enemy.shoot(player.rect.x + 50, player.rect.y + 50)
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

                if remove:
                    bullet_list.remove(bullet)
                    allsprites.remove(bullet)
                    bullet.kill()

            # remove potions going off screen
            for potion in potion_list:
                if potion.rect.y > screen_height-30:
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
        text_surface = score_text.generate_surface('Health: ')
        screen.blit(text_surface,
                    (screen_width - text_surface.get_width() - 90, screen_height - text_surface.get_height() - 54))
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
