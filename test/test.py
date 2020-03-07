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
x_change = 0
y_change = 0
player_speed = 0

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
            elif event.key == pygame.K_DOWN:
                y_change = 5
            elif event.key == pygame.K_UP:
                y_change = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                y_change = 0

    x += x_change
    y += y_change

    game_display.fill((255, 255, 255))
    player(x, y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
