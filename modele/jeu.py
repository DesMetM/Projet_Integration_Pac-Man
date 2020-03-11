import pygame
import os
import modele.board as board
from modele.modes_fantome import Mode
from modele.timer import TimerJeu


# permet de partir une nouvelle partie avec les éléments
# APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

class Jeu:
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
        self.nbr_vie = 5
        self.timer_jeu = TimerJeu(self)

        self.nouvelle_partie()
        self.score = 0
        # self.bool_chomp = False;
        # pygame.mixer.Sound(os.path.join('ressource','sons','Chomp.wav')).play(-1)

    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.pac_init_pos()
        self.fantomes, self.blinky = board.fantomes_init_pos()
        self.partie_terminee = False

    """Anime les Power-pellets(Clignotent)"""

    def pellets_animation(self):
        if self.pellet_anim > 6:
            self.pellet_anim = 0
            for sprite in self.power_pellets:
                sprite.frame = not sprite.frame
                sprite.image = sprite.images[sprite.frame]
        else:
            self.pellet_anim += 1

    """Vérifies les collisions entre les groupes de Sprites(voir board.py)"""

    def collision(self):
        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False,
                                      dokillb=True):  # collision avec une pastille
            self.pastilles_mangees += 1
            self.ajouter_points_pellet()

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False, dokillb=True):
            self.timer_jeu.mode_effraye()
            self.ajouter_points_powerpellet()

            for x in self.fantomes:
                x.peur = True
                if x.mode == Mode.CHASSE or x.mode == Mode.DISPERSION:
                    x.set_mode(Mode.EFFRAYE)
                    self.phase_effraye = True

        fantome_list = pygame.sprite.spritecollide(self.pacman.sprite, self.fantomes, False,
                                                   pygame.sprite.collide_circle)

        if fantome_list:  # collision avec un fantome
            for ghost in fantome_list:
                if (ghost.mode is not Mode.EFFRAYE) and (ghost.mode is not Mode.RETOUR):
                    self.pacman.sprite.is_alive = False
                    self.pacman.sprite.count_anim = 0
                    self.timer_jeu.pause()
                elif ghost.mode is Mode.EFFRAYE:
                    ghost.set_mode(Mode.RETOUR)

    def get_surface(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.pellets_animation()
        self.pastilles.draw(background)
        self.power_pellets.draw(background)

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(self.pacman.sprite.left_images[1], (60 + life * 60, 815))

        self.timer_jeu.update()

        if self.pacman.sprite.is_alive:
            self.collision()
            self.pacman.update(direction)
            self.pacman.sprite.move_animation()
            board.detecte_noeud(self.pacman.sprite.rect)
            self.fantomes.update(self)
            self.fantomes.draw(background)

        else:
            self.partie_terminee = self.pacman.sprite.kill_animation()
        self.pacman.draw(background)

        if self.partie_terminee:
            self.partie_terminee = False
            self.pacman.sprite.respawn()
            for fantome in self.fantomes:
                fantome.respawn(self)

        font = pygame.font.SysFont(None, 30)
        text_score = font.render(str(self.score), 1, (255, 255, 255))
        text_1up = font.render('1UP', 1, (255, 255, 255))

        background.blit(text_score, (70, 40))
        background.blit(text_1up, (70, 0))

        return background

    def ajouter_points_pellet(self):
        self.score += 10

    def ajouter_points_powerpellet(self):
        self.score += 50
