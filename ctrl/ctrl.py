from modele.jeu import Jeu
from vue.vue import Vue


# Classe contrôleur; passe l'information de la vue au modèle
class Ctrl:
    """
    Cette classe est le contrôleur du jeu de Pac-Man. Elle est l'intermédiaire entre la vue et le modèle.
    """

    def __init__(self):
        """
        Constructeur de la classe. Instancie le jeu et la vue.
        """
        self.jeu = Jeu()
        self.vue = Vue(self)

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
            self.jeu.nouvelle_partie(Vue.FRAME_RATE)
            self.jeu.pacman.sprite.nbr_vie = 3
            self.jeu.fruits_mangees = 0
            self.jeu.score = 0
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
