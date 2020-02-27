import pygame
import os
import modele.board as board

# permet de partir une nouvelle partie avec les éléments
class Jeu:

    def __init__(self):
        self.currentPastilles = None
        self.currentPowerP = None
        self.pac = None
        self.fantomes = None
        self.pellet_anim = 0
        self.count_pastille_manger = 0
        self.partie_terminee = False
        self.nouvelle_partie()

    # débute une nouvelle partie
    def nouvelle_partie(self):
        '''Reset tout pour une nouvelle partie.'''
        self.currentPastilles = board.pastille()
        self.currentPowerP = board.grosses_pastilles()
        self.pac = board.pac_init_pos()
        self.fantomes = board.fantomes_init_pos()
        self.partie_terminee = False
    """Anime les Power-pellets(Clignotent)"""
    def pellets_animation(self):
        if self.pellet_anim > 6:
            self.pellet_anim = 0
            for sprite in self.currentPowerP:
                sprite.frame = not sprite.frame
                sprite.image = sprite.images[sprite.frame]
        else:
            self.pellet_anim += 1
    """Vérifies les collisions entre les groupes de Sprites(voir board.py)"""
    def collision(self):
        if pygame.sprite.groupcollide(groupa=self.pac, groupb=self.currentPastilles, dokilla=False, dokillb=True):
            self.count_pastille_manger += 1

        if pygame.sprite.groupcollide(groupa=self.pac, groupb=self.currentPowerP, dokilla=False, dokillb=True):
            print("manger manger manger")

        if pygame.sprite.groupcollide(groupa=self.pac, groupb=self.fantomes, dokilla=False, dokillb=False):
            self.pac.sprite.is_alive = False
            self.pac.sprite.count_anim = 0
    """Coeur du jeu, update la position du Pac-Man, anime les différentes composantes et vérifies les collisions"""
    def get_surface_drawn(self, direction) -> pygame.Surface:
        '''Point d'entrée du ctrl.'''
        background = pygame.image.load(os.path.join('ressource', 'images', 'Board.png'))
        self.pellets_animation()
        self.currentPastilles.draw(background)
        self.currentPowerP.draw(background)

        if self.pac.sprite.is_alive:
            self.collision()
            self.pac.update(direction)
            self.pac.sprite.move_animation()
            self.fantomes.draw(background)

        else:
            self.partie_terminee = self.pac.sprite.kill_animation()
        self.pac.draw(background)

        if self.partie_terminee:
            #Créé un nouveau Pac-Man.
            # self.partie_terminee devient vrai seulement à la fin de l'animation de mort.
            pass
        return background
