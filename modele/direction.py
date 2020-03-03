from enum import Enum


class Direction(Enum):
    GAUCHE = 0
    HAUT = 1
    DROITE = 2
    BAS = 3
    AUCUNE = 4

    def get_vecteur(self):
        if self == Direction.GAUCHE:
            return [-1, 0]
        elif self == Direction.HAUT:
            return [0, -1]
        elif self == Direction.DROITE:
            return [1, 0]
        elif self == Direction.BAS:
            return [0, 1]

    def opposee(self):
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
