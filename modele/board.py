import pygame
import os

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
PACSPAWN = (14 * SCALING, 23 * SCALING + DECALAGE)
INKYSPAWN = (12 * SCALING, 14 * SCALING + DECALAGE)
PINKYSPAWN = (14 * SCALING, 14 * SCALING + DECALAGE)
CLYDESPAWN = (16 * SCALING, 14 * SCALING + DECALAGE)
BLINKYSPAWN = (14 * SCALING, 11 * SCALING + DECALAGE)
FANTOMES_SPAWN = {BLINKYSPAWN: 'Blinky', PINKYSPAWN: 'Pinky', INKYSPAWN: 'Inky', CLYDESPAWN: 'Clyde'}


def pastille():
    groupe = pygame.sprite.Group()
    for ligne in range(len(GRILLE_DE_JEU)):
        for col in range(len(GRILLE_DE_JEU[ligne])):
            if GRILLE_DE_JEU[ligne][col] == POINT:
                groupe.add(Pastille((col * SCALING + DECALAGEX, ligne * SCALING + DECALAGE)))
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


def est_un_mur(position):
    pacman = PacMan
    try:
        #print(position)
        #print(GRILLE_DE_JEU[position[1]][position[0]])
        return GRILLE_DE_JEU[position[1]][position[0]] == MUR
    except IndexError:
        if position[1] > 15:
            pacman.pos((20, 432))
            print("position changé")
        else:
            pacman.pos((650, 432))
            print("position changé")

    ''' rect = self.rect
     pos_grille = ((rect.left) // SCALING, (rect.centery - DECALAGE) // SCALING)
     if pos_grille == [0, 15]:
         self.pos = (20 + (self.vitesse[0]), self.pos[1] + (self.vitesse[1]))

     elif pos_grille == [28, 15]:
         self.pos = (650 + (self.vitesse[0]), self.pos[1] + (self.vitesse[1]))'''


def collision_mur(pacman):
    rect = pacman.rect
    d = pacman.direction

    if d == 0:  # Left
        # Regarder si la position (rect.left,rect.y) **un coup ajusté a la grille** est un mur. on set la vitesse de pacman à 0.
        pos_grille = ((rect.centerx) // SCALING - 1, (rect.centery - DECALAGE) // SCALING)
        return est_un_mur(pos_grille)

    elif d == 2:  # Right
        pos_grille = ((rect.centerx - 4) // SCALING + 1, (rect.centery - DECALAGE) // SCALING)
        return est_un_mur(pos_grille)

    elif d == 3:  # Down
        pos_grille = ((rect.centerx) // SCALING, (rect.centery - DECALAGE) // SCALING + 1)
        return est_un_mur(pos_grille)
    elif d == 1:  # Up
        pos_grille = ((rect.centerx // SCALING), (rect.centery - DECALAGE - 4) // SCALING)
        return est_un_mur(pos_grille)

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


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.frame = 0
        pygame.sprite.Sprite.__init__(self)
        self.up_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManUp0.png')),
                          pygame.image.load(os.path.join('ressource', 'images', 'PacManUp1.png'))]
        self.down_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManDown0.png')),
                            pygame.image.load(os.path.join('ressource', 'images', 'PacManDown1.png'))]
        self.left_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft0.png')),
                            pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))]
        self.right_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManRight0.png')),
                             pygame.image.load(os.path.join('ressource', 'images', 'PacManRight1.png'))]
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = [PACSPAWN[0], PACSPAWN[1]]
        """Direction (en attendant l'enum) : 0 = Left   1 = Up    2 = Right   3 = Down"""
        self.direction = 0
        self.CNSTE_VITESSE = 8
        self.GoLeft = [-self.CNSTE_VITESSE, 0]
        self.GoUp = [0, -self.CNSTE_VITESSE]
        self.GoRight = [self.CNSTE_VITESSE, 0]
        self.GoDown = [0, self.CNSTE_VITESSE]
        self.vitesse = [0, 0]

    def update(self, direction):
        self.direction = direction
        if direction == 0:
            self.vitesse = self.GoLeft
            # self.image = self.left_images[0]
        elif direction == 1:
            self.vitesse = self.GoUp
            # self.image = self.up_images[0]
        elif direction == 2:
            self.vitesse = self.GoRight
            # self.image = self.right_images[0]
        elif direction == 3:
            self.vitesse = self.GoDown
            # elf.image = self.down_images[0]

        if collision_mur(self):
            self.vitesse = [0, 0]

        self.pos = (self.pos[0] + (self.vitesse[0]), self.pos[1] + (self.vitesse[1]))
        self.rect.center = self.pos

    def kill_animation(self):
        self.pac.vitesse = [0, 0]
        self.pac.image = pygame.image.load(os.path.join(os.path.join('ressource', 'images', 'PacDead0.png')))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead1.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead2.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead3.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead4.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead5.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead6.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead7.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead8.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead9.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead10.png'))
        pygame.time.wait(self.VITESSE_MORT)
        self.pac.image = pygame.image.load(os.path.join('ressource', 'images', 'PacDead11.png'))
        pygame.time.wait(self.VITESSE_MORT)

    def set_position(self, position):
        self.pos = position


class Fantome(pygame.sprite.Sprite):
    def __init__(self, pos, nom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(nom)))
        self.rect = self.image.get_rect(center=pos)
