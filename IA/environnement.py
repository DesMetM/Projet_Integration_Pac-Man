import gym
import numpy as np
from modele.board import SCALING, DECALAGEX, DECALAGE
from math import ceil
from modele.direction import Direction


class PacEnv(gym.Env):
    """
    Le df est un dataframe(Pandas) qui va contenir les infos que l'Ia a besoin, donc la position des fantômes,
    sa position(je crois), le score actuel, etc. Il gardera en mémoire le dernier score enregistré pour voir si son
    score a augmenté et ainsi déterminer sa récompense(Je ne crois pas que c'est ici que cela se fera tho)
    """

    __VIDE = 0
    __MUR = 1
    __POWER_PELLET = 6
    __POINT = 4

    __PACMAN = 9
    __FANTOME_EFFRAYE = 6
    __FANTOME = -9

    REWARD_MORT = -5
    REWARD_RIEN = -3
    REWARD_P = 1
    REWARD_PP = 2
    REWARD_F = 3
    REWARD_CLE = 5

    def __init__(self, jeu):
        """
        Initie l'environnement du réseau neuronal.
        :param jeu: L'objet jeu qui va permettre à l'environnement de repérer les informations dont il a besoin.
                    C'est-à-dire la position du Pac-Man, des fantômes, des pellets et des Power-Pellet.
        """
        super(PacEnv, self).__init__()
        self.action_space = [0, 1, 2, 3, 4]
        self.jeu = jeu
        self.observation_space = None
        self.last_score = 0
        self.__next_observation()

    def __next_observation(self):
        """
        Crée à nouveau l'observation_space pour prendre en compte la position des entitées importantes.
        """
        x_pacman, y_pacman = PacEnv.__position(self.jeu.pacman.sprite.rect)

        self.jeu.maGrille[y_pacman][x_pacman] = PacEnv.__VIDE

        self.observation_space = np.array(self.jeu.maGrille)

        self.observation_space[y_pacman][x_pacman] = self.__PACMAN

        for fantome in self.jeu.fantomes:
            x, y = PacEnv.__position(fantome.rect)

            if self.observation_space[y][x] != PacEnv.__MUR:
                if fantome.peur:
                    self.observation_space[y][x] = PacEnv.__FANTOME_EFFRAYE
                else:
                    self.observation_space[y][x] = PacEnv.__FANTOME

        self.observation_space = self.observation_space[self.observation_space != PacEnv.__MUR]
        self.observation_space = np.reshape(self.observation_space, (1, 1, 318))
        self.observation_space = self.observation_space.astype("float") / 9

        return x_pacman, y_pacman

    @staticmethod
    def __position(rect):
        x, y = ceil((rect.x - DECALAGEX) / SCALING), ceil((rect.y - DECALAGE) / SCALING)
        if x < 0:
            x = 0
        elif x > 27:
            x = 27
        return x, y

    def calculer_score(self):
        """
        Calcule le reward de l'observation actuel.
        :return: le reward de l'observation actuel.
        """
        delta_score = self.jeu.score - self.last_score

        if not self.jeu.pacman.sprite.is_alive:
            reward = PacEnv.REWARD_MORT
        elif delta_score == 0:
            reward = PacEnv.REWARD_RIEN
        elif 0 < delta_score < 30:
            reward = PacEnv.REWARD_P
        elif 30 <= delta_score < 70:
            reward = PacEnv.REWARD_PP
        elif 180 <= delta_score < 1620:
            reward = PacEnv.REWARD_F
        else:
            reward = PacEnv.REWARD_CLE

        self.last_score = self.jeu.score
        return reward

    def step(self, action: int, fantome=True):
        # Take action
        if fantome:
            self.jeu.update_jeu(Direction(action))
        else:
            self.jeu.update_jeu_test(Direction(action))

        # Determine new state
        info = self.jeu.pacman.sprite.is_alive, self.__next_observation()

        # Determine reward linked with outcome(?)
        if action != 4:
            reward = self.calculer_score()
        else:
            reward = 0

        # Determine if game finished
        done = self.jeu.pacman.sprite.nbr_vie == 0
        return self.observation_space, reward, done, info

    def reset(self):
        """
        Reset l'environnement et la partie en cours. Remets les entitées importantes à leurs positions de base.
        Mets le nombre de vies de Pac-Man à 4, reset le score et reset les sons.
        Ensuite, il observe la grille fraichement crée et la prends en mémoire.
        :return:
        """
        self.jeu.reset()
        self.__next_observation()
        return self.observation_space

    def render(self, mode='human'):
        """
        Retourne le frame du jeu et les channels actifs.
        :param mode: Peu importe.
        :return: le frame du jeu et les channels actifs.
        """
        return self.jeu.get_surface(), self.jeu.get_audio()
