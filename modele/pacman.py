import os
import pygame
from modele.direction import Direction
import modele.board as board


class PacMan(pygame.sprite.Sprite):
    CNSTE_VITESSE = 6

    def __init__(self, pos):
        self.frame = 0
        pygame.sprite.Sprite.__init__(self)
        self.up_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManUp0.png')),
                          pygame.image.load(os.path.join('ressource', 'images', 'PacManUp1.png'))]
        self.down_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManDown0.png')),
                            pygame.image.load(os.path.join('ressource', 'images', 'PacManDown1.png'))]
        self.left_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft0.png')),
                            pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))]
        self.right_images = [pygame.image.load(os.path.join('ressource', 'images', 'PacManRight0.png')),
                             pygame.image.load(os.path.join('ressource', 'images', 'PacManRight1.png'))]
        self.image = pygame.image.load(os.path.join('ressource', 'images', 'PacManLeft1.png'))
        self.rect = self.image.get_rect(center=pos)
        self.direction = Direction.GAUCHE
        self.vitesse = [0, 0]
        self.count_anim = 0
        self.is_alive = True

    def update(self, direction):
        if direction != Direction.AUCUNE and not board.collision_mur(self.rect, direction):
            self.direction = direction
            self.vitesse = [PacMan.CNSTE_VITESSE * i for i in direction.get_vecteur()]

        elif board.collision_mur(self.rect, self.direction):
            self.vitesse = [0, 0]

        self.rect = self.rect.move(self.vitesse)

    def kill_animation(self):
        if self.count_anim <= 11:
            self.image = pygame.image.load(
                os.path.join(os.path.join('ressource', 'images', 'PacDead' + str(self.count_anim) + '.png')))
            self.count_anim = self.count_anim + 1
        return self.count_anim == 12

    def move_animation(self):
        if self.count_anim > 2:
            self.count_anim = 0

            if self.vitesse != [0, 0]:
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