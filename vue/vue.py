import ctrl.ctrl
import pygame
import os

window = pygame.display.set_mode((672, 864))
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')))

class Vue(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl


    def interface_debut(self):
        ''' Affiche l'interface qui donne le choix d'accéder au jeu en tant que joueur ou IA.
        Retourne vrai si le joueur à été sélectionner. '''
        return True


    def mode_IA(self):
        '''Lance une partie avec l'IA.'''
        return 0

    def get_surface(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''

        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.ctrl.modele.currentPastilles.draw(background)
        self.ctrl.modele.currentPowerP.draw(background)
        self.ctrl.modele.pac.draw(background)
        self.ctrl.modele.fantomes.draw(background)

        return background


    def mode_joueur(self):

        quitter = False

        while not quitter:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitter = True

            window.blit(self.ctrl.vue.get_surface(0), (0, 0))
            pygame.display.update()
