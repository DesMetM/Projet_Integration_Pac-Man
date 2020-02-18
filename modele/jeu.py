import pygame
import os


def nouvelle_partie():
    '''Reset tout pour une nouvelle partie.'''
    return 0


def get_surface(direction) -> pygame.Surface:
    '''Point d'entrée du ctrl.'''

    background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))

    return background
