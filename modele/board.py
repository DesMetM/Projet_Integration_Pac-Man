import pygame
import os
from modele.direction import Direction
from modele.pacman import PacMan
from modele.fantome import Blinky, Pinky, Inky, Clyde

# 28i x 30j
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
PACSPAWN = (14 * SCALING, 23 * SCALING + DECALAGE)
READYSPAWN = (14 * SCALING, 17 * SCALING + DECALAGE)
NOEUDS = set()

NOEUDS.add(Blinky.SPAWN)


def is_node(x, y):
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

"""Crée le groupe de pellets et les place à leur position de base selon la grille de jeu.
Le groupe sert à intéragir avec Pac-Man"""


def pastilles():
    groupe = pygame.sprite.Group()
    for ligne in range(len(GRILLE_DE_JEU)):
        for col in range(len(GRILLE_DE_JEU[ligne])):
            if GRILLE_DE_JEU[ligne][col] == POINT:
                groupe.add(Pastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
    return groupe


"""Crée le groupe de Power-pellets et les place à leur position de base selon la grille ed jeu
Le groupe sert à intéragir avec Pac-Man"""


def grosses_pastilles():
    groupe = pygame.sprite.Group()
    for ligne in range(len(GRILLE_DE_JEU)):
        for col in range(len(GRILLE_DE_JEU[ligne])):
            if GRILLE_DE_JEU[ligne][col] == POWER_PELLET:
                groupe.add(GrossePastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
    return groupe


"""Crée une instance de Pac-Man et lui fait un groupe personnel pour le controller à partir des autres classes."""


def pac_init_pos():
    groupe = pygame.sprite.GroupSingle()
    groupe.add(PacMan(PACSPAWN))
    return groupe


def fantomes_init_pos():
    groupe = pygame.sprite.Group()
    blinky = Blinky()
    groupe.add(blinky, Pinky(), Inky(), Clyde())
    return groupe, blinky


"""Vérifies si la position donnée est une entité donnée"""


def est_un_mur(position):
    try:
        return GRILLE_DE_JEU[position[1]][position[0]] == MUR
    except IndexError:
        return position[1] != 14


def tunnel(rect):
    if rect.x < -39:
        rect.y = 400
        rect.x = 681
    elif rect.x > 681:
        rect.y = 400
        rect.x = -39


def detecte_noeud(rect):
    return rect.center in NOEUDS


"""Vérifies si le prochain pixel dans la trajectoire d'une entité dynamique est un mur"""


def collision_mur(rect, direction):
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
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'Pellet.png'))
        self.rect = self.image.get_rect(center=pos)


class GrossePastille(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join('ressource', 'images', 'BigPellet.png')),
                       pygame.image.load(os.path.join('ressource', 'images', 'Empty.png'))]
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.isVisible = True
