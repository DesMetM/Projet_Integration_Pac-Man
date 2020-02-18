import pygame
import os
import modele.board as board


class Jeu(object):


    def __init__(self):
        self.nouvelle_partie()
        self.currentPastilles = None
        self.currentPowerP = None


    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.currentPastilles = board.pastille()
        self.currentPowerP = board.grosses_pastilles()
        return 0



