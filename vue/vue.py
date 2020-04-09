import pygame
from modele.direction import Direction
import os

window = pygame.display.set_mode((672, 864))


class Vue:
    """
    Cette classe est la vue du jeu de Pac-Man. Elle permet d'afficher les frames et de jouer de la musique.
    """

    FRAME_RATE = 30
    SOUND = None
    READY = pygame.image.load(os.path.join('ressource', 'images', 'Ready!.png'))

    def __init__(self, p_ctrl):
        """
        Constructeur de la classe.
        :param p_ctrl: Contrôleur du jeu de Pac-Man.
        """
        self.ctrl = p_ctrl
        self.vie_sup = False
        if Vue.SOUND is None:
            Vue.SOUND = [pygame.mixer.Sound(os.path.join('ressource', 'sons', '1_up.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', '1_waka_waka.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'fantome_effraye.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'fantome_mange.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'fantome_normal.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'fantome_retour.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'fruit.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'Intro.ogg')),
                         pygame.mixer.Sound(os.path.join('ressource', 'sons', 'pacman_mort.ogg'))]

        self.channels = [None] * 9
        self.text_font = pygame.font.Font(os.path.abspath("ressource/font/emulogic.ttf"), 26)
        for i in [1, 2, 4, 5]:
            self.channels[i] = Vue.SOUND[i].play(-1)
            self.channels[i].pause()

    def interface_debut(self):
        '''
        Affiche l'interface qui donne le choix d'accéder au jeu en tant que joueur ou IA.
        :return: «True» si le joueur à été sélectionner.
        '''
        PositionP1 = (217, 232)
        PositionIA = (290, 432)
        PositionQuit = (217,632)

        board = pygame.image.load(os.path.join('ressource', 'images', 'Board_Intro.png'))

        player1 = pygame.image.load(os.path.join('ressource', 'images', 'PlayerOne.png'))
        player1_rect = player1.get_rect()
        player1_rect.topleft = PositionP1

        IA = pygame.image.load(os.path.join('ressource', 'images', 'Player_IA.png'))
        IA_rect = IA.get_rect()
        IA_rect.topleft = PositionIA


        text_quitter = self.text_font.render('EXIT GAME', True, (0,255,255))
        text_rect = text_quitter.get_rect()
        text_rect.topleft = PositionQuit

        window.blit(board, (0, 0))
        window.blit(player1, PositionP1)
        window.blit(IA, PositionIA)
        window.blit(text_quitter, PositionQuit)
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif IA_rect.collidepoint(pygame.mouse.get_pos()):
                        print('Ça lance le joueur 1 puisque l\'IA n\'est pas encore prêt :)')
                        return True
                    elif text_rect.collidepoint(pygame.mouse.get_pos()):
                        quit()

    def intro(self):
        """
        Affiche l'image «Ready!.png» au début de la partie et joue la musique du début.
        :return: None
        """
        window.blit(self.ctrl.get_surface(), (0, 0))
        window.blit(Vue.READY, (270, 485))
        pygame.display.update()

        Vue.SOUND[-2].play(loops=0)
        pygame.time.delay(4500)

    def mode_IA(self):
        '''
        Lance une partie avec l'IA.
        :return: None
        '''
        pass

    def audio(self):
        """
        Cette méthode active certains sons selon l'état du jeu.
        :return: None
        """
        channel_actif = self.ctrl.get_audio()

        # Audio mort
        if channel_actif[-1]:
            for channel in self.channels:
                if channel is not None:
                    channel.pause()
            self.channels[-1] = Vue.SOUND[-1].play(loops=0)

        # Audio vie supplémentaire
        elif channel_actif[0] and not self.vie_sup:
            self.vie_sup = True
            self.channels[0] = Vue.SOUND[0].play(loops=0)

        else:
            # Audio manger
            if self.channels[-1] is None or not self.channels[-1].get_busy():
                if channel_actif[3]:
                    self.channels[3] = Vue.SOUND[3].play(loops=0)
                elif channel_actif[6]:
                    self.channels[6] = Vue.SOUND[6].play(loops=0)
                elif channel_actif[1]:
                    self.channels[1].unpause()
                else:
                    self.channels[1].pause()

                # Audio fantômes
                for i in [5, 2, 4]:
                    if channel_actif[i]:
                        for j in [5, 2, 4]:
                            if i == j:
                                self.channels[j].unpause()
                            else:
                                self.channels[j].pause()
                        break
                    elif i == 4:
                        for channel in self.channels:
                            if channel is not None:
                                channel.pause()


    def ready_respawn(self):
        """
        Apparaît l'image «Ready!.png» lorsqu'une partie est relancée.
        :return: None
        """
        window.blit(self.ctrl.get_surface(), (0, 0))
        window.blit(Vue.READY, (270, 485))
        pygame.display.update()

        pygame.time.delay(1500)

    def mode_joueur(self):
        """
        Lance une partie où est-ce-que le joueur peut interagir avec les touches directionnelles.
        :return: None
        """
        quitter = False
        clock = pygame.time.Clock()
        key_pressed = []
        self.vie_sup = False
        self.intro()

        while not quitter:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitter = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_pressed.append(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.append(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.append(Direction.DROITE)
                    if event.key == pygame.K_DOWN:
                        key_pressed.append(Direction.BAS)
                    if event.key == pygame.K_ESCAPE:
                        quitter = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        key_pressed.remove(Direction.GAUCHE)
                    if event.key == pygame.K_UP:
                        key_pressed.remove(Direction.HAUT)
                    if event.key == pygame.K_RIGHT:
                        key_pressed.remove(Direction.DROITE)
                    if event.key == pygame.K_DOWN:
                        key_pressed.remove(Direction.BAS)
                    if event.key == pygame.K_ESCAPE:
                        quitter = True

            if key_pressed:
                p_terminee = self.ctrl.update_jeu(key_pressed[-1])
            else:
                p_terminee = self.ctrl.update_jeu(Direction.AUCUNE)

            if p_terminee:
                if self.ctrl.jeu.pacman.sprite.nbr_vie<0:
                    quitter = True
                else:
                    self.ready_respawn()

            self.audio()
            window.blit(self.ctrl.get_surface(), (0, 0))
            clock.tick(Vue.FRAME_RATE)
            pygame.display.update()

        for ch in self.channels:
            if ch is not None:
                ch.pause()

        self.ctrl.start()
        #LEADERBOARD
        #MAIN MENU

    def mode_IA(self):
        """
        Lance une partie où est-ce-que l'IA joue à notre place'
        :return: None
        """
        # Choose direction using model
        # Send choice to game
        # Read&Save new game_info
