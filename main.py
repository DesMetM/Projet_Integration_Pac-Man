import pygame
import ctrl.ctrl as c
import vue.vue as v
import modele.jeu as j

# Initialiser pygame.
pygame.init()

# Le contrôleur débute la partie.
monJeu = j.Jeu()
monCtrl = c.Ctrl(monJeu)
monCtrl.start()
