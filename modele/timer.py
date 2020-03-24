from modele.modes_fantome import Mode


class TimerAbstrait:
    """
    Classe abstraite d'un timer qui gère le temps en seconde.
    Le timer compte le nombre de frame et le compare avec le frame rate du jeu.
    ATTENTION : Le frame rate est approximé par une constante, il ne faut donc pas avoir de baisse de fps.
    """

    def __init__(self, frame_rate):
        """
        Construit un timer abstrait selon le frame rate.
        :param frame_rate: La vitesse d'affichage du jeu.
        """
        self.current = 0
        self.fin = 0
        self.ended = True
        self.paused = False
        self.frame_rate = frame_rate

    def is_running(self):
        """
        Le temps est incrémenté et retourne «True» si et seulement si le timer est en train de fonctionner.
        :return: «True» si et seulement si le timer est en train de fonctionner.
        """
        if self.ended:
            return False
        self.current += 1
        self.ended = self.fin == self.current
        return not self.ended

    def set_timer(self, seconde):
        """
        Repart un nouveau timer pour une durée un seconde.
        :param seconde: Durée du timer.
        :return: None
        """
        self.current = 0
        self.fin = seconde * self.frame_rate
        self.ended = False

    def update(self):
        """
        Doit être redéfini pour que le timer fasse une tâche plus spécifique.
        :return:
        """
        pass


class TimerJeu(TimerAbstrait):
    """
    Cette classe est le timer du jeu et gère le mode des fantômes et les autres timers.
    """
    TEMPS_DISPERSION = 7
    TEMPS_CHASSE = 20
    TEMPS_EFFRAYE = 10

    def __init__(self, jeu, frame_rate):
        """
        Constructeur du timer.
        :param jeu: Le jeu auquel il appartient.
        :param frame_rate: La vitesse d'affichage du jeu.
        """
        TimerAbstrait.__init__(self, frame_rate)
        self.current_mode = Mode.DISPERSION
        self.set_timer(TimerJeu.TEMPS_DISPERSION)
        self.timer_fantome = TimerFantome(frame_rate)
        self.timer_animation = TimerAnimation(jeu)
        self.jeu = jeu

    def update(self):
        """
        Met à jour le mode des fantômes au bon moment et met à jour les animations des fantômes et de Pac-Man.
        :return: None
        """
        if not self.paused and not self.is_running():
            if self.current_mode == Mode.CHASSE:
                self.current_mode = Mode.DISPERSION
                self.update_mode()
                self.set_timer(TimerJeu.TEMPS_DISPERSION)
            else:
                self.current_mode = Mode.CHASSE
                self.update_mode()
                self.set_timer(TimerJeu.TEMPS_CHASSE)

        elif self.timer_fantome.is_running():
            self.timer_fantome.update()

        elif self.jeu.pacman.sprite.is_alive:
            self.paused = False  # Repartir le timer du jeu.
            self.update_mode()

        self.timer_animation.update(self.timer_fantome)

    def pacman_mort(self):
        """
        Quand Pac-Man meurt, on met sur pause le timer du jeu et
        on remet à 0 le timer d'animation pour l'animation de mort.
        :return: None
        """
        self.paused = True
        self.timer_animation.compteur = 0

    def mode_effraye(self):
        """
        En mode effrayé, le temps du jeu arrête et on démarre un timer de 10 secondes.
        :return: None
        """
        self.paused = True
        self.timer_fantome.set_timer(TimerJeu.TEMPS_EFFRAYE)
        self.timer_fantome.acheve = False

    def update_mode(self):
        """
        S'occupe des changements de mode des fantômes. Cette méthode est appelée seulement à la fin d'un timer.
        :return:
        """
        for fantome in self.jeu.fantomes:
            fantome.peur = False
            if fantome.mode != Mode.INACTIF and fantome.mode != Mode.RETOUR and fantome.mode != Mode.SORTIR:
                fantome.set_mode(self.current_mode)


class TimerFantome(TimerAbstrait):
    """
    Cette classe est le timer des fantômes lorsqu'ils sont effrayé.
    Les fantômes doivent clignoter quand il reste 2 secondes.
    """

    def __init__(self, frame_rate):
        """
        Constructeur du timer des fantômes en mode effrayé.
        :param frame_rate: La vitesse d'affichage du jeu.
        """
        TimerAbstrait.__init__(self, frame_rate)
        self.acheve = False

    def update(self):
        """
        Met à jour l'attribut acheve qui est vrai si et seulement s'il reste 2 secondes au timer.
        :return:
        """
        self.acheve = 8 / 10 * self.fin < self.current


class TimerAnimation:
    """
    Timer d'animation du jeu. Ce timer NE compte PAS des secondes, mais des frames.
    Le timer s'occupe de mettre à jour l'animation des fantômes, de Pac-Man et des grosses pastilles.
    """
    CYCLE = 102

    def __init__(self, jeu):
        """
        Constructeur d'un timer d'animation.
        :param jeu: Le jeu auquel le timer appartient.
        """
        self.compteur = 0
        self.pastilles_visibles = True
        self.action_fantome = 0
        self.jeu = jeu

    def update(self, timer_fantome):
        """
        Met à jour l'image de Pac-Man, des fantômes et des grosses pastilles selon le temps.
        :param timer_fantome: Le timer du mode effrayé des fantômes.
        :return: None
        """
        self.compteur += 1
        if self.compteur == TimerAnimation.CYCLE:
            self.compteur = 0

        if self.compteur % 3 == 0:
            partie_gagnee = len(self.jeu.pastilles) + len(self.jeu.power_pellets) == 0

            self.jeu.pacman.sprite.animation(self.compteur, partie_gagnee)

            if not partie_gagnee:
                if not timer_fantome.ended and timer_fantome.acheve:
                    self.action_fantome = (self.action_fantome + 1) % 4
                else:
                    self.action_fantome = not self.action_fantome

                for fantome in self.jeu.fantomes:
                    fantome.animation(self.action_fantome)

                if self.compteur % 6 == 0:
                    self.pastilles_visibles = not self.pastilles_visibles
