from modele.jeu import Jeu
from vue.vue import Vue


# Classe contrôleur; passe l'information de la vue au modèle
class Ctrl:

    # constructeur du contrôleur
    def __init__(self):
        self.jeu = Jeu()
        self.vue = Vue(self)

    def start(self):
        mode_de_jeu = self.vue.interface_debut()

        # Si mode_de_jeu est vrai, alors on lance la partie en mode joueur. Sinon, on lance la partie en mode IA.
        self.jeu.nouvelle_partie()
        if mode_de_jeu:
            self.vue.mode_joueur()
        else:
            self.vue.mode_IA()

    def get_surface(self, direction):
        return self.jeu.get_surface(direction)

#    def kill_ready(self):
#        self.jeu.ready.sprite.kill()
