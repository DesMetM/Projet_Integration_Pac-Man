import modele
import vue.vue


def start():
    mode_de_jeu = vue.vue.interface_debut()

    # Si mode_de_jeu est vrai, alors on lance la partie en mode joueur. Sinon, on lance la partie en mode IA.
    if mode_de_jeu:
        vue.vue.mode_joueur()
    else:
        vue.vue.mode_IA()


def nouvelle_partie():
    modele.jeu.nouvelle_partie()


def get_surface(direction):
    return modele.jeu.get_surface(direction)
