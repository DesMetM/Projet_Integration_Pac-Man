import pygame
import os
import modele.board as board
from math import ceil
from modele.modes_fantome import Mode
from modele.timer import TimerJeu, TimerFruit, TimerAnimation
from modele.pacman import PacMan
from modele.direction import Direction
from modele.board import Pastille, GrossePastille, Fruit, GRILLE_DE_JEU, SCALING, DECALAGE, DECALAGEX, copy_grille


class Jeu:
    """
    Cette classe gère le jeu Pac-Man.
    """
    BACKGROUND = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
    BACKGROUND_BLANC = pygame.image.load(os.path.join('ressource', 'images', 'Board_Blanc.png'))
    FRUIT = Fruit.get_liste_fruits()
    FONT = None
    FONT2 = None


    def __init__(self):
        """
        Le constructeur déclare seulement les attributs. Il faut appeller la méthode nouvelle_partie(self) par la suite.
        """

        self.pastilles = Pastille.pastilles()
        self.power_pellets = GrossePastille.grosses_pastilles()
        self.pacman = PacMan.get_pacman()
        self.fantomes = None
        self.blinky = None
        self.pastilles_mangees = 0
        self.timer_jeu = None
        self.channel_actif = [False] * 9
        self.fantome_mange = False
        self.position_fantome_mange = None
        self.frame_fantome_mange = 0
        self.nbr_fantomes_manges = 0
        self.score = 0
        self.derniere_pastille = None
        self.count_board_anim = 0


        self.fruits_mangees = 0
        self.fruit_est_mange = False
        self.frame_fruit_mange = 0
        self.maGrille = GRILLE_DE_JEU.copy()

        '''peut être enlevé pour version finale'''
        self.game_rapide = False

        if Jeu.FONT is None:
            Jeu.FONT = pygame.font.Font(os.path.abspath("ressource/font/emulogic.ttf"), 20)
        if Jeu.FONT2 is None:
            Jeu.FONT2 = pygame.font.Font(os.path.abspath("ressource/font/emulogic.ttf"), 12)

    def printGrille(self):
        for ligne in self.maGrille:
            print(ligne, '\n')

    def nouvelle_partie(self, frame_rate):
        '''
        Débute une nouvelle partie.
        :param frame_rate: La vitesse que doit compter le timer. Le frame rate doit correspondre à celui de la vue.
        :return: None
        '''
        self.score = 0
        self.maGrille = copy_grille()
        self.pastilles = Pastille.pastilles()
        self.power_pellets = GrossePastille.grosses_pastilles()
        self.pacman.sprite.respawn()
        self.pacman.sprite.nbr_vie = 4
        self.fantomes, self.blinky = board.fantomes_init_pos()
        self.timer_jeu = TimerJeu(self, frame_rate)
        self.pastilles_mangees = 0
        self.timer_jeu.timer_sortie.debut_compteur()

    def collision(self):
        """
        Cette méthode s'occupe des collisions entre les pastilles, Pac-Man et les fantômes.
        :return: None
        """
        dict = pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False,
                                          dokillb=True)
        if dict:  # collision avec une pastille
            if len(self.pastilles) + len(self.power_pellets) == 0:
                self.timer_jeu.timer_animation.compteur = TimerAnimation.CYCLE // 2
            self.pastilles_mangees += 1
            self.ajouter_points_pellet()
            self.derniere_pastille = list(dict.values())[0][0]
            x, y = ceil((self.derniere_pastille.rect.x - DECALAGEX) / SCALING), ceil(
                (self.derniere_pastille.rect.y-DECALAGE) / SCALING)
            self.maGrille[y][x] = 6

        dict = pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False,
                                          dokillb=True)

        if dict:  # collision avec une power pellet
            if len(self.pastilles) + len(self.power_pellets) == 0:
                self.timer_jeu.timer_animation.compteur = TimerAnimation.CYCLE // 2
            self.timer_jeu.mode_effraye()
            self.ajouter_points_powerpellet()
            self.nbr_fantomes_manges = 0
            self.derniere_pastille = list(dict.values())[0][0]
            x, y = ceil((self.derniere_pastille.rect.x - DECALAGEX) / SCALING), ceil(
                (self.derniere_pastille.rect.y - DECALAGE) / SCALING)
            self.maGrille[y][x] = 6

            for x in self.fantomes:
                x.peur = True
                if x.mode == Mode.CHASSE or x.mode == Mode.DISPERSION:
                    x.set_mode(Mode.EFFRAYE)

        fantome_list = pygame.sprite.spritecollide(self.pacman.sprite, self.fantomes, False,
                                                   pygame.sprite.collide_circle)

        if fantome_list:  # collision avec un fantome
            for ghost in fantome_list:
                if (ghost.mode is not Mode.EFFRAYE) and (ghost.mode is not Mode.RETOUR):
                    self.channel_actif[8] = True
                    self.pacman.sprite.is_alive = False
                    self.timer_jeu.pacman_mort()
                elif ghost.peur:
                    self.fantome_mange = True
                    self.position_fantome_mange = (ghost.rect.left - 10, ghost.rect.top - 10)
                    self.frame_fantome_mange = self.timer_jeu.timer_animation.compteur if self.timer_jeu.timer_animation.compteur < self.timer_jeu.timer_animation.CYCLE - 20 else self.timer_jeu.timer_animation.CYCLE - 1 - 20
                    self.channel_actif[3] = True
                    self.nbr_fantomes_manges += 1
                    self.ajouter_points_fantome()
                    ghost.set_mode(Mode.RETOUR)

        if not self.timer_jeu.timer_fruit.ended and self.timer_jeu.timer_fruit.fruit != TimerFruit.TEMPS_DELAI and pygame.sprite.spritecollide(
                Jeu.FRUIT[self.fruits_mangees if self.fruits_mangees < 13 else 12], self.pacman,
                False):
            self.timer_jeu.timer_fruit.ended = True
            self.score += Jeu.FRUIT[self.fruits_mangees if self.fruits_mangees < 13 else 12].score
            self.fruits_mangees += 1
            self.channel_actif[6] = True
            self.fruit_est_mange = True
            self.frame_fruit_mange = self.timer_jeu.timer_animation.compteur if self.timer_jeu.timer_animation.compteur < self.timer_jeu.timer_animation.CYCLE - 20 else self.timer_jeu.timer_animation.CYCLE - 1 - 20

    def nouveau_fruit(self, fruit):
        self.timer_jeu.nouveau_fruit(fruit)

    def update_jeu(self, direction):
        """
        Passe au prochain état du jeu selon l'action du joueur.
        :param direction: L'action du joueur.
        :return: «True» si la partie est relancée.
        """
        self.channel_actif = [False] * 9
        self.channel_actif[0] = self.score >= 10000

        self.timer_jeu.update()

        if self.pacman.sprite.is_alive:
            if self.pastilles_mangees == 70 or self.pastilles_mangees == 100:
                self.nouveau_fruit(self.pastilles_mangees)

            elif len(self.pastilles) + len(self.power_pellets) == 0:
                if self.timer_jeu.timer_animation.compteur == 0:
                    self.nouvelle_partie(self.timer_jeu.frame_rate)
                    return True
                return False

            self.collision()
            self.pacman.update(direction)
            self.fantomes.update(self)

            if not self.channel_actif[0] and self.score >= 10000:
                self.pacman.sprite.nbr_vie += 1
                self.channel_actif[0] = True

        elif self.timer_jeu.timer_animation.compteur == 0:
            self.pacman.sprite.respawn()
            self.timer_jeu.timer_sortie.debut_compteur()
            for fantome in self.fantomes:
                fantome.respawn(self)
            return True

        return False

    def surface_partie_gagnee(self, background):
        """
        Fais clignoter la grille de jeu selon le timer.
        :param background: La surface à retourner.
        :return: Une surface de la grille de jeu qui contient Pac-Man et qui est soit blanche, soit bleu.
        """
        if self.timer_jeu.timer_animation.compteur % 8 <= 3:
            background.blit(Jeu.BACKGROUND_BLANC, (0, 0))
        else:
            background.blit(Jeu.BACKGROUND, (0, 0))
        self.pacman.draw(background)
        return background

    def surface_partie_perdu(self, background):
        """
        Fais clignoter la grille de jeu selon le timer.
        :param background: La surface à retourner.
        :return: Une surface de la grille de jeu qui contient Pac-Man et qui est soit blanche, soit bleu.
        """
        background.blit(Jeu.BACKGROUND, (0, 0))
        self.pacman.draw(background)
        return background

    def get_surface(self) -> pygame.Surface:
        '''
        Construit et retourne l'image de l'état actuel du jeu.
        :return: l'image de l'état actuel du jeu.
        '''
        background = pygame.Surface(Jeu.BACKGROUND.get_size())

        if len(self.pastilles) + len(self.power_pellets) == 0:
            return self.surface_partie_gagnee(background)

        background.blit(Jeu.BACKGROUND, (0, 0))

        self.pastilles.draw(background)
        text_score = Jeu.FONT.render(str(self.score), 1, (255, 255, 255))
        background.blit(text_score, (130 - text_score.get_rect().right, 40))

        if self.timer_jeu.timer_animation.pastilles_visibles:
            text_1up = Jeu.FONT.render('1UP', 1, (255, 255, 255))
            background.blit(text_1up, (70, 0))
            self.power_pellets.draw(background)

        if not self.timer_jeu.timer_fruit.ended and self.timer_jeu.timer_fruit.fruit != TimerFruit.TEMPS_DELAI:
            background.blit(Jeu.FRUIT[self.fruits_mangees if self.fruits_mangees < 13 else 12].image, Fruit.POSITION)
        for fruit in range(self.fruits_mangees + 1 if self.fruits_mangees < 8 else 8):
            background.blit(Jeu.FRUIT[self.fruits_mangees - fruit if fruit < 13 else 12].image,
                            (620 - (self.fruits_mangees - fruit if fruit < 13 else 12) * 50, 815))

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(PacMan.IMAGES[Direction.GAUCHE][1], (50 + life * 60, 815))

        if self.fantome_mange:  # permet d'indiquer les points à coté du fantôme mangé
            if self.frame_fantome_mange + 20 == self.timer_jeu.timer_animation.compteur:
                self.fantome_mange = False
            text_pts = Jeu.FONT2.render(str(self.nbr_fantomes_manges * 200), 1, (3, 240, 252))
            background.blit(text_pts, self.position_fantome_mange)

        if self.fruit_est_mange:  # permet d'indiquer les points à coté d'un fruit mangé
            if self.frame_fruit_mange + 20 == self.timer_jeu.timer_animation.compteur:
                self.fruit_est_mange = False
            text_pts = Jeu.FONT2.render(str(Jeu.FRUIT[self.fruits_mangees if self.fruits_mangees < 13 else 12].score),
                                        1, (185, 44, 232))
            background.blit(text_pts, (Fruit.POSITION[0] - 10, Fruit.POSITION[1] - 10))

        if self.pacman.sprite.is_alive:
            self.fantomes.draw(background)

        self.pacman.draw(background)

        return background

    def ajouter_points_pellet(self):
        """
        Incrémente le score du jeu pour avoir mangé une pastille.
        :return: None
        """
        self.score += 10

    def ajouter_points_powerpellet(self):
        """
        Incrémente le score du jeu pour avoir mangé une grosse pastille.
        :return: None
        """
        self.score += 50

    def ajouter_points_fantome(self):
        """
        Incrémente le score du jeu pour avoir mangé un fantôme.
        :return: None
        """
        self.score += 200 * self.nbr_fantomes_manges

    def get_audio(self):
        """
        Retourne une liste de channel à activer selon l'état du jeu.
        :return: une liste de channel à activer selon l'état du jeu.
        """
        if self.pacman.sprite.is_alive and len(self.pastilles) + len(self.power_pellets) != 0:
            if self.derniere_pastille is not None:
                if pygame.sprite.spritecollideany(self.derniere_pastille,
                                                  self.pacman) and self.pacman.sprite.vitesse != [0, 0]:
                    self.channel_actif[1] = True
                else:
                    self.derniere_pastille = None

            for fantome in self.fantomes:
                if fantome.mode is Mode.EFFRAYE:
                    self.channel_actif[2] = True
                elif fantome.mode is Mode.RETOUR:
                    self.channel_actif[5] = True
                else:
                    self.channel_actif[4] = True
        return self.channel_actif
