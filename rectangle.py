import pygame


class Rectangle(pygame.sprite.Sprite):

    def __init__(self):
        super(Rectangle, self).__init__()
        self.image = pygame.Surface([16, 16])
        self.rect = pygame.Rect(0, 0, 16, 16)