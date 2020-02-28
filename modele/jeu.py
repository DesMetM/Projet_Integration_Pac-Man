import pygame
import os
import modele.board as board


# permet de partir une nouvelle partie avec les éléments
class Jeu:

    def __init__(self):
        self.pastilles = None
        self.power_pellets = None
        self.pacman = None
        self.fantomes = None
        self.pellet_anim = 0
        self.pastilles_mangees = 0
        self.tests = None
        self.ready = None
        self.partie_terminee = False
        self.nouvelle_partie()
        self.nbr_vie = 5

    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.pac_init_pos()
        self.fantomes = board.fantomes_init_pos()
        self.tests = board.tests()
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
        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False, dokillb=True):
            self.pastilles_mangees += 1

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False, dokillb=True):
            print('La nourriture c\'est la vie --- ' * 3)
            #self.fantomes.sprite.phase_apeuree()

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.fantomes, dokilla=False, dokillb=False):
            self.pacman.sprite.is_alive = False
            self.pacman.sprite.count_anim = 0

    def get_surface(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.pellets_animation()
        self.pastilles.draw(background)
        self.power_pellets.draw(background)
        self.tests.draw(background)

        for life in range(self.pacman.sprite.nbr_vie):
            background.blit(self.pacman.sprite.left_images[1], (60 + life * 60, 815))

        if self.pacman.sprite.is_alive:
            self.collision()
            self.pacman.update(direction)
            self.pacman.sprite.move_animation()
            board.detecte_noeud(self.pacman.sprite.rect)
            self.fantomes.update()
            self.fantomes.draw(background)

        else:
            self.partie_terminee = self.pacman.sprite.kill_animation()
        self.pacman.draw(background)

        if self.partie_terminee:
            self.partie_terminee = False
            self.pacman.sprite.respawn()
        return background
