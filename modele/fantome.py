import pygame
import os


class Fantome(pygame.sprite.Sprite):
    def __init__(self, pos, nom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(nom)))
        self.rect = self.image.get_rect(center=pos)
