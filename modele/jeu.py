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
        self.partie_terminee = False

    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.pastilles = board.pastilles()
        self.power_pellets = board.grosses_pastilles()
        self.pacman = board.pac_init_pos()
        self.fantomes = board.fantomes_init_pos()
        self.partie_terminee = False

    def pellets_animation(self):
        if self.pellet_anim > 6:
            self.pellet_anim = 0
            for sprite in self.power_pellets:
                sprite.frame = not sprite.frame
                sprite.image = sprite.images[sprite.frame]
        else:
            self.pellet_anim += 1

    def collision(self):
        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.pastilles, dokilla=False, dokillb=True):
            self.pastilles_mangees += 1

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.power_pellets, dokilla=False, dokillb=True):
            print("manger manger manger")

        if pygame.sprite.groupcollide(groupa=self.pacman, groupb=self.fantomes, dokilla=False, dokillb=False):
            self.pacman.sprite.is_alive = False
            self.pacman.sprite.count_anim = 0

    def get_surface(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.pellets_animation()
        self.pastilles.draw(background)
        self.power_pellets.draw(background)

        if self.pacman.sprite.is_alive:
            self.collision()
            self.pacman.sprite.move_animation()
            self.pacman.update(direction)
            self.fantomes.draw(background)

        else:
            self.partie_terminee = self.pacman.sprite.kill_animation()
        self.pacman.draw(background)

        if self.partie_terminee:
            #Créé un nouveau Pac-Man.
            # self.partie_terminee devient vrai seulement à la fin de l'animation de mort.
            pass
        return background
