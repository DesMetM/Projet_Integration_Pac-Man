from enum import Enum


class Mode(Enum):
    CHASSE = lambda fantome, jeu: fantome.mode_chasse(jeu)
    DISPERSION = 1
    EFFRAYE = 2
    RETOUR = 3
    INACTIF = lambda fantome, jeu: Mode.inactif(fantome, jeu)
    SORTIR = 5

    @staticmethod
    def inactif(fantome, jeu):
        if fantome.nbr_activation < jeu.pastilles_mangees:
            fantome.mode = Mode.DISPERSION


"""
class Mode(Enum):
    CHASSE = 0
    DISPERSION = 1
    EFFRAYE = 2
    RETOUR = 3
    INACTIF = 4
    SORTIR = 5"""
