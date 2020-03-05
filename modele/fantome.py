import pygame
import os
from modele.direction import Direction
import modele.board as board
from math import hypot
from modele.modes_fantome import Mode
from random import randint


class Fantome(pygame.sprite.Sprite):
    CSTNE_VITESSE = 6

    def __init__(self, pos, nom, scatter):
        self.target = None
        self.mode = Mode.INACTIF
        self.nbr_activation = -1
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.count_anim = 0
        self.count_effraye = 0
        self.frame = 0
        self.nom = nom
        self.radius = 21
        self.scatter = scatter
        self.acheve = False
        self.compteur_peur = 0
        self.compteur_ini = 0
        self.niveau = 0
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

    def update(self, jeu):
        self.mode(self, jeu)

        self.animation()

    def sortir(self):
        if self.rect.centerx != 336:
            self.target = (336, 421)
        else:
            self.target = Blinky.SPAWN

        if self.rect.center != Blinky.SPAWN:
            self.choose_direction(False)
            self.rect = self.rect.move(self.vitesse)
        else:
            self.set_mode(Mode.DISPERSION)
            self.avancer()

    def set_mode(self, mode):
        if mode == Mode.DISPERSION:
            self.target = self.scatter
        elif mode == Mode.RETOUR:
            self.target = Blinky.SPAWN
        self.mode = mode

    def retour_au_bercail(self):
        """
        Le fantôme retourne dans la cage. self.image est affectée comme étant des yeux seulement.
        :return: void
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

    def respawn(self):
        """
        Cette méthode doit être redéfinie par chaque enfant. Elle affecte la vitesse, la direction et la position du spawn du fantôme.
        :return: void
        """
        pass

    def avancer(self):
        """
        Déplace le fantôme vers son target.
        :return: void
        """
        if board.detecte_noeud(self.rect):
            self.choose_direction(True)
        self.rect = self.rect.move(self.vitesse)
        board.tunnel(self.rect)

    def mode_chasse(self, jeu):
        """
        Cette méthode doit être redéfinie par chaque enfant. Elle redéfinie le target du fantôme selon son comportement.
        :return:
        """
        pass

    def choose_direction(self, mur):
        """
        Choisi la meilleure direction à prendre vers le target. Prend en compte les murs.
        :return: void
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
        :param rect:
        :return: La distance
        """
        return hypot(rect.centerx - self.target[0], rect.centery - self.target[1])

    def animation(self):
        if self.mode != Mode.EFFRAYE:
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
        else:
            if self.count_anim > 2 and not self.acheve:
                self.count_anim = 0
                if not (self.frame == 0 or self.frame == 1):
                    self.frame = 0
                self.frame = not self.frame
                self.image = self.images_scared[self.frame + 1]
            elif self.count_anim > 2:
                self.count_anim = 0
                self.frame = (self.frame + 1) % 4
                self.image = self.images_scared[self.frame + 1]
            else:
                self.count_anim += 1

    # Cette phase est activé lorsque le Pac-Man mange un power pellet
    def mode_effraye(self):
        # DO SOMETHING
        if self.compteur_peur == 0:
            self.compteur_ini = pygame.time.get_ticks()
            self.compteur_peur = self.compteur_ini
            self.direction = self.direction.opposee()
        if self.compteur_peur > self.compteur_ini + (
                (20000 - self.niveau * 500) / 2) and self.compteur_peur < self.compteur_ini + (
                20000 - self.niveau * 500):
            self.acheve = True
            self.compteur_peur = pygame.time.get_ticks()
        elif pygame.time.get_ticks() >= self.compteur_ini + (20000 - self.niveau * 500):
            self.set_mode(Mode.DISPERSION)
            self.compteur_peur = 0
            self.acheve = False
        else:
            self.compteur_peur = pygame.time.get_ticks()

        if board.detecte_noeud(self.rect):
            groupe = []
            groupe2 = {}
            for d in Direction.__iter__():
                if d != self.direction.opposee() and d != self.direction.AUCUNE and not board.collision_mur(self.rect,
                                                                                                            d):
                    groupe.append(d)
            for d in groupe:
                groupe2[d] = [x * (Fantome.CSTNE_VITESSE * 3 / 5) for x in Direction.get_vecteur(d)]
            self.direction = groupe[randint(0, len(groupe) - 1)]
            self.vitesse = groupe2[self.direction]

        self.rect = self.rect.move(self.vitesse)
        board.tunnel(self.rect)

        # Doit faire changer la couleur des fantômes
        # Doit durer un temps prédéterminé (20 sec - moins 'niveau')
        # Doit changer la collision avec pacman, au lieu de tuer PacMan, le fantôme meurt
        pass

    def calculer_avance(self, pos_pacman, pac_direction, n_cases):
        """
        Permet de savoir la position plus n cases du pacman, s'adapte aussi au tunnel pour donner l'autre bout
        :param pos_pacman: la position du pac man
        :param pac_direction: la direction du pac man
        :return: la position en avance du pac man
        """
        if pac_direction == Direction.GAUCHE:
            if pos_pacman.centerx - n_cases * board.SCALING < 0 and pos_pacman.y == 400:
                return (672 - n_cases * board.SCALING, pos_pacman.centery)  # environ 4 cases à la sorite du tunnel
            else:
                return (pos_pacman.centerx - n_cases * board.SCALING, pos_pacman.centery)
        elif pac_direction == Direction.DROITE:
            if pos_pacman.centerx + n_cases * board.SCALING > 672 and pos_pacman.y == 400:  # revoir pour les cases
                return (0 + n_cases * board.SCALING, pos_pacman.centery)  # environ 4 cases à la sorite du tunnel
            else:
                return (pos_pacman.centerx + n_cases * board.SCALING, pos_pacman.centery)
        elif pac_direction == Direction.HAUT:
            return (pos_pacman.centerx - n_cases * board.SCALING, pos_pacman.centery - n_cases * board.SCALING)
        elif pac_direction == Direction.BAS:
            return (pos_pacman.centerx, pos_pacman.centery + n_cases * board.SCALING)


class Blinky(Fantome):
    SCATTER_TARGET = (670, 1)
    SPAWN = (336, 349)

    def __init__(self):
        Fantome.__init__(self, Blinky.SPAWN, "Blinky", Blinky.SCATTER_TARGET)
        self.actif = True
        self.vitesse = [x * Fantome.CSTNE_VITESSE for x in self.direction.get_vecteur()]
        self.target = self.scatter
        self.mode = Mode.DISPERSION

    def respawn(self):
        self.rect.center = Blinky.SPAWN
        self.mode = Mode.DISPERSION

    def mode_chasse(self, jeu):
        self.target = jeu.pacman.sprite.rect.center
        self.avancer()


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
        self.mode = Mode.INACTIF

    def mode_chasse(self, jeu):
        pacman = jeu.pacman.sprite
        self.target = self.calculer_avance(pacman.rect, pacman.direction, 4)
        self.avancer()


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
        self.mode = Mode.INACTIF

    def mode_chasse(self, jeu):
        pacman = jeu.pacman.sprite
        blinky = jeu.blinky
        pos_avance = self.calculer_avance(pacman.rect, pacman.direction, 2)
        difx = pos_avance[0] - blinky.rect.centerx
        dify = pos_avance[1] - blinky.rect.centery
        self.target = (pos_avance[0] + difx, pos_avance[1] + dify)
        self.avancer()


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
        self.mode = Mode.INACTIF

    def mode_chasse(self, pacman=None, blinky=None):
        self.target = pacman.rect.center
        if self.distance(self.rect) < 192:
            self.target = Clyde.SCATTER_TARGET
        self.avancer()
