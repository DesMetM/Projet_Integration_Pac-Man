import pygame
import ctrl.ctrl as c
import vue.vue as v
import modele.jeu as j

# Initialiser pygame.
pygame.init()
clock = pygame.time.Clock()
clock.tick(30)
# Le contrôleur débute la partie.
monJeu = j.Jeu()
monCtrl = c.Ctrl(monJeu)
monCtrl.start()
