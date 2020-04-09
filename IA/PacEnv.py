import gym
from modele.jeu import Jeu
from gym import spaces
import numpy as np
import pandas as pd
from modele.board import SCALING, DECALAGEX, DECALAGE, GRILLE_DE_JEU, Blinky, Pinky, Inky, Clyde
from math import ceil

class PacEnv(gym.Env):

    """
    Le df est un dataframe(Pandas) qui va contenir les infos que l'Ia a besoin, donc la position des fantômes,
    sa position(je crois), le score actuel, etc. Il gardera en mémoire le dernier score enregistré pour voir si son
    score a augmenté et ainsi déterminer sa récompense(Je ne crois pas que c'est ici que cela se fera tho)
    """
    __VIDE = 6
    __MUR = 1
    __POWER_PELLET = 8
    __POINT = 0
    __CLYDE = 2
    __PINKY = 3
    __BLINKY = 4
    __INKY = 5
    __PACMAN = 9
    __FANTOME_EFFRAYE = 7
    __BOARD_INIT = GRILLE_DE_JEU.copy()
    __FANTOMES = {Blinky: __BLINKY, Pinky: __PINKY, Inky: __INKY, Clyde: __CLYDE}

    def __init__(self, jeu):
        super(PacEnv, self).__init__()

        self.action_space = [0,1,2,3,4]
        self.jeu = jeu
        # self.observation_space = la grille. Reconstruite à chaque itération pour voir la position des fantomes, pellets etc
        self.observation_space = self.jeu.maGrille

    def __next_observation(self):
        self.observation_space = self.jeu.maGrille
        x, y = ceil((self.jeu.pacman.sprite.rect.x - DECALAGEX)/SCALING), ceil((self.jeu.pacman.sprite.rect.y - DECALAGE)/SCALING)
        self.observation_space[y, x] = self.__PACMAN

        for fantome in self.jeu.fantomes:
          x,y = ceil((fantome.sprite.rect.x-DECALAGEX)/SCALING), ceil((fantome.sprite.rect.y-DECALAGE)/SCALING)
          self.observation_space[y, x] = self.__FANTOMES[type(fantome)]

    def step(self, action):
        # Take action
          """Dans ce cas-ci, il faudrait feed au jeu l'action que l'IA a choisi. Il va choisir
          une valeur entre 0 et 3 qui représente chacun une direction"""
        # Determine new state
          """ On regarde ce que le move a fait. Est-ce Pac est mort? Est-ce que Pac a eu des points? Si oui cb?"""
        # Determine reward linked with outcome(?)
          """Dependemment du nouveau state, donc de ce qui s'est passé avec l'action, on attribue un reward. De base, 
          toute les actions ont une reward de -1 pour motiver l'IA à travailler rapidement. Il reste à déterminer
          ce que vaut de plus les autres résultats(mort, points, etc)"""
        # Determine if game finished
          """Vérifier si la partie est terminée. La partie est terminée si tous les points sont mangés ou si le Pac n'a
          plus de vies."""
        # Evaluate new state
          """Évalue son état actuel pour que le model puisse prendre la prochaine action"""
        # return new_state, reward, done, None

    def reset(self):
        # posPac, posFant, nbPts tous remis à depart
        pass

    def render(self, mode='human'):
        pass