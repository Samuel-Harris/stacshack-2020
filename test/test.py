import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('test game')
clock = pygame.time.Clock()

crashed = False
player_img = pygame.image.load('../art/player/player_default.png')


def player(x, y):
    game_display.blit(player_img, (x, y))


x = (display_width * 0.25)
y = (display_height * 0.2)
direction = None
player_speed = 0


def player_move(direction, x, y):
    if direction:
        if direction == pygame.K_UP:
            y -= 5
        elif direction == pygame.K_DOWN:
            y += 5
        if direction == pygame.K_LEFT:
            x -= 5
        elif direction == pygame.K_RIGHT:
            x += 5
    return x, y


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        # player movement
        if event.type == pygame.KEYDOWN:
            direction = event.key
        if event.type == pygame.KEYUP:
            if event.key == direction:
                direction = None

    x, y = player_move(direction, x, y)

    # draw
    game_display.fill((255, 255, 255))
    player(x, y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
