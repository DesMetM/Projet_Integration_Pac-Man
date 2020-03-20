from modele.modes_fantome import Mode


class TimerAbstrait:
    def __init__(self, frame_rate):
        self.current = 0
        self.fin = 0
        self.ended = True
        self.paused = False
        self.frame_rate = frame_rate

    def is_running(self):
        """
        Update aussi le timer.
        :return: «True» si et seulement si le timer est en train de fonctionner.
        """
        if self.ended:
            return False
        self.current += 1
        self.ended = self.fin == self.current
        return not self.ended

    def set_timer(self, seconde):
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
    TEMPS_DISPERSION = 7
    TEMPS_CHASSE = 20
    TEMPS_EFFRAYE = 10

    def __init__(self, jeu, frame_rate):
        TimerAbstrait.__init__(self, frame_rate)
        self.current_mode = Mode.DISPERSION
        self.set_timer(TimerJeu.TEMPS_DISPERSION)
        self.timer_fantome = TimerFantome(frame_rate)
        self.timer_animation = TimerAnimation(jeu)
        self.jeu = jeu

    def update(self):
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
        self.paused = True
        self.timer_animation.compteur = 0

    def mode_effraye(self):
        self.paused = True
        self.timer_fantome.set_timer(TimerJeu.TEMPS_EFFRAYE)
        self.timer_fantome.acheve = False

    def update_mode(self):
        for fantome in self.jeu.fantomes:
            fantome.peur = False
            if fantome.mode != Mode.INACTIF and fantome.mode != Mode.RETOUR and fantome.mode != Mode.SORTIR:
                fantome.set_mode(self.current_mode)


class TimerFantome(TimerAbstrait):
    def __init__(self, frame_rate):
        TimerAbstrait.__init__(self, frame_rate)
        self.acheve = False

    def update(self):
        self.acheve = 8 / 10 * self.fin < self.current


class TimerAnimation:
    CYCLE = 54

    def __init__(self, jeu):
        self.compteur = 0
        self.pastilles_visibles = True
        self.action_fantome = 0
        self.jeu = jeu

    def update(self, timer_fantome):
        self.compteur += 1
        if self.compteur == TimerAnimation.CYCLE:
            self.compteur = 0

        if self.compteur % 3 == 0:
            self.jeu.pacman.sprite.animation(self.compteur)

            if not timer_fantome.ended and timer_fantome.acheve:
                self.action_fantome = (self.action_fantome + 1) % 4
            else:
                self.action_fantome = not self.action_fantome

            for fantome in self.jeu.fantomes:
                fantome.animation(self.action_fantome)

            if self.compteur % 6 == 0:
                self.pastilles_visibles = not self.pastilles_visibles
