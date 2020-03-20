import os
import pygame
from modele.direction import Direction
import modele.board as board

"""Classe représentant le Pac-Man. Est un enfant de Sprite et redéfinie la méthode Update"""


class PacMan(pygame.sprite.Sprite):
    CNSTE_VITESSE = 6
    SPAWN = (336, 637)
    IMAGES = {Direction.GAUCHE: [pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft0.png')),
                                 pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))],
              Direction.HAUT: [pygame.image.load(os.path.join('ressource', 'images', 'PacManUp0.png')),
                               pygame.image.load(os.path.join('ressource', 'images', 'PacManUp1.png'))],
              Direction.DROITE: [pygame.image.load(os.path.join('ressource', 'images', 'PacManRight0.png')),
                                 pygame.image.load(os.path.join('ressource', 'images', 'PacManRight1.png'))],
              Direction.BAS: [pygame.image.load(os.path.join('ressource', 'images', 'PacManDown0.png')),
                              pygame.image.load(os.path.join('ressource', 'images', 'PacManDown1.png'))]}
    MORT = []
    for i in range(12):
        MORT.append(pygame.image.load(os.path.join('ressource', 'images', 'PacDead' + str(i) + '.png')))

    """Constructeur. Load les images d'animation, set l'image de base, crée le rect et instantie les frames pour l'animation."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PacMan.IMAGES[Direction.GAUCHE][1]
        self.rect = self.image.get_rect(center=PacMan.SPAWN)
        self.radius = 21
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.nbr_vie = 4
        self.is_alive = True
        self.action = 1

    """Méthode appelée à chaque update de position du Pac-Man. Dépendement de la direction donnée en paramètre (Enum), set la vitesse actuelle. 
La vitesse acctuelle est un vecteur représentant la vitesse x et y. Tentative de portail Haha"""

    def update(self, direction):
        """Vérifies la présence d'un mur"""
        if direction != Direction.AUCUNE and not board.collision_mur(self.rect, direction):
            self.direction = direction
            self.vitesse = [PacMan.CNSTE_VITESSE * i for i in direction.get_vecteur()]

        elif board.collision_mur(self.rect, self.direction):
            self.vitesse = [0, 0]

        board.tunnel(self.rect)
        self.rect = self.rect.move(self.vitesse)

    def animation(self, compteur):
        if self.is_alive:
            if self.vitesse != [0, 0]:
                self.action = not self.action
                self.image = PacMan.IMAGES[self.direction][self.action]
        elif compteur <= 33:
            self.image = PacMan.MORT[compteur // 3]

    def respawn(self):
        self.nbr_vie -= 1
        self.vitesse = [0, 0]
        self.rect.center = PacMan.SPAWN
        self.image = PacMan.IMAGES[Direction.GAUCHE][1]
        self.is_alive = True
