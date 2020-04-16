from enum import Enum


class Mode(Enum):
    """
    Enum contenant les différents modes que les fantômes adopter durant la partie.
    """
    CHASSE = lambda fantome, jeu: fantome.mode_chasse(jeu)
    DISPERSION = lambda fantome, jeu: fantome.avancer()
    EFFRAYE = lambda fantome, jeu: fantome.mode_effraye()
    RETOUR = lambda fantome, jeu: fantome.retour_au_bercail()
    INACTIF = lambda fantome, jeu: Mode.inactif(fantome, jeu)
    SORTIR = lambda fantome, jeu: fantome.sortir(jeu)

    @staticmethod
    def inactif(fantome, jeu):
        """
        S'il y a assez de pastilles mangées dans le jeu, alors le fantôme passe en mode «sortir».
        :param fantome: Un fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        if fantome.nbr_activation < jeu.pastilles_mangees and fantome.ordre_sortie * jeu.timer_jeu.timer_sortie.marche <= jeu.timer_jeu.timer_sortie.compteur:
            fantome.mode = Mode.SORTIR
