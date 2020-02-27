import pygame
import os
from modele.direction import Direction
from modele.pacman import PacMan

# 28i x 30j
"""Grille représentant la position des murs, de espaces permis de déplacement et la position initiale des pellets et Power-pellets."""
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
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [3, 6, 6, 6, 6, 6, 0, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 0, 6, 6, 6, 6, 6, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1],
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
PORTAIL = 3
"""Variables nécessaires à l'initialisation du jeu. 
Comprends les positions de base, le décalage requis pour placer les entités sur le display 
et le facteur de mise à niveau pour faire correspondre la grille à l'affichage"""
SCALING = 24
DECALAGE = 85
DECALAGEX = 12
PACSPAWN = (14 * SCALING, 23 * SCALING + DECALAGE)
INKYSPAWN = (12 * SCALING, 14 * SCALING + DECALAGE)
PINKYSPAWN = (14 * SCALING, 14 * SCALING + DECALAGE)
CLYDESPAWN = (16 * SCALING, 14 * SCALING + DECALAGE)
BLINKYSPAWN = (14 * SCALING, 11 * SCALING + DECALAGE)
FANTOMES_SPAWN = {BLINKYSPAWN: 'Blinky', PINKYSPAWN: 'Pinky', INKYSPAWN: 'Inky', CLYDESPAWN: 'Clyde'}

"""Crée le groupe de pellets et les place à leur position de base selon la grille de jeu.
Le groupe sert à intéragir avec Pac-Man"""
def pastille():
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

"""Crée le groupe des fantômes et les place à leur position de  base selon la grille de jeu.
Le groupe sert à intéragir avec Pac-Man"""
def fantomes_init_pos():
    groupe = pygame.sprite.Group()
    for spawn in FANTOMES_SPAWN.keys():
        groupe.add(Fantome(spawn, FANTOMES_SPAWN[spawn]))
    return groupe

"""Vérifies si la position donnée est une entité donnée"""
def est_un(position, entite):
    return GRILLE_DE_JEU[position[1]][position[0]] == entite

    ''' rect = self.rect
     pos_grille = ((rect.left) // SCALING, (rect.centery - DECALAGE) // SCALING)
     if pos_grille == [0, 15]:
         self.pos = (20 + (self.vitesse[0]), self.pos[1] + (self.vitesse[1]))
/
     elif pos_grille == [28, 15]:
         self.pos = (650 + (self.vitesse[0]), self.pos[1] + (self.vitesse[1]))'''

"""Vérifies si le prochain pixel dans la trajectoire d'une entité dynamique est un mur"""
def collision_mur(rect, direction):
    if direction == Direction.GAUCHE:
        # Regarder si la position (rect.left,rect.y) **un coup ajusté a la grille** est un mur. on set la vitesse de pacman à 0.
        pos_grille = (rect.left // SCALING, (rect.centery - DECALAGE) // SCALING)
        return est_un(pos_grille, MUR)

    elif direction == Direction.DROITE:
        pos_grille = (rect.right // SCALING, (rect.centery - DECALAGE) // SCALING)
        return est_un(pos_grille, MUR)

    elif direction == Direction.HAUT:
        pos_grille = ((rect.centerx // SCALING), (rect.top - DECALAGE - 4) // SCALING + 1)
        return est_un(pos_grille, MUR)

    elif direction == Direction.BAS:
        pos_grille = (rect.centerx // SCALING, (rect.bottom - DECALAGE - 4) // SCALING)
        return est_un(pos_grille, MUR)
"""Vérifies si le prochain pixel dans la trajectoire d'une entité dynamique est un portail (Gros BS fait par nul autre que NikkyBee"""
def collision_portail(rect, direction):
        if direction == Direction.GAUCHE:
            # Regarder si la position (rect.left,rect.y) **un coup ajusté a la grille** est un mur. on set la vitesse de pacman à 0.
            pos_grille = (rect.left // SCALING, (rect.centery - DECALAGE) // SCALING)
            return est_un(pos_grille, PORTAIL)

        elif direction == Direction.DROITE:
            pos_grille = (rect.right // SCALING, (rect.centery - DECALAGE) // SCALING)
            return est_un(pos_grille, PORTAIL)

        elif direction == Direction.HAUT:
            pos_grille = ((rect.centerx // SCALING), (rect.top - DECALAGE - 4) // SCALING + 1)
            return est_un(pos_grille, PORTAIL)

        elif direction == Direction.BAS:
            pos_grille = (rect.centerx // SCALING, (rect.bottom - DECALAGE - 4) // SCALING)
            return est_un(pos_grille, PORTAIL)

"""Classe représentant un pellet. (Aussi appelé pastille) Est un enfant de pygame.Sprite"""
class Pastille(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'Pellet.png'))
        self.rect = self.image.get_rect(center=pos)

"""Classe représentant un Power-pellet. (Aussi appelé grosse pastille) Est un enfant de pygame.Sprite"""
class GrossePastille(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join('ressource', 'images', 'BigPellet.png')),
                       pygame.image.load(os.path.join('ressource', 'images', 'Empty.png'))]
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.isVisible = True

"""Classe représentant un fantôme. (À remplacer) Est un enfant de pygame.Sprite"""
class Fantome(pygame.sprite.Sprite):
    def __init__(self, pos, nom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(nom)))
        self.rect = self.image.get_rect(center=pos)
