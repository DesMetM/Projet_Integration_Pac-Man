import ctrl.ctrl
import pygame
import os

window = pygame.display.set_mode((672, 864))
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')))


def interface_debut():
    ''' Affiche l'interface qui donne le choix d'accéder au jeu en tant que joueur ou IA.
    Retourne vrai si le joueur à été sélectionner. '''
    return True


def mode_IA():
    '''Lance une partie avec l'IA.'''
    return 0


def mode_joueur():
    ctrl.ctrl.nouvelle_partie()

    quitter = False

    while not quitter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True

        window.blit(ctrl.ctrl.get_surface(0), (0, 0))
        pygame.display.update()
