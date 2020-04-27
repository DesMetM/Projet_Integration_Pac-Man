import pygame
import os
from modele.direction import Direction
from modele.fantome import Blinky, Pinky, Inky, Clyde

# 28i x 31j
GRILLE_DE_JEU = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 8, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 8, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

VIDE = 6
MUR = 1
POWER_PELLET = 8
POINT = 0

SCALING = 24
DECALAGE = 85
DECALAGEX = 12
NOEUDS = set()  # Les coordonnées en pixel des intersections dans la grille.

NOEUDS.add(Blinky.SPAWN)


def is_node(x, y):
    """
    Valide si la position donnée est un noeud dans la grille de jeu.
    :param x: Position en x de la case à vérifier.
    :param y: Position en y de la case à vérifier.
    :return: «True» si et seulement si la case est un noeud dans la grille.
    """
    pas_un_mur = 0
    for dx in [-1, 1]:
        try:
            if GRILLE_DE_JEU[x + dx][y] != MUR:
                pas_un_mur += 1
                break
        except IndexError:
            pass

    for dy in [-1, 1]:
        try:
            if GRILLE_DE_JEU[x][y + dy] != MUR:
                pas_un_mur += 1
                break
        except IndexError:
            pass
    return pas_un_mur >= 2


for x in range(len(GRILLE_DE_JEU)):
    for y in range(len(GRILLE_DE_JEU[x])):
        if GRILLE_DE_JEU[x][y] != MUR and is_node(x, y):
            NOEUDS.add((y * SCALING + DECALAGEX, x * SCALING + DECALAGE))


def fantomes_init_pos():
    """
    Retourne un groupe de fantôme et l'instance de Blinky.
    :return: Un groupe de fantôme et l'instance de Blinky.
    """
    groupe = pygame.sprite.Group()
    blinky = Blinky()
    groupe.add(blinky, Pinky(), Inky(), Clyde())
    return groupe, blinky


def est_un_mur(position):
    """
    Vérifie selon la grille de jeu si la position donnée est un mur.
    :param position: une position dans la grille.
    :return: «True» si et seulement si c'est un mur.
    """
    try:
        return GRILLE_DE_JEU[position[1]][position[0]] == MUR
    except IndexError:
        return position[1] != 14


def tunnel(rect):
    """
    Regarde si un rectangle est sorti par la gauche ou la droite de la grille de jeu.
    Fais réapparaître le rectangle de l'autre côté.
    :param rect: Le rectangle (Pac-Man ou les fantômes) à observer.
    :return: None
    """
    if rect.x < -39:
        rect.y = 400
        rect.x = 681
    elif rect.x > 681:
        rect.y = 400
        rect.x = -39


def detecte_noeud(rect):
    """
    Retourne «True» si et seulement si le rectangle est sur un noeud dans la grille.
    :param rect: Le rectangle (Pac-Man ou les fantômes) à observer.
    :return: «True» si et seulement si le rectangle est sur un noeud dans la grille.
    """
    return rect.center in NOEUDS


def collision_mur(rect, direction):
    """
    Regarde s'il y a un mur devant le rectangle.
    :param rect: Le rectangle (Pac-Man ou les fantômes) à observer.
    :param direction: La direction du rectangle.
    :return: «True» si et seulement s'il y a un mur devant le rectangle.
    """
    if direction == Direction.GAUCHE:
        pos_grille = ((rect.left + 4) // SCALING, (rect.centery - DECALAGE) // SCALING)
        return est_un_mur(pos_grille) or not pos_grille[1] * SCALING == rect.centery - DECALAGE

    elif direction == Direction.DROITE:
        pos_grille = ((rect.right - 4) // SCALING, (rect.centery - DECALAGE) // SCALING)
        return est_un_mur(pos_grille) or not pos_grille[1] * SCALING == rect.centery - DECALAGE

    elif direction == Direction.HAUT:
        pos_grille = ((rect.centerx // SCALING), (rect.top - DECALAGE - 4) // SCALING + 1)
        return est_un_mur(pos_grille) or not pos_grille[0] * SCALING == rect.centerx - DECALAGEX

    elif direction == Direction.BAS:
        pos_grille = (rect.centerx // SCALING, (rect.bottom - DECALAGE + 4) // SCALING)
        return est_un_mur(pos_grille) or not pos_grille[0] * SCALING == rect.centerx - DECALAGEX


class Pastille(pygame.sprite.Sprite):
    """
    Cette classe contient l'image et la position d'une pastille.
    """
    IMAGE = pygame.image.load(os.path.join('ressource', 'images', 'Pellet.png'))

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Pastille.IMAGE
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def pastilles():
        """
        Crée le groupe de pastilles selon leur position dans la grille de jeu.
        :return: Un groupe de pastilles.
        """
        groupe = pygame.sprite.Group()
        for ligne in range(len(GRILLE_DE_JEU)):
            for col in range(len(GRILLE_DE_JEU[ligne])):
                if GRILLE_DE_JEU[ligne][col] == POINT:
                    groupe.add(Pastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
        return groupe


class GrossePastille(pygame.sprite.Sprite):
    """
    Cette classe contient l'image et la position d'une grosse pastille.
    """
    IMAGE = pygame.image.load(os.path.join('ressource', 'images', 'BigPellet.png'))

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = GrossePastille.IMAGE
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def grosses_pastilles():
        """
        Crée le groupe de grosses pastilles selon leur position dans la grille de jeu.
        :return: Un groupe de grosses pastilles.
        """
        groupe = pygame.sprite.Group()
        for ligne in range(len(GRILLE_DE_JEU)):
            for col in range(len(GRILLE_DE_JEU[ligne])):
                if GRILLE_DE_JEU[ligne][col] == POWER_PELLET:
                    groupe.add(GrossePastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
        return groupe


class Fruit(pygame.sprite.Sprite):
    POSITION = (13 * SCALING, 16 * SCALING + DECALAGE)

    def __init__(self, image, score):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=Fruit.POSITION)
        self.score = score

    @staticmethod
    def get_liste_fruits():
        return [Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')), 100),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Strawberry.png')), 200),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Apple.png')), 700),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Peach.png')), 500),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Peach.png')), 500),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Apple.png')), 700),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Grape.png')), 1000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Grape.png')), 1000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Galaxian.png')), 2000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Galaxian.png')), 2000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Bell.png')), 3000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Bell.png')), 3000),
                Fruit(pygame.image.load(os.path.join('ressource', 'images', 'Key.png')), 5000)]
