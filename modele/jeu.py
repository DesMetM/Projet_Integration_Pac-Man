import pygame
import os
import modele.board as board
from modele.modes_fantome import Mode
from modele.timer import TimerJeu
from modele.pacman import PacMan
from modele.direction import Direction


# permet de partir une nouvelle partie avec les éléments
# APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

class Jeu:
    BACKGROUND = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))

    def __init__(self):
        # self.chomp = pygame.mixer.Sound(os.path.join('ressource', 'sons', 'Chomp.wav'))
        self.pastilles = None
        self.power_pellets = None
        self.pacman = None
        self.fantomes = None
        self.blinky = None
        self.pellet_anim = 0
        self.pastilles_mangees = 0
        self.partie_terminee = False
        self.timer_jeu = None
        self.nbr_fantomes_manges = 0
        self.anim_1up = True
        self.font = pygame.font.Font(os.path.abspath("ressource/font/emulogic.ttf"), 20)
        self.score = 0
        # self.bool_chomp = False;
        # pygame.mixer.Sound(os.path.join('ressource','sons','Chomp.wav')).play(-1)

    # débute une nouvelle partie
    def nouvelle_partie(self, frame_rate):
        '''Reset tout pour une nouvelle partie.'''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.pac_init_pos()
        self.fantomes, self.blinky = board.fantomes_init_pos()
        self.partie_terminee = False
        self.timer_jeu = TimerJeu(self, frame_rate)

    """Vérifies les collisions entre les groupes de Sprites(voir board.py)"""

    def collision(self):
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
        '''Point d'entrée du ctrl.'''
        background = pygame.Surface(Jeu.BACKGROUND.get_size())
        background.blit(Jeu.BACKGROUND, (0, 0))

        self.pastilles.draw(background)
        text_score = self.font.render(str(self.score), 1, (255, 255, 255))
        background.blit(text_score, (130 - text_score.get_rect().right, 40))

        if self.timer_jeu.timer_animation.pastilles_visibles:
            text_1up = self.font.render('1UP', 1, (255, 255, 255))
            background.blit(text_1up, (70, 0))
            self.power_pellets.draw(background)

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(PacMan.IMAGES[Direction.GAUCHE][1], (60 + life * 60, 815))

        if self.pacman.sprite.is_alive:
            self.fantomes.draw(background)

        self.pacman.draw(background)

        return background

    def ajouter_points_pellet(self):
        self.score += 10

    def ajouter_points_powerpellet(self):
        self.score += 50

    def ajouter_points_fantome(self):
        self.score += 200 * self.nbr_fantomes_manges
