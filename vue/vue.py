import os
import pygame
from modele.leaderboard import Leaderboard
from modele.direction import Direction
from tkinter.filedialog import askopenfilename

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
        self.__action_ia = 4
        for i in [1, 2, 4, 5]:
            self.channels[i] = Vue.SOUND[i].play(-1)
            self.channels[i].pause()

    def interface_debut(self):
        '''
        Affiche l'interface qui donne le choix d'accéder au jeu en tant que joueur ou IA.
        :return: «True» si le joueur à été sélectionner.
        '''
        PositionP1 = (217, 232)
        PositionIA = (310, 432)
        PositionQuit = (217, 632)

        board = pygame.image.load(os.path.join('ressource', 'images', 'Board_Intro.png'))

        player1 = pygame.image.load(os.path.join('ressource', 'images', 'PlayerOne.png'))
        player1_rect = player1.get_rect()
        player1_rect.topleft = PositionP1

        IA = pygame.image.load(os.path.join('ressource', 'images', 'Player_IA.png'))
        IA_rect = IA.get_rect()
        IA_rect.topleft = PositionIA

        text_quitter = self.text_font.render('EXIT GAME', True, (0, 255, 255))
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
                    return 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(pygame.mouse.get_pos()):
                        return 1
                    elif IA_rect.collidepoint(pygame.mouse.get_pos()):
                        return 2
                    elif text_rect.collidepoint(pygame.mouse.get_pos()):
                        return 3

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

    def update_action_ia(self, action):
        self.__action_ia = action

    def mode_IA(self):
        '''
        Lance une partie avec l'IA.
        :return: None
        '''

        name = askopenfilename(initialdir=os.path.join('ressource', 'IA'),
                               filetypes=(("Fichiers HDF5", "*.hdf5"), ("All Files", "*.*")))

        if name[-4:] != "hdf5":
            return False

        self.ctrl.load_agent_dqn(name)

        done = False
        is_alive = True
        clock = pygame.time.Clock()
        self.vie_sup = False
        self.intro()

        while not done:
            surface, audio, done, info = self.ctrl.get_surface_dqn()

            if done:
                break
            elif not is_alive and info:
                self.ready_respawn()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_ESCAPE:
                    done = True

            is_alive = info

            self.audio()
            window.blit(surface, (0, 0))
            clock.tick(Vue.FRAME_RATE)
            pygame.display.update()

        self.gameover()
        return False

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
        :return: «True» si et seulement si le jeu doit fermer.
        """
        quitter = False
        clock = pygame.time.Clock()
        key_pressed = []
        self.vie_sup = False
        self.intro()

        while not quitter:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

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
                if self.ctrl.jeu.pacman.sprite.nbr_vie == 0:
                    quitter = True
                else:
                    self.ready_respawn()

            self.audio()
            window.blit(self.ctrl.get_surface(), (0, 0))
            clock.tick(Vue.FRAME_RATE)
            pygame.display.update()

        self.gameover()
        self.leaderboard()
        return False

    def leaderboard(self):
        # LeaderBoard
        self.leader_board = Leaderboard()
        board = pygame.image.load(os.path.join('ressource', 'images', 'Board_Intro.png'))
        window.blit(board, (0, 0))

        # Voici la liste de tous les textes prédéfinis
        texte_instruction1 = self.text_font.render('Entrer votre nom et', True, (255, 255, 255))
        texte_instruction2 = self.text_font.render('appuyer sur', True, (255, 255, 255))
        texte_instruction3 = self.text_font.render('la touche retour', True, (255, 255, 255))
        texte_leaderboard = self.text_font.render('LEADERBOARD', True, (0, 55, 255))
        texte_quitter1 = self.text_font.render('Appuyer sur la touche', True, (255, 255, 255))
        texte_quitter2 = self.text_font.render('espace pour quitter', True, (255, 255, 255))

        # Couleur pour les noms dans le leaderboard
        couleurs_c = ((255, 153, 153), (255, 102, 102), (255, 51, 51), (255, 153, 51), (255, 255, 51))
        couleurs_f = ((51, 255, 255), (51, 153, 255), (51, 51, 255), (153, 51, 255), (255, 51, 255))

        # la boucle permet d'entrer le nom du joueur et de voir le texte se rafraichir à toutes les fois qu'une touche est appuyé
        name = ''
        enter_name = True
        while enter_name:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        enter_name = False
            window.blit(board, (0, 0))
            texte_nom = self.text_font.render(name, True, (255, 255, 255))

            window.blit(texte_nom, (336 - (texte_nom.get_rect().width / 2), 485))
            window.blit(texte_instruction1, (336 - (texte_instruction1.get_rect().width / 2), 185))
            window.blit(texte_instruction2, (336 - (texte_instruction2.get_rect().width / 2), 235))
            window.blit(texte_instruction3, (336 - (texte_instruction3.get_rect().width / 2), 285))
            pygame.display.flip()

        # classe les meilleurs score afin d'afficher le meilleur classement
        self.leader_board.compare_lead(score=self.ctrl.jeu.score, name=name)

        # affiche le leaderboard par colonne et applique la police et la couleur en plus de les alligner
        window.blit(board, (0, 0))
        pressed_enter = True
        while pressed_enter:
            for i in range(5):
                if self.leader_board.df.loc[i]['name'] == name:
                    window.blit(self.text_font.render(self.leader_board.df.loc[i]['name'], True, (0, 255, 0)),
                                (150, 235 + i * 50))
                else:
                    window.blit(self.text_font.render(self.leader_board.df.loc[i]['name'], True, couleurs_c[i]),
                                (150, 235 + i * 50))
            for i in range(5):
                if self.leader_board.df.loc[i]['score'] == self.ctrl.jeu.score:
                    window.blit(self.text_font.render(str(self.leader_board.df.loc[i]['score']), True, (0, 255, 0)),
                                (450, 235 + i * 50))
                else:
                    '''juste après le True, on peut changer la couleur du texte du leaderboard en changeant couleur_c 
                    par couleur_f '''
                    window.blit(self.text_font.render(str(self.leader_board.df.loc[i]['score']), True, couleurs_c[i]),
                                (450, 235 + i * 50))
            window.blit(texte_leaderboard, (336 - (texte_leaderboard.get_rect().width / 2), 85))
            window.blit(texte_quitter1, (336 - (texte_quitter1.get_rect().width / 2), 635))
            window.blit(texte_quitter2, (336 - (texte_quitter2.get_rect().width / 2), 685))
            pygame.display.flip()

            # boucle permettant au joueur de cliquer sur espace pour quitter le leaderboard
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pressed_enter = False

    def gameover(self):
        for ch in self.channels:
            if ch is not None:
                ch.pause()

            # Game over
        board = pygame.image.load(os.path.join('ressource', 'images', 'Board_Intro.png'))
        window.blit(board, (0, 0))

        texteG_O = self.text_font.render('GAME  OVER', True, (255, 0, 0))
        texte_pos = (205, 485)
        window.blit(texteG_O, texte_pos)

        pygame.display.flip()

        pygame.time.delay(3000)

