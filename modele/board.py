import pygame
import os

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
    [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6],
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
SCALING = 24
DECALAGE = 85
DECALAGEX = 12
PACSPAWN = (14*SCALING,23*SCALING+DECALAGE)
INKYSPAWN = (12*SCALING, 14*SCALING+DECALAGE)
PINKYSPAWN = (14*SCALING, 14*SCALING+DECALAGE)
CLYDESPAWN = (16*SCALING, 14*SCALING+DECALAGE)
BLINKYSPAWN = (14*SCALING, 11*SCALING+DECALAGE)
FANTOMES_SPAWN = {BLINKYSPAWN:'Blinky', PINKYSPAWN:'Pinky', INKYSPAWN:'Inky', CLYDESPAWN:'Clyde'}


def pastille():
    groupe = pygame.sprite.Group()
    for ligne in range(len(GRILLE_DE_JEU)):
        for col in range(len(GRILLE_DE_JEU[ligne])):
            if GRILLE_DE_JEU[ligne][col] == POINT:
                groupe.add(Pastille((col * SCALING + DECALAGEX, ligne * SCALING  + DECALAGE)))
    return groupe


def grosses_pastilles():
    groupe = pygame.sprite.Group()
    for ligne in range(len(GRILLE_DE_JEU)):
        for col in range(len(GRILLE_DE_JEU[ligne])):
            if GRILLE_DE_JEU[ligne][col] == POWER_PELLET:
                groupe.add(GrossePastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
    return groupe

def pac_init_pos():
    groupe = pygame.sprite.GroupSingle()
    groupe.add(PacMan(PACSPAWN))
    return groupe

def fantomes_init_pos():
    groupe = pygame.sprite.Group()
    for spawn in FANTOMES_SPAWN.keys():
        groupe.add(Fantome(spawn, FANTOMES_SPAWN[spawn]))
    return groupe


class Pastille(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'Pellet.png'))
        self.rect = self.image.get_rect(center=pos)


class GrossePastille(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join('ressource', 'images', 'BigPellet.png')), pygame.image.load(os.path.join('ressource', 'images', 'Empty.png'))]
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.isVisible = True

class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = [PACSPAWN[0],PACSPAWN[1]]
        """Direction (en attendant l'enum) : 0 = Left   1 = Up    2 = Right   3 = Down"""
        self.direction = 0
        self.GoLeft = [-1,0]
        self.GoUp = [0,1]
        self.GoRight = [1,0]
        self.GoDown = [0,-1]
        self.vitesse = [0,0]

    def update(self):
        if self.direction == 0:
            self.vitesse = self.GoLeft
        elif self.direction == 1:
            self.vitesse = self.GoUp
        elif self.direction == 2:
            self.vitesse = self.GoRight
        elif self.direction == 3:
            self.vitesse = self.GoDown

        print('Works{}'.format(self.direction))
        self.rect.move(self.vitesse[0], self.vitesse[1])


class Fantome(pygame.sprite.Sprite):
    def __init__(self, pos, nom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(nom)))
        self.rect = self.image.get_rect(center=pos)
