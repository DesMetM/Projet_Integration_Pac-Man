import pygame
import ctrl.ctrl as ctrl
import os

# Initialiser pygame.
pygame.init()
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Cherry.png')))

# Le contrôleur débute la partie.

monCtrl = ctrl.Ctrl()
monCtrl.start()
