import gym
from modele.jeu import Jeu
from gym import spaces
import numpy as np
import pandas as pd
from modele.board import SCALING, DECALAGEX, DECALAGE, GRILLE_DE_JEU, Blinky, Pinky, Inky, Clyde
from math import ceil
from vue import vue
from modele.direction import Direction


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

    __FANTOMES = {Blinky: __BLINKY, Pinky: __PINKY, Inky: __INKY, Clyde: __CLYDE}

    __BOARD_INIT = GRILLE_DE_JEU.copy()

    REWARD_RIEN = -1
    REWARD_P = 0
    REWARD_PP = 1
    REWARD_F = 3
    REWARD_CLE = 5

    def __init__(self, jeu, vue):
        """
        Initie l'environnement du réseau neuronal.
        :param jeu: L'objet jeu qui va permettre à l'environnement de repérer les informations dont il a besoin.
                    C'est-à-dire la position du Pac-Man, des fantômes, des pellets et des Power-Pellet.
        """
        super(PacEnv, self).__init__()
        self.action_space = [0, 1, 2, 3, 4]
        self.action_space = np.reshape(self.action_space, (1, 5))
        self.action_space = self.action_space.T
        self.jeu = jeu
        self.observation_space = []
        self.__next_observation()
        self.vue = vue

    def __next_observation(self):
        """
        Crée à nouveau l'observation_space pour prendre en compte la position des entitées importantes.
        """
        self.last_obs = [self.observation_space, self.jeu.score]
        self.observation_space = self.jeu.maGrille
        x, y = ceil((self.jeu.pacman.sprite.rect.x - DECALAGEX) / SCALING), ceil(
            (self.jeu.pacman.sprite.rect.y - DECALAGE) / SCALING)
        self.observation_space[y, x] = self.__PACMAN

        for fantome in self.jeu.fantomes:
            x, y = ceil((fantome.sprite.rect.x - DECALAGEX) / SCALING), ceil(
                (fantome.sprite.rect.y - DECALAGE) / SCALING)
            self.observation_space[y, x] = self.__FANTOMES[type(fantome)]

        self.observation_space = np.reshape(self.observation_space, (1, 840))
        self.observation_space = self.observation_space.T

    def calculer_score(self):
        Dscore = self.jeu.score - self.last_obs[1]

        if not self.jeu.pacman.sprite.is_alive:
            return -5

        elif Dscore == 0:
            return PacEnv.REWARD_RIEN

        elif Dscore > 0 and Dscore < 30:
            return PacEnv.REWARD_P

        elif Dscore >= 30 and Dscore < 70:
            return PacEnv.REWARD_PP

        elif Dscore >= 180 and Dscore <= 1620:
            return PacEnv.REWARD_F

        else:
            return PacEnv.REWARD_CLE

    def step(self, action):
        # Take action
        """Dans ce cas-ci, il faudrait feed au jeu l'action que l'IA a choisi. Il va choisir
          une valeur entre 0 et 3 qui représente chacun une direction"""
        self.jeu.update_jeu(Direction.value[action])
        # Determine new state
        """ On regarde ce que le move a fait. Est-ce Pac est mort? Est-ce que Pac a eu des points? Si oui cb?"""
        self.__next_observation()
        # Determine reward linked with outcome(?)
        """Dependemment du nouveau state, donc de ce qui s'est passé avec l'action, on attribue un reward. De base, 
          toute les actions ont une reward de -1 pour motiver l'IA à travailler rapidement. Il reste à déterminer
          ce que vaut de plus les autres résultats(mort, points, etc)"""
        if action != 4:
            reward = self.calculer_score()
        else:
            reward = 0
        # Determine if game finished
        """Vérifier si la partie est terminée. La partie est terminée si tous les points sont mangés ou si le Pac n'a
          plus de vies."""
        done = self.jeu.pacman.sprite.nbr_vie == 0 or len(self.jeu.pastilles) + len(self.jeu.power_pellets) == 0
        return self.observation_space, reward, done, self.jeu.pacman.sprite.is_alive

    def reset(self):
        """
        Reset l'environnement et la partie en cours. Remets les entitées importantes à leurs positions de base.
        Mets le nombre de vies de Pac-Man à 4, reset le score et reset les sons.
        Ensuite, il observe la grille fraichement crée et la prends en mémoire.
        :return:
        """
        self.jeu.nouvelle_partie()
        self.jeu.pacman.sprite.nbr_vie = 4
        self.jeu.score = 0
        self.jeu.channel_actif = [False for x in range(len(self.jeu.channel_actif))]

        self.__next_observation()

    def render(self, mode='human'):
        pass
