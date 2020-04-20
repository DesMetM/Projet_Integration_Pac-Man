import os
import pygame
from modele.direction import Direction
import modele.board as board


class PacMan(pygame.sprite.Sprite):
    """
    Classe représentant le Pac-Man. Est un enfant de Sprite et redéfinie la méthode update(self).
    """
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

    def __init__(self):
        """
        Constructeur de Pac-Man. Pac-Man regarde à gauche et commence à sa position initiale dans la grille.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = PacMan.IMAGES[Direction.GAUCHE][1]
        self.rect = self.image.get_rect(center=PacMan.SPAWN)
        self.radius = 21
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.nbr_vie = 4
        self.is_alive = True
        self.action = 1

    @staticmethod
    def get_pacman():
        """
        Retourne un SingleGroup contenant le Pac-Man.
        :return: Un SingleGroup contenant le Pac-Man.
        """
        groupe = pygame.sprite.GroupSingle()
        groupe.add(PacMan())
        return groupe

    def update(self, direction):
        """
        Méthode appelée à chaque update de position du Pac-Man. Dépendement de la direction donnée en paramètre,
         set la vitesse actuelle s'il y a un mur ou non.
        :param direction: Action du joueur.
        :return: None
        """
        if direction != Direction.AUCUNE and not board.collision_mur(self.rect, direction):
            self.direction = direction
            self.vitesse = [PacMan.CNSTE_VITESSE * i for i in direction.get_vecteur()]

        elif board.collision_mur(self.rect, self.direction):
            self.vitesse = [0, 0]

        board.tunnel(self.rect)
        self.rect = self.rect.move(self.vitesse)

    def animation(self, compteur, partie_gagnee):
        """
        Affecte l'image de Pac-Man selon le temps, sa direction et s'il est en vie.
        :param compteur: Le temps du timer.
        :return: None
        """
        if partie_gagnee:
            self.image = PacMan.MORT[0]
        elif self.is_alive:
            if self.vitesse != [0, 0]:
                self.action = not self.action
                self.image = PacMan.IMAGES[self.direction][self.action]
        elif compteur <= 33:
            self.image = PacMan.MORT[compteur // 3]

    def respawn(self):
        """
        Pac-Man pert une vie et réaparaît à sa position initiale.
        :return: None
        """
        self.nbr_vie -= 1
        self.vitesse = [0, 0]
        self.rect.center = PacMan.SPAWN
        self.image = PacMan.IMAGES[Direction.GAUCHE][1]
        self.is_alive = True
