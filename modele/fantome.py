import pygame
import os
from modele.direction import Direction
import modele.board as board
from math import hypot
from modele.modes_fantome import Mode
import random


class Fantome(pygame.sprite.Sprite):
    """
    Classe abstraite d'un fantôme.
    """
    CSTNE_VITESSE = 6
    IMAGES_EFFRAYE = [
        pygame.image.load(os.path.join('ressource', 'images', 'Scared00.png')),
        pygame.image.load(os.path.join('ressource', 'images', 'Scared01.png')),
        pygame.image.load(os.path.join('ressource', 'images', 'Scared10.png')),
        pygame.image.load(os.path.join('ressource', 'images', 'Scared11.png'))]

    IMAGES_RETOUR = {Direction.HAUT: pygame.image.load(os.path.join('ressource', 'images', 'EatenUp.png')),
                     Direction.DROITE: pygame.image.load(os.path.join('ressource', 'images', 'EatenRight.png')),
                     Direction.BAS: pygame.image.load(os.path.join('ressource', 'images', 'EatenDown.png')),
                     Direction.GAUCHE: pygame.image.load(os.path.join('ressource', 'images', 'EatenLeft.png'))}

    def __init__(self, pos, nom, scatter):
        """
        Constructeur d'un fantôme.
        :param pos: Position où faire apparaître le fantôme.
        :param nom: Le nom du fantôme.
        :param scatter: La cible du fantôme en mode dispersion.
        """
        self.target = None
        self.mode = Mode.INACTIF
        self.peur = False
        self.nbr_activation = -1
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.radius = 16
        self.scatter = scatter
        pygame.sprite.Sprite.__init__(self)

        self.images = {
            Direction.HAUT: [pygame.image.load(os.path.join('ressource', 'images', '{0}Up0.png'.format(nom))),
                             pygame.image.load(os.path.join('ressource', 'images', '{0}Up1.png'.format(nom)))],
            Direction.DROITE: [pygame.image.load(os.path.join('ressource', 'images', '{0}Right0.png'.format(nom))),
                               pygame.image.load(os.path.join('ressource', 'images', '{0}Right1.png'.format(nom)))],
            Direction.BAS: [pygame.image.load(os.path.join('ressource', 'images', '{0}Down0.png'.format(nom))),
                            pygame.image.load(os.path.join('ressource', 'images', '{0}Down1.png'.format(nom)))],
            Direction.GAUCHE: [pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(nom))),
                               pygame.image.load(os.path.join('ressource', 'images', '{0}Left1.png'.format(nom)))]}

        self.image = self.images[Direction.GAUCHE][1]
        self.rect = self.image.get_rect(center=pos)

    def update(self, jeu):
        """
        Met à jour l'état du fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        self.mode(self, jeu)

    def sortir(self, jeu):
        """
        Fais sortir le fantôme de la cage.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        if self.rect.centerx != 336:
            self.target = (336, 421)
        else:
            self.target = Blinky.SPAWN

        if self.rect.center != Blinky.SPAWN:
            self.choose_direction(False)
            self.vitesse = [x * 3 / 5 for x in self.vitesse]
            self.rect = self.rect.move(self.vitesse)
        else:
            if self.peur:
                self.set_mode(Mode.EFFRAYE)
            else:
                self.set_mode(jeu.timer_jeu.current_mode)

    def set_mode(self, mode):
        """
        S'occupe de faire les actions nécessaire lors d'un changement de mode.
        :param mode: Le mode auquel on veut changer.
        :return: None
        """
        if mode == Mode.DISPERSION:
            self.target = self.scatter
        elif mode == Mode.RETOUR:
            self.peur = False
            self.target = Blinky.SPAWN
        elif mode == Mode.EFFRAYE:
            self.direction = self.direction.opposee()
            self.vitesse = [x * Fantome.CSTNE_VITESSE * 3 / 5 for x in self.direction.get_vecteur()]
        self.mode = mode

    def retour_au_bercail(self):
        """
        Le fantôme retourne dans la cage. «self.image» est affectée comme étant des yeux seulement.
        :return: None
        """
        if self.rect.center == Blinky.SPAWN:
            self.target = Pinky.SPAWN
        elif self.rect.center == Pinky.SPAWN:
            self.direction = self.direction.opposee()
            self.set_mode(Mode.SORTIR)

        if self.target == Blinky.SPAWN:
            if board.detecte_noeud(self.rect):
                self.choose_direction(True)
        else:
            self.choose_direction(False)

        self.rect = self.rect.move(self.vitesse)
        board.tunnel(self.rect)

    def respawn(self, jeu):
        """
        Cette méthode doit être redéfinie par chaque enfant. Elle affecte le mode et la position du Fantôme.
        :return: None
        """
        self.set_mode(Mode.INACTIF)
        self.peur = False
        self.image = self.images[Direction.GAUCHE][1]

    def avancer(self):
        """
        Déplace le fantôme vers son target.
        :return: None
        """
        if board.detecte_noeud(self.rect):
            self.choose_direction(True)
        self.rect = self.rect.move(self.vitesse)
        board.tunnel(self.rect)

    def mode_chasse(self, jeu):
        """
        Cette méthode doit être redéfinie par chaque enfant. Elle affecte le target du fantôme selon son comportement.
        :return:
        """
        pass

    def choose_direction(self, mur):
        """
        Choisi la meilleure direction à prendre vers le target. Prend en compte les murs.
        :param mur: «True» pour prendre en compte les murs, «False» pour ne pas prendre en compte les murs.
        :return: None
        """
        distance = 100000000
        meilleur_choix = Direction.GAUCHE
        for d in Direction.__iter__():
            if d == Direction.AUCUNE:
                break
            if d != self.direction.opposee() and (not mur or not board.collision_mur(self.rect, d)):
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
        :param rect: Rectangle que l'on veut comparer.
        :return: La distance entre un rect et son target.
        """
        return hypot(rect.centerx - self.target[0], rect.centery - self.target[1])

    def animation(self, action_fantome):
        """
        Cette méthode change l'image du fantôme selon son mode actuel.
        :param action_fantome: Le moment du jeu.
        :return: None
        """
        if self.peur:
            self.image = Fantome.IMAGES_EFFRAYE[action_fantome]
        elif self.mode == Mode.RETOUR:
            self.image = Fantome.IMAGES_RETOUR[self.direction]
        else:
            self.image = self.images[self.direction][action_fantome % 2]

    # Cette phase est activé lorsque le Pac-Man mange un power pellet
    def mode_effraye(self):
        """
        Un fantôme en mode effrayé se déplace aléatoirement et plus lentement.
        :return: None
        """
        if board.detecte_noeud(self.rect):
            groupe = {}
            for d in Direction.__iter__():
                if d != self.direction.opposee() and d != self.direction.AUCUNE \
                        and not board.collision_mur(self.rect, d):
                    v = [x * (Fantome.CSTNE_VITESSE * 3 / 5) for x in Direction.get_vecteur(d)]
                    groupe[d] = v

            self.direction = random.choice(list(groupe.keys()))
            self.vitesse = groupe[self.direction]

        self.rect = self.rect.move(self.vitesse)
        board.tunnel(self.rect)

    @staticmethod
    def calculer_avance(pos_pacman, pac_direction, n_cases):
        """
        Permet de savoir la position plus n cases du pacman, s'adapte aussi au tunnel pour donner l'autre bout.
        :param n_cases: Le nombre de case à calculer devant Pac-Man.
        :param pos_pacman: la position du Pac-Man.
        :param pac_direction: la direction du Pac-Man.
        :return: la position en avance Pac-Man.
        """
        if pac_direction == Direction.GAUCHE:
            if pos_pacman.centerx - n_cases * board.SCALING < 0 and pos_pacman.y == 400:
                return 672 - n_cases * board.SCALING, pos_pacman.centery  # environ 4 cases à la sorite du tunnel
            else:
                return pos_pacman.centerx - n_cases * board.SCALING, pos_pacman.centery
        elif pac_direction == Direction.DROITE:
            if pos_pacman.centerx + n_cases * board.SCALING > 672 and pos_pacman.y == 400:  # revoir pour les cases
                return n_cases * board.SCALING, pos_pacman.centery  # environ 4 cases à la sorite du tunnel
            else:
                return pos_pacman.centerx + n_cases * board.SCALING, pos_pacman.centery
        elif pac_direction == Direction.HAUT:
            return pos_pacman.centerx - n_cases * board.SCALING, pos_pacman.centery - n_cases * board.SCALING
        elif pac_direction == Direction.BAS:
            return pos_pacman.centerx, pos_pacman.centery + n_cases * board.SCALING


class Blinky(Fantome):
    """
    Le fantôme rouge.
    """
    SCATTER_TARGET = (670, 1)
    SPAWN = (336, 349)

    def __init__(self):
        """
        Constructeur de Blinky.
        """
        Fantome.__init__(self, Blinky.SPAWN, "Blinky", Blinky.SCATTER_TARGET)
        self.set_mode(Mode.DISPERSION)

    def respawn(self, jeu):
        """
        Pose le mode et la position initial du Fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        super().respawn(jeu)
        self.rect.center = Blinky.SPAWN
        self.mode = jeu.timer_jeu.current_mode

    def mode_chasse(self, jeu):
        """
        Choisit le chemin le plus court vers Pac-Man.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        self.target = jeu.pacman.sprite.rect.center
        self.avancer()


class Pinky(Fantome):
    """
    Le fantôme rose.
    """
    SCATTER_TARGET = (1, 1)
    SPAWN = (336, 421)

    def __init__(self):
        """
        Constructeur de Pinky.
        """
        Fantome.__init__(self, Pinky.SPAWN, "Pinky", Pinky.SCATTER_TARGET)
        self.nbr_activation = 5

    def respawn(self, jeu):
        """
        Pose le mode et la position initial du Fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        super().respawn(jeu)
        self.rect.center = Pinky.SPAWN

    def mode_chasse(self, jeu):
        """
        Se déplace quatre cases devant Pac-Man.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        pacman = jeu.pacman.sprite
        self.target = Fantome.calculer_avance(pacman.rect, pacman.direction, 4)
        self.avancer()


class Inky(Fantome):
    """
    Le fantôme bleu.
    """
    SCATTER_TARGET = (670, 860)
    SPAWN = (288, 421)

    def __init__(self):
        """
        Le constructeur de Inky.
        """
        Fantome.__init__(self, Inky.SPAWN, "Inky", Inky.SCATTER_TARGET)
        self.nbr_activation = 30

    def respawn(self, jeu):
        """
        Pose le mode et la position initial du Fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        super().respawn(jeu)
        self.rect.center = Inky.SPAWN

    def mode_chasse(self, jeu):
        """
        Si on trace un vecteur qui débute deux cases devant Pac-Man et qui termine sur blinky,
        alors Inky se déplace dans la direction opposée à ce vecteur. Cela a pour conséquence de bloquer en sandwich
        Pac-Man.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        pacman = jeu.pacman.sprite
        blinky = jeu.blinky
        pos_avance = Fantome.calculer_avance(pacman.rect, pacman.direction, 2)
        difx = pos_avance[0] - blinky.rect.centerx
        dify = pos_avance[1] - blinky.rect.centery
        self.target = (pos_avance[0] + difx, pos_avance[1] + dify)
        self.avancer()


class Clyde(Fantome):
    """
    Le fantôme orange.
    """
    SCATTER_TARGET = (1, 860)
    SPAWN = (384, 421)

    def __init__(self):
        """
        Le constructeur de Clyde.
        """
        Fantome.__init__(self, Clyde.SPAWN, "Clyde", Clyde.SCATTER_TARGET)
        self.nbr_activation = 60

    def respawn(self, jeu):
        """
        Pose le mode et la position initial du Fantôme.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        super().respawn(jeu)
        self.rect.center = Clyde.SPAWN

    def mode_chasse(self, jeu):
        """
        Choisit le chemin le plus court vers Pac-Man et quand il est à une distance inférieur à 8 cases,
        il fuit vers sa cible de dispersion.
        :param jeu: Le jeu auquel le fantôme appartient.
        :return: None
        """
        self.target = jeu.pacman.sprite.rect.center
        if self.distance(self.rect) < 192:
            self.target = Clyde.SCATTER_TARGET
        self.avancer()
