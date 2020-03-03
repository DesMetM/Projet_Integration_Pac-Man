from enum import Enum


class Mode(Enum):
    CHASSE = lambda fantome, jeu: fantome.mode_chasse(jeu)
    DISPERSION = lambda fantome, jeu: fantome.avancer()
    EFFRAYE = lambda fantome, jeu: fantome.mode_effraye()
    RETOUR = 3
    INACTIF = lambda fantome, jeu: Mode.inactif(fantome, jeu)
    SORTIR = lambda fantome, jeu: fantome.sortir()

    @staticmethod
    def inactif(fantome, jeu):
        if fantome.nbr_activation < jeu.pastilles_mangees:
            fantome.mode = Mode.SORTIR

