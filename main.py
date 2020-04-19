import pygame
import ctrl.ctrl as ctrl
import os

# Initialiser pygame.
pygame.mixer.pre_init(44100, 16, 8, 4096)
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption('Pac-Man')
pygame.display.set_icon(pygame.image.load(os.path.join('ressource', 'images', 'Icon.png')))
#pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # pour mettre en plenine écran

# Le contrôleur débute la partie.
monCtrl = ctrl.Ctrl()
monCtrl.start()

#dernière version 3