from builtins import print

import pygame
import os
import modele.board as board


# permet de partir une nouvelle partie avec les éléments
class Jeu(object):

    def __init__(self):
        self.nouvelle_partie()
        self.currentPastilles = None
        self.currentPowerP = None
        self.pac = None
        self.fantomes = None
        self.count = 0
        self.count_pac = 0
        self.count_pastille_manger = 0

    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.currentPastilles = board.pastille()
        self.currentPowerP = board.grosses_pastilles()
        self.pac = board.pac_init_pos()
        self.fantomes = board.fantomes_init_pos()
        return 0

    def get_surface_drawn(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        if pygame.sprite.groupcollide(groupa=self.pac, groupb=self.currentPastilles, dokilla=False, dokillb=True):
            self.count_pastille_manger += 1
            print(self.count_pastille_manger)

        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.currentPastilles.draw(background)
        self.currentPowerP.draw(background)
        self.pac.update(direction)
        self.pac.draw(background)
        self.fantomes.draw(background)

        if self.count > 2:
            self.count = 0
            for s in self.currentPowerP:
                s.frame = (s.frame + 1) % 2
                s.image = s.images[s.frame]
        else:
            self.count += 1

        if self.count_pac > 2:
            self.count_pac = 0
            for s in self.pac:
                s.frame = (s.frame + 1) % 2
                if direction == 0:
                    s.image = s.left_images[s.frame]
                elif direction == 1:
                    s.image = s.up_images[s.frame]
                elif direction == 2:
                    s.image = s.right_images[s.frame]
                elif direction == 3:
                    s.image = s.down_images[s.frame]
        else:
            self.count_pac += 1

        return background
