import pygame
from modele.direction import Direction

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
        key_pressed = [False] * 4

        while not quitter:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quitter = True

                elif event.type == pygame.KEYDOWN:
                    #if self.ctrl.jeu.ready.alive():
                        #self.ctrl.jeu.ready.kill()
                    if event.key == pygame.K_LEFT:
                        key_pressed[Direction.GAUCHE.value] = True
                    if event.key == pygame.K_UP:
                        key_pressed[Direction.HAUT.value] = True
                    if event.key == pygame.K_RIGHT:
                        key_pressed[Direction.DROITE.value] = True
                    if event.key == pygame.K_DOWN:
                        key_pressed[Direction.BAS.value] = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        key_pressed[Direction.GAUCHE.value] = False
                    if event.key == pygame.K_UP:
                        key_pressed[Direction.HAUT.value] = False
                    if event.key == pygame.K_RIGHT:
                        key_pressed[Direction.DROITE.value] = False
                    if event.key == pygame.K_DOWN:
                        key_pressed[Direction.BAS.value] = False

            if any(key_pressed):
                for direction in Direction.__iter__():
                    if key_pressed[direction.value]:
                        pac_direction = direction
                        break
            else:
                pac_direction = Direction.AUCUNE

            window.blit(self.ctrl.get_surface(pac_direction), (0, 0))
            pygame.display.update()
