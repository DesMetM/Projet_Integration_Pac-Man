import pygame
from modele.direction import Direction
import os

window = pygame.display.set_mode((672, 864))


class Vue:
    def __init__(self, p_ctrl):
        self.ctrl = p_ctrl

    def interface_debut(self):
        ''' Affiche l'interface qui donne le choix d'accéder au jeu en tant que joueur ou IA.
        Retourne vrai si le joueur à été sélectionner. '''
        return True

    def mode_IA(self):
        '''Lance une partie avec l'IA.'''
        return 0

    def mode_joueur(self):
        """
        Crée les events pour que le joueur puisse puisse jouer
        :return:
        """

        quitter = False
        clock = pygame.time.Clock()
        clock.tick(40)
        pac_direction = Direction.AUCUNE
        key_pressed = []

        while not quitter:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quitter = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_pressed.append(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.append(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.append(Direction.DROITE)
                    if event.key == pygame.K_DOWN:
                        key_pressed.append(Direction.BAS)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        key_pressed.remove(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.remove(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.remove(Direction.DROITE)
                    if event.key == pygame.K_DOWN:
                        key_pressed.remove(Direction.BAS)

            if key_pressed:
                pac_direction = key_pressed[-1]
            else:
                pac_direction = Direction.AUCUNE

            window.blit(self.ctrl.get_surface(pac_direction), (0, 0))
            pygame.display.update()
