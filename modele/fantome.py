import pygame
import os
from modele.direction import Direction
import modele.board as board
from math import hypot


class Fantome(pygame.sprite.Sprite):
    CSTNE_VITESSE = 6

    def __init__(self, pos, nom, target):
        self.target = target
        self.nbr_activation = -1
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.count_anim = 0
        self.frame = 0
        self.nom = nom
        pygame.sprite.Sprite.__init__(self)

        self.up_images = [pygame.image.load(os.path.join('ressource', 'images', '{0}Up0.png'.format(self.nom))),
                          pygame.image.load(os.path.join('ressource', 'images', '{0}Up1.png'.format(self.nom)))]

        self.down_images = [pygame.image.load(os.path.join('ressource', 'images', '{0}Down0.png'.format(self.nom))),
                            pygame.image.load(os.path.join('ressource', 'images', '{0}Down1.png'.format(self.nom)))]

        self.left_images = [pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(self.nom))),
                            pygame.image.load(os.path.join('ressource', 'images', '{0}Left1.png'.format(self.nom)))]

        self.right_images = [pygame.image.load(os.path.join('ressource', 'images', '{0}Right0.png'.format(self.nom))),
                             pygame.image.load(os.path.join('ressource', 'images', '{0}Right1.png'.format(self.nom)))]

        self.images_scared = {
            1: pygame.image.load(os.path.join('ressource', 'images', 'Scared00.png'.format(self.nom))),
            2: pygame.image.load(os.path.join('ressource', 'images', 'Scared01.png'.format(self.nom))),
            3: pygame.image.load(os.path.join('ressource', 'images', 'Scared10.png'.format(self.nom))),
            4: pygame.image.load(os.path.join('ressource', 'images', 'Scared11.png'.format(self.nom)))}
        self.image = self.left_images[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self, pac_rect, pastille_mangees, pac_direction):
        if self.nbr_activation < pastille_mangees:
            if board.detecte_noeud(self.rect):
                self.choose_direction()
            self.rect = self.rect.move(self.vitesse)
            board.tunnel(self.rect)
        else:
            pass
        self.normal_animation()

    def respawn(self):
        """
        Cette méthode doit être redéfinie par chaque enfant.
        :return: void
        """
        pass

    def select_target(self, new_target):
        """
        Cette méthode donne une nouvelle target au fantôme
        :param new_target: la nouvelle target du fantôme
        :return: void
        """
        self.target = new_target

    def move_to_target(self):
        pass

    def get_possible_direction(self):
        pass

    def choose_direction(self):
        distance = 100000000
        meilleur_choix = Direction.GAUCHE
        for d in Direction.__iter__():
            if d == Direction.AUCUNE:
                break
            if d != self.direction.opposee() and not board.collision_mur(self.rect, d):
                v = [x * Fantome.CSTNE_VITESSE for x in Direction.get_vecteur(d)]
                temp = self.distance(self.rect.move(v))
                if temp < distance:
                    distance = temp
                    meilleur_choix = d
                    self.vitesse = v
        self.direction = meilleur_choix

    def distance(self, rect):
        """
        Distance entre un Rect et le target.
        :param rect:
        :return: La distance
        """
        return hypot(rect.centerx - self.target[0], rect.centery - self.target[1])

    def normal_animation(self):
        if self.count_anim > 2:
            self.count_anim = 0
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

    # Cette phase est activé lorsque le Pac-Man mange un power pellet
    def phase_apeuree(self):
        # Doit faire changer la couleur des fantômes
        # Doit durer un temps prédéterminé (20 sec - moins 'niveau')
        # Doit changer la collision avec pacman, au lieu de tuer PacMan, le fantôme meurt
        pass

    def calculer_avance(self, pos_pacman, pac_direction):
        """
        Permet de savoir la position plus 4 cases du pacman, s'adapte aussi au tunnel pour donner l'autre bout
        :param pos_pacman: la position du pac man
        :param pac_direction: la direction du pac man
        :return: la position en avance du pac man
        """
        if pac_direction == Direction.GAUCHE:
            if pos_pacman.centerx - 4 * board.SCALING < 0 and pos_pacman.y == 400:
                return (672 - 4 * board.SCALING, pos_pacman.centery)  # environ 4 cases à la sorite du tunnel
            else:
                return (pos_pacman.centerx - 4 * board.SCALING, pos_pacman.centery)
        elif pac_direction == Direction.DROITE:
            if pos_pacman.centerx + 4 * board.SCALING > 672 and pos_pacman.y == 400:  # revoir pour les cases
                return (0 + 4 * board.SCALING, pos_pacman.centery)  # environ 4 cases à la sorite du tunnel
            else:
                return (pos_pacman.centerx + 4 * board.SCALING, pos_pacman.centery)
        elif pac_direction == Direction.HAUT:
            return (pos_pacman.centerx, pos_pacman.centery - 4 * board.SCALING)
        elif pac_direction == Direction.BAS:
            return (pos_pacman.centerx, pos_pacman.centery + 4 * board.SCALING)


class Blinky(Fantome):
    SCATTER_TARGET = (670, 1)
    SPAWN = (336, 349)

    def __init__(self):
        Fantome.__init__(self, Blinky.SPAWN, "Blinky", Blinky.SCATTER_TARGET)
        self.actif = True
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def respawn(self):
        self.rect.center = Blinky.SPAWN
        self.direction = Direction.GAUCHE
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def phase_chasse(self, pos_pacman):
        self.target = (pos_pacman)


class Pinky(Fantome):
    SCATTER_TARGET = (1, 1)
    SPAWN = (336, 421)

    def __init__(self):
        Fantome.__init__(self, Pinky.SPAWN, "Pinky", Pinky.SCATTER_TARGET)
        self.direction = Direction.GAUCHE
        self.actif = True
        self.nbr_activation = 5
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def respawn(self):
        self.rect.center = Pinky.SPAWN
        self.direction = Direction.BAS
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def phase_chasse(self, pos_avance):
        self.target = pos_avance


class Inky(Fantome):
    SCATTER_TARGET = (670, 860)
    SPAWN = (288, 421)

    def __init__(self):
        Fantome.__init__(self, Inky.SPAWN, "Inky", Inky.SCATTER_TARGET)
        self.direction = Direction.BAS
        self.nbr_activation = 30
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def respawn(self):
        self.rect.center = Inky.SPAWN
        self.direction = Direction.BAS
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def phase_chasse(self, pos_blinky, pos_avance):
        difx = pos_avance[0] - pos_blinky[0]
        dify = pos_avance[1] - pos_blinky[1]
        self.target = (pos_avance[0] + difx, pos_avance[1] + dify)


class Clyde(Fantome):
    SCATTER_TARGET = (1, 860)
    SPAWN = (384, 421)

    def __init__(self):
        Fantome.__init__(self, Clyde.SPAWN, "Clyde", Clyde.SCATTER_TARGET)
        self.direction = Direction.BAS
        self.nbr_activation = 60
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def respawn(self):
        self.rect.center = Clyde.SPAWN
        self.direction = Direction.BAS
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]

    def phase_chasse(self, pos_pacman):
        # la différence de 8 cases c tu en diagonale?
        pass
