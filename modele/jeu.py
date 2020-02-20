import pygame
import os
import modele.board as board


class Jeu(object):


    def __init__(self):
        self.nouvelle_partie()
        self.currentPastilles = None
        self.currentPowerP = None
        self.pac = None
        self.fantomes = None
        self.count =0


    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.currentPastilles = board.pastille()
        self.currentPowerP = board.grosses_pastilles()
        self.pac = board.pac_init_pos()
        self.fantomes = board.fantomes_init_pos()
        return 0

    def get_surface_drawn(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''

        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.currentPastilles.draw(background)
        self.currentPowerP.draw(background)
        self.pac.draw(background)
        self.fantomes.draw(background)

        if self.count > 2:
            self.count = 0
            for s in self.currentPowerP:
                s.frame = (s.frame + 1) % 2
                s.image = s.images[s.frame]
        else:
            self.count += 1

        return background



