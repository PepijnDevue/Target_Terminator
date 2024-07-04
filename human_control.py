from human_rendering import Human_rendering

import pygame


class Human_control(Human_rendering):
    def __init__(
        self, 
        window_size: tuple, 
        random_target: bool=False, 
        random_agent: bool=False
    )-> None:
        super().__init__(
            window_size=window_size,
            random_target=random_target, 
            random_agent=random_agent
        )

    def step(self, action=0):
        action = 0 # action parameter not used for this mode
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print("uppies")
            action = 1
        if keys[pygame.K_DOWN]:
            print("down with the empire")
            action = 2
        if keys[pygame.K_RIGHT]:
            print("rightwing")
            action = 3
        if keys[pygame.K_LEFT]:
            print("leftwing")
            action = 4
        if keys[pygame.K_SPACE]:
            print("pew pew")
            action = 5
        
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.close()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             print("uppies")
        #             action = 1
        #         if event.key == pygame.K_DOWN:
        #             print("down with the empire")
        #             action = 2
        #         if event.key == pygame.K_LEFT:
        #             print("rightwing")
        #             action = 3
        #         if event.key == pygame.K_RIGHT:
        #             print("leftwing")
        #             action = 4
        #         if event.key == pygame.K_SPACE:
        #             print("pew pew")
        #             action = 5

        return super().step(action=action)

