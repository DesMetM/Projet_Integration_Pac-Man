import pygame
import ctrl.ctrl as ctrl
import os
from random import randint
#from modele.direction import Direction

# Initialiser pygame.
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')))

# Le contrôleur débute la partie.
monCtrl = ctrl.Ctrl()
monCtrl.start()
#print(Direction.GAUCHE.opposee())
