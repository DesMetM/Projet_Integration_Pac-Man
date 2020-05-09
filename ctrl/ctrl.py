from modele.jeu import Jeu
from vue.vue import Vue
from IA.environnement import PacEnv
from IA.agent_dqn import AgentDQN
import numpy as np


# Classe contrôleur; passe l'information de la vue au modèle
class Ctrl:
    """
    Cette classe est le contrôleur du jeu de Pac-Man. Elle est l'intermédiaire entre la vue et le modèle.
    """

    def __init__(self):
        """
        Constructeur de la classe. Instancie le jeu et la vue.
        """
        self.jeu = Jeu(Vue.FRAME_RATE)
        self.vue = Vue(self)
        self.agent = None
        self.env = None

    def start(self):
        """
        On demande à l'utilisateur ce qu'il veut faire et on démarre une nouvelle partie.
        :return: None
        """
        en_jeu = True

        while en_jeu:
            mode_de_jeu = self.vue.interface_debut()
            # Si mode_de_jeu est vrai, alors on lance la partie en mode joueur. Sinon, on lance la partie en mode IA.
            if mode_de_jeu == 3:
                break
            self.jeu.reset()

            if mode_de_jeu == 1 and self.vue.mode_joueur() or mode_de_jeu == 2 and self.vue.mode_IA():
                break

    def update_jeu(self, direction):
        """
        Le jeu passe à l'état suivant selon l'action qui a été fait.
        :param direction: L'action que le joueur veut faire.
        :return: Un tuple de bool. La première valeur désigne si la partie a été gagnée.
        La deuxième valeur désigne si la partie est relancée.
        """
        return self.jeu.update_jeu(direction)

    def update_jeu_test(self, direction):
        """
        Le jeu passe à l'état suivant selon l'action qui a été fait. Version Test de la méthode
        qui ne vas pas changer l'état des fantômes et ne prendra pas en compte les collisions avec ceux-ci
        :param direction: L'action que le joueur veut faire.
        :return: Un tuple de bool. La première valeur désigne si la partie a été gagnée.
        La deuxième valeur désigne si la partie est relancée.
        """
        return self.jeu.update_jeu_test(direction)

    def get_surface(self):
        """
        Construit l'image de l'état du jeu et la retourne.
        :return: None
        """
        return self.jeu.get_surface()

    def get_audio(self):
        """
        Retourne une liste de channel à activer.
        :return: une liste de channel à activer.
        """
        return self.jeu.get_audio()

    def load_agent_dqn(self, name):
        self.env = PacEnv(self.jeu)
        self.agent = AgentDQN(318, 4)
        self.agent.epsilon = 0.0
        self.agent.load(name)

    def printobs(self, mat):
        retour = ""
        mat = mat[0]
        mat = map(str, mat)
        for ligne in mat:
            for col in ligne:
                retour+= col
            retour+="\n"
        return retour

    def get_surface_dqn(self):
        action = self.agent.act(self.env.observation_space)
        next_observation, reward, done, info = self.env.step(action, fantome=True)
        surface, audio = self.env.render()
        return surface, audio, done, info[0]
