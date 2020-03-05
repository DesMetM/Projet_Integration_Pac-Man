import pygame
import os, sys
import modele.board as board
from modele.modes_fantome import Mode
from modele.fantome import Fantome


# permet de partir une nouvelle partie avec les éléments
#APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

class Jeu:
    def __init__(self):
        #self.chomp = pygame.mixer.Sound(os.path.join('ressource', 'sons', 'Chomp.wav'))
        self.pastilles = None
        self.power_pellets = None
        self.pacman = None
        self.fantomes = None
        self.blinky = None
        self.pellet_anim = 0
        self.pastilles_mangees = 0
        self.ready = None
        self.partie_terminee = False
        self.nouvelle_partie()
        self.nbr_vie = 5
        self.phase_effraye = False
        self._CURRENT_MODE = Mode.CHASSE
        #self.bool_chomp = False;
        #pygame.mixer.Sound(os.path.join('ressource','sons','Chomp.wav')).play(-1)
    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.pac_init_pos()
        self.fantomes, self.blinky = board.fantomes_init_pos()
        self.partie_terminee = False
        # self.ready = board.ready()

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

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False, dokillb=True):
            self.pastilles_mangees += 1

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False, dokillb=True):
            for x in self.fantomes:
                Fantome.compteur_peur = 0
                Fantome.acheve = False
                if x.mode != Mode.INACTIF:
                    x.set_mode(Mode.EFFRAYE)
                    self.phase_effraye = True
        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.fantomes, dokilla=False, dokillb=False):
            self.encore_effraye()
            if not self.phase_effraye:
                self.pacman.sprite.is_alive = False
                self.pacman.sprite.count_anim = 0
            else:
                #DÉTECTER QUEL FANTOME A ÉTÉ MANGÉ
                #AJOUTER POINTS
                #SET_MODE
                pass
    def encore_effraye(self):
        self.phase_effraye = False
        for f in self.fantomes:
            if f.mode == Mode.EFFRAYE:
                self.phase_effraye = True


    def get_surface(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.pellets_animation()
        self.pastilles.draw(background)
        self.power_pellets.draw(background)

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(self.pacman.sprite.left_images[1], (60 + life * 60, 815))

        if Fantome.compteur_peur >= Fantome.compteur_ini + Fantome.temps_max:
            for f in self.fantomes:
                if f.mode != Mode.INACTIF:
                    f.set_mode(self._CURRENT_MODE)
            Fantome.acheve = False
            Fantome.compteur_peur=0

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
        return background
