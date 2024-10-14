import pygame
import numpy as np


def run(entities):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    running = True
    dt = 0
    center = np.array((screen.get_width() / 2, screen.get_height() / 2))

    airplane_sprites = []
    target_sprites = []
    bullet_sprites = []

    # for airplane in entities.scalars[entities.scalars[:,10]==0]:
    #     sprite = pygame.transform.scale(
    #         pygame.image.load("assets/i16_falangist.png"),
    #         [48,24],
    #     )
    #     airplane_sprites.append(sprite)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("white")

        action = 0
        actions = []
        keys = pygame.key.get_pressed()
        # right = pitch down
        if keys[pygame.K_RIGHT]:
            action = 2
        # left = pitch up
        elif keys[pygame.K_LEFT]:
            action = 1
        # up = throttle up
        if keys[pygame.K_UP]:
            action = 3
        # down = throttle down
        elif keys[pygame.K_DOWN]:
            action = 4
        # space = shoot a bullet
        elif keys[pygame.K_SPACE]:
            action = 5

        actions = np.array([[0,action]])
        entities.tick(dt,actions)


        # player.pos[0] = player.pos[0] % screen.get_width()
        # player.pos[1] = player.pos[1] % screen.get_height()
        # screen.blit(player.rot_sprite, player.rot_rect)

        for bullet in entities.vectors[entities.scalars[:,11]==2,3]:
            pygame.draw.circle(screen, 'black', bullet, 1)

        pygame.draw.circle(screen, 'black', entities.vectors[0,3], 6)
        c = 10
        pygame.draw.line(screen, 'black', center, center + entities.vectors[0,2])
        pygame.draw.line(screen, 'red', center, center + entities.vectors[0,6]/c)
        pygame.draw.line(screen, 'blue', center, center + entities.vectors[0,7]/c)
        pygame.draw.line(screen, 'green', center, center + entities.vectors[0,8]/(c**2))
        pygame.draw.line(screen, 'yellow', center, center + entities.vectors[0,5]/(c**2))
        #
        screen.blit(font.render('AoA:             ' + str(entities.scalars[:2,10]), False, 'black'), (20, 20))
        screen.blit(font.render('pitch:           ' + str(entities.scalars[:2,8]), False, 'black'), (20, 40))
        screen.blit(font.render('action:          ' + str(entities.scalars[:2,13]), False, 'black'), (20, 60))
        screen.blit(font.render('throttle:        ' + str(entities.scalars[:2,7]), False, 'black'), (20, 80))
        # screen.blit(font.render('speed:             ' + str(-player.pos[1]), False, 'black'), (20, 100))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()
