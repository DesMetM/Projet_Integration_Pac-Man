import pygame
import os
import modele.board as board
from modele.modes_fantome import Mode
from modele.timer import TimerJeu
from modele.pacman import PacMan
from modele.direction import Direction


class Jeu:
    """
    Cette classe gère le jeu Pac-Man.
    """
    BACKGROUND = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
    BACKGROUND_BLANC = pygame.image.load(os.path.join('ressource', 'images', 'Board_Blanc.png'))
    #PAC0 = pygame.image.load(os.path.join('ressource', 'images', 'PacDead0.png'))
    FONT = None

    def __init__(self, ctrl):
        """
        Le constructeur déclare seulement les attributs. Il faut appeller la méthode nouvelle_partie(self) par la suite.
        """
        self.ctrl = ctrl
        self.pastilles = None
        self.power_pellets = None
        self.pacman = None
        self.fantomes = None
        self.blinky = None
        self.pastilles_mangees = 0
        self.partie_terminee = False
        self.timer_jeu = None
        self.nbr_fantomes_manges = 0
        self.score = 0
        self.count_board_anim = 0


        if Jeu.FONT is None:
            Jeu.FONT = pygame.font.Font(os.path.abspath("ressource/font/emulogic.ttf"), 20)

    def nouvelle_partie(self, frame_rate):
        '''
        Débute une nouvelle partie.
        :param frame_rate: La vitesse que doit compter le timer. Le frame rate doit correspondre à celui de la vue.
        :return: None
        '''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.get_pacman()
        self.fantomes, self.blinky = board.fantomes_init_pos()
        self.partie_terminee = False
        self.timer_jeu = TimerJeu(self, frame_rate)

    def collision(self):
        """
        Cette méthode s'occupe des collisions entre les pastilles, Pac-Man et les fantômes.
        :return: None
        """
        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False,
                                      dokillb=True):  # collision avec une pastille
            self.pastilles_mangees += 1
            self.ajouter_points_pellet()

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False,
                                      dokillb=True):  # collision avec une power pellet
            self.timer_jeu.mode_effraye()
            self.ajouter_points_powerpellet()
            self.nbr_fantomes_manges = 0

            for x in self.fantomes:
                x.peur = True
                if x.mode == Mode.CHASSE or x.mode == Mode.DISPERSION:
                    x.set_mode(Mode.EFFRAYE)

        fantome_list = pygame.sprite.spritecollide(self.pacman.sprite, self.fantomes, False,
                                                   pygame.sprite.collide_circle)

        if fantome_list:  # collision avec un fantome
            for ghost in fantome_list:
                if (ghost.mode is not Mode.EFFRAYE) and (ghost.mode is not Mode.RETOUR):
                    self.pacman.sprite.is_alive = False
                    self.timer_jeu.pacman_mort()
                elif ghost.peur:
                    self.nbr_fantomes_manges += 1
                    self.ajouter_points_fantome()
                    ghost.set_mode(Mode.RETOUR)

    def update_jeu(self, direction):
        """
        Passe au prochain état du jeu selon l'action du joueur.
        :param direction: L'action du joueur.
        :return: None
        """
        self.timer_jeu.update()

        if self.pacman.sprite.is_alive:

            self.collision()
            self.pacman.update(direction)
            self.fantomes.update(self)

        else:
            self.partie_terminee = self.timer_jeu.timer_animation.compteur == 0

        if self.partie_terminee:
            self.partie_terminee = False
            self.pacman.sprite.respawn()
            for fantome in self.fantomes:
                fantome.respawn(self)

    def get_surface(self) -> pygame.Surface:
        '''
        Construit et retourne l'image de l'état actuel du jeu.
        :return: l'image de l'état actuel du jeu.
        '''
        background = pygame.Surface(Jeu.BACKGROUND.get_size())
        background.blit(Jeu.BACKGROUND, (0, 0))

        self.pastilles.draw(background)
        text_score = Jeu.FONT.render(str(self.score), 1, (255, 255, 255))
        background.blit(text_score, (130 - text_score.get_rect().right, 40))

        if self.timer_jeu.timer_animation.pastilles_visibles:
            text_1up = Jeu.FONT.render('1UP', 1, (255, 255, 255))
            background.blit(text_1up, (70, 0))
            self.power_pellets.draw(background)

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(PacMan.IMAGES[Direction.GAUCHE][1], (60 + life * 60, 815))

        if self.pacman.sprite.is_alive:

            '''À enlever, seulement pour que les tests soit moins long'''
            if self.pastilles_mangees == 15:
                self.pastilles.empty()
                self.power_pellets.empty()
                self.pastilles_mangees = 0

            if len(self.pastilles) + len(self.power_pellets) == 0:
                # Change la couleur du board
                self.count_board_anim += 0.25
                if self.count_board_anim < 8:
                    if (self.count_board_anim//1) % 2 == 0:
                        background = self.BACKGROUND_BLANC
                    else:
                        background = self.BACKGROUND
                    return background
                else:
                    self.nouvelle_partie(self.ctrl.vue.FRAME_RATE)
                    self.count_board_anim = 0
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