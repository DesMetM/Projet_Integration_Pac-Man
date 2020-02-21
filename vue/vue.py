import ctrl.ctrl
import pygame
import os

window = pygame.display.set_mode((672, 864))
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')))

class Vue(object):

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

        quitter = False
        clock = pygame.time.Clock()
        pac_direction = 0

        while not quitter:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quitter = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pac_direction = 0
                    if event.key == pygame.K_UP:
                        pac_direction = 1
                    if event.key == pygame.K_RIGHT:
                        pac_direction = 2
                    if event.key == pygame.K_DOWN:
                        pac_direction = 3


                    if pac_direction == 0:
                        img = self.ctrl.currentJeu.pac.sprite.left_images[0]
                    elif pac_direction == 1:
                        img = self.ctrl.currentJeu.pac.sprite.up_images[0]
                    elif pac_direction == 2:
                        img = self.ctrl.currentJeu.pac.sprite.right_images[0]
                    else:
                        img = self.ctrl.currentJeu.pac.sprite.down_images[0]
                    self.ctrl.currentJeu.pac.sprite.image =img


            window.blit(self.ctrl.get_surface(pac_direction), (0, 0))
            pygame.display.update()
            clock.tick(40)
