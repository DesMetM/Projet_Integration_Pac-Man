from enum import Enum


class Direction(Enum):
    """
    Enum contenant les différentes actions que l'utilisateur peut faire.
    Cet enum est aussi utile pour connaître la direction des sprites.
    """
    GAUCHE = 0
    HAUT = 1
    DROITE = 2
    BAS = 3
    AUCUNE = 4

    def get_vecteur(self):
        """
        Retourne le vecteur unitaire de la direction.
        :return: le vecteur unitaire de la direction.
        """
        if self == Direction.GAUCHE:
            return [-1, 0]
        elif self == Direction.HAUT:
            return [0, -1]
        elif self == Direction.DROITE:
            return [1, 0]
        elif self == Direction.BAS:
            return [0, 1]

    def opposee(self):
        """
        Retourne la direction opposée à cette direction (self).
        :return: la direction opposée à cette direction (self).
        """
        if self == Direction.GAUCHE:
            return Direction.DROITE
        elif self == Direction.HAUT:
            return Direction.BAS
        elif self == Direction.DROITE:
            return Direction.GAUCHE
        elif self == Direction.BAS:
            return Direction.HAUT
        else:
            return Direction.AUCUNE
