import modele
import vue.vue as v

#Classe contrôleur; passe l'information de la vue au modèle
class Ctrl(object):

    #constructeur du contrôleur
    def __init__(self, model:modele.jeu.Jeu):
        self.currentJeu = None
        self.modele = model
        model.nouvelle_partie()
        self.vue = v.Vue(self)

    def start(self):
        mode_de_jeu = self.vue.interface_debut()

        # Si mode_de_jeu est vrai, alors on lance la partie en mode joueur. Sinon, on lance la partie en mode IA.
        self.nouvelle_partie()
        if mode_de_jeu:
            self.vue.mode_joueur()
        else:
            self.vue.mode_IA()


    def nouvelle_partie(self):
        self.currentJeu = modele.jeu.Jeu()
        self.currentJeu.nouvelle_partie()

    def get_surface(self, direction):
        return self.currentJeu.get_surface_drawn(direction)
