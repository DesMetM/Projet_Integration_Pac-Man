import pygame
import os


class Fantome(pygame.sprite.Sprite):
    def __init__(self, pos, nom):
        self.compteur = 0
        self.frame = 0
        self.nom = nom
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join('ressource', 'images', '{0}Left0.png'.format(self.nom))), pygame.image.load(os.path.join('ressource', 'images', '{0}Left1.png'.format(self.nom)))]
        self.images_scared = {1 : pygame.image.load(os.path.join('ressource', 'images', 'Scared00.png'.format(self.nom))),2 : pygame.image.load(os.path.join('ressource', 'images', 'Scared01.png'.format(self.nom))),3 : pygame.image.load(os.path.join('ressource', 'images', 'Scared10.png'.format(self.nom))),4 : pygame.image.load(os.path.join('ressource', 'images', 'Scared11.png'.format(self.nom))) }
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.normal_animation()

    def select_target(self):
        pass

    def move_to_target(self):
        pass

    def get_possible_direction(self):
        pass

    def choose_direction(self, ):
        pass

    def normal_animation(self):
        if self.compteur >2:
            self.compteur = 0
            self.frame = not self.frame
            self.image = self.images[self.frame]
        else:
            self.compteur+=1

    #Cette phase est activé lorsque le Pac-Man mange un power pellet
    def phase_apeuree(self):
        #Doit faire changer la couleur des fantômes
        #Doit durer un temps prédéterminé (20 sec - moins 'niveau')
        #Doit changer la collision avec pacman, au lieu de tuer PacMan, le fantôme meurt
        pass
