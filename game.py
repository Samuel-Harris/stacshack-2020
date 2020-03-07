# Import Modules
from collections import defaultdict

import pygame as pg
import random

from sprites.hud import HUD
from sprites.player import Player
from sprites.potion import Potion
from sprites.wall import Wall
from sprites.enemy import Enemy
from util.spawning import chance_spawn


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

    # Create The Background
    # background = pg.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))
    bg = pg.image.load("art/background/background.png")
    bg_offset = 0

    # Put Text On The Background, Centered
    # if pg.font:
    #     font = pg.font.Font(None, 36)
    #     text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
    #     textpos = text.get_rect(centerx=background.get_width() / 2)
    #     background.blit(text, textpos)

    # Display The Background
    screen.blit(bg, (0, 0))
    # pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    potion_list = []
    player = Player(screen_width, screen_height, potion_list)
    hud = HUD(player)

    invisible_top_wall = Wall(0, -35, screen_width, 10)
    invisible_bottom_wall = Wall(0, screen_height + 25, screen_width, 10)
    invisible_left_wall = Wall(-35, 0, 10, screen_height)
    invisible_right_wall = Wall(screen_width + 25, 0, 10, screen_height)
    top_wall = Wall(0, 0, screen_width, 10)
    bottom_wall = Wall(0, screen_height - 10, screen_width, 10)
    left_wall = Wall(0, 0, 10, screen_height)
    right_wall = Wall(screen_width-10, 0, 10, screen_height)
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

    # Main Loop
    going = True
    while going:
        # draw two backgrounds, slowly moving down
        screen.blit(bg, (0, bg_offset))
        screen.blit(bg, (0, bg_offset - screen_height))
        if bg_offset < screen_height:
            bg_offset += 1
        else:   # once offset goes off the screen, reset it
            bg_offset = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            # player attack
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.start_attack()

        if random.random() < chance_spawn(item_count[Potion]):  # TODO: Replace me with actual logic!
            potion = Potion(screen_width, screen_height)
            potion_list.append(potion)
            allsprites.add(potion)
            item_count[Potion] = item_count[Potion] + 1

        if random.random() < chance_spawn(item_count[Enemy]):
            enemy = Enemy(screen_width, screen_height, player.rect.center)
            enemy_list.append(enemy)
            allsprites.add(enemy)
            item_count[Enemy] = item_count[Enemy] + 1

        # update player (movement, attack frame, health)
        player.update()

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

                # get each enemy to go through a 'shoot' cycle; returns None if no bullet generated
                bullet = enemy.shoot(player.rect.x+50, player.rect.y+50)
                if bullet:
                    bullet_list.append(bullet)
                    allsprites.add(bullet)

            for bullet in bullet_list:
                remove = False
                # hit by player attack
                if player.attack and player.attack_box.colliderect(bullet.hurtbox):
                    remove = True
                # hits player
                elif player.hurtbox.colliderect(bullet.hurtbox):
                    if player.damage_cooldown == 0:
                        player.get_hurt()
                    remove = True
                # off screen
                elif bullet.rect.x < 100 or bullet.rect.x > screen_width-100 \
                        or bullet.rect.y < 100 or bullet.rect.y > screen_height-100:
                    remove = True

                if remove:
                    bullet_list.remove(bullet)
                    bullet.kill()

        # draw
        allsprites.update()

        # Draw Everything
        allsprites.draw(screen)
        pg.display.flip()

        clock.tick(60)

    pg.quit()


if __name__ == '__main__':
    main()
