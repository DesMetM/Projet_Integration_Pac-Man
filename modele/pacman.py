import os
import pygame
from modele.direction import Direction
import modele.board as board

"""Classe représentant le Pac-Man. Est un enfant de Sprite et redéfinie la méthode Update"""
class PacMan(pygame.sprite.Sprite):
    """Constructeur. Load les images d'animation, set l'image de base, crée le rect et instantie les frames pour l'animation."""
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
        self.direction = Direction.GAUCHE
        self.CNSTE_VITESSE = 6
        self.GoLeft = [-self.CNSTE_VITESSE, 0]
        self.GoUp = [0, -self.CNSTE_VITESSE]
        self.GoRight = [self.CNSTE_VITESSE, 0]
        self.GoDown = [0, self.CNSTE_VITESSE]
        self.vitesse = [0, 0]
        self.count_anim = 0
        self.is_alive = True

    """Méthode appelée à chaque update de position du Pac-Man. Dépendement de la direction donnée en paramètre (Enum), set la vitesse actuelle. 
La vitesse acctuelle est un vecteur représentant la vitesse x et y. Tentative de portail Haha"""
    def update(self, direction):
        """Vérifies la présence d'un mur"""
        if direction != Direction.AUCUNE and not board.collision_mur(self.rect, direction) and not board.collision_portail(self.rect, direction):
            self.direction = direction
            """Change la vitesse selon la direction (ecteur)"""
            if direction == Direction.GAUCHE:
                self.vitesse = self.GoLeft
            elif direction == Direction.HAUT:
                self.vitesse = self.GoUp
            elif direction == Direction.DROITE:
                self.vitesse = self.GoRight
            elif direction == Direction.BAS:
                self.vitesse = self.GoDown
            """Si un mur est présent, stop Pac-Man"""
        elif board.collision_mur(self.rect, self.direction):
            self.vitesse = [0, 0]
            """Si un portail est trouvé, teleporte de l'autre côté (Gros BS fait par nul autre que NikkyBee)"""
        elif board.collision_portail(self.rect, self.direction):
            if direction == Direction.GAUCHE:
                self.rect.move_ip((200, 0))
            elif direction == Direction.DROITE:
                self.rect.move_ip((-200, 0))
        """Change la position de Pac-Man"""
        self.rect = self.rect.move(self.vitesse)

    """ Méthode qui anime la mort de Pac-Man. 12 images."""
    def kill_animation(self):
        if self.count_anim <= 11:
            self.image = pygame.image.load(
                os.path.join(os.path.join('ressource', 'images', 'PacDead' + str(self.count_anim) + '.png')))
            self.count_anim = self.count_anim + 1
        return self.count_anim == 12

    """Méthode qui anime le mouvement de Pac-Man"""
    def move_animation(self):
        if self.count_anim > 2:
            self.count_anim = 0
            """Dépendemment de la direction, l'animation est différente ( Pac-Man fait face à sa direction)"""
            if self.vitesse != [0, 0]:
                self.frame = not self.frame
                if self.direction == Direction.GAUCHE:
                    self.image = self.left_images[self.frame]
                elif self.direction == Direction.HAUT:
                    self.image = self.up_images[self.frame]
                elif self.direction == Direction.DROITE:
                    self.image = self.right_images[self.frame]
                elif self.direction == Direction.BAS:
                    self.image = self.down_images[self.frame]
        else:
            self.count_anim += 1
