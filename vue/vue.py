import os

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
        board = pygame.image.load(os.path.join('ressource', 'images', 'Board_Intro.png'))

        player1 = pygame.image.load(os.path.join('ressource', 'images', 'PlayerOne.png'))
        player1_rect = player1.get_rect()
        player1_rect.topleft = (217,332)

        IA = pygame.image.load(os.path.join('ressource', 'images', 'Player_IA.png'))
        IA_rect= IA.get_rect()
        IA_rect.topleft = (285, 532)

        window.blit(board, (0,0))
        window.blit(player1, (217, 332))
        window.blit(IA, (285, 532))
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(pygame.mouse.get_pos()):
                        print(pygame.mouse.get_pos())
                        return True
                    elif IA_rect.collidepoint(pygame.mouse.get_pos()):
                        print('Ça lance le joueur 1 puisque l\'IA n\'est pas encore prêt :)')
                        return True

    def mode_IA(self):
        '''Lance une partie avec l'IA.'''
        return 0

    def mode_joueur(self):
        """
        Crée les events pour que le joueur puisse puisse jouer
        :return:
        """
        partie_commencer = False
        ready = pygame.image.load(os.path.join('ressource', 'images', 'Ready!.png'))
        quitter = False
        clock = pygame.time.Clock()
        clock.tick(40)
        pac_direction = Direction.AUCUNE
        key_pressed = []
        window.blit(self.ctrl.get_surface(Direction.AUCUNE), (0, 0))
        pygame.mixer.music.load(os.path.join('ressource', 'sons', 'Theme.wav'))
        pygame.mixer.music.play(-1)


        while not quitter:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quitter = True

                elif event.type == pygame.KEYDOWN:

                    partie_commencer = True

                    if event.key == pygame.K_LEFT:
                        key_pressed.append(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.append(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.append(Direction.DROITE)
                    if event.key == pygame.K_DOWN:

                        key_pressed.append(Direction.BAS)
                    if event.key == pygame.K_ESCAPE:
                        quitter = True


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        key_pressed.remove(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.remove(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.remove(Direction.DROITE)
                    if event.key == pygame.K_DOWN:

                        key_pressed.remove(Direction.BAS)
                    if event.key == pygame.K_ESCAPE:
                        quitter = True


            if key_pressed:
                pac_direction = key_pressed[-1]
            else:
                pac_direction = Direction.AUCUNE

            if not partie_commencer:
                window.blit(ready, (270, 485))
            else:
                window.blit(self.ctrl.get_surface(pac_direction), (0, 0))
                pygame.mixer.music.stop()

            pygame.display.update()
