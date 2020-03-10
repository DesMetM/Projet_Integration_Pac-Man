from pygame.time import get_ticks
from modele.modes_fantome import Mode


class TimerAbstrait:
    def __init__(self):
        self.debut = 0
        self.current = 0
        self.duree = 0
        self.ended = True
        self.paused = False

    def is_running(self):
        """
        Update aussi le timer.
        :return: «True» si et seulement si le timer est en train de fonctionner.
        """
        if self.ended:
            return False
        self.current = get_ticks()
        self.ended = self.duree <= self.current - self.debut
        return not self.ended

    def pause(self):
        """
        Met en pause le timer. Si on appelle la même méthode lorsque le timer est sur pause, le timer repart.
        :return: void
        """
        if self.paused:
            self.debut = get_ticks() - (self.current - self.debut)
            self.current = get_ticks()
            self.paused = False
        else:
            self.paused = True

    def set_timer(self, millis):
        """
        Réinitialise le timer pour une certaine durée en milli-seconde.
        :param millis: Durée du timer en milli-seconde.
        :return: void
        """
        self.debut = get_ticks()
        self.current = self.debut
        self.duree = millis
        self.ended = False
        self.paused = False

    def update(self):
        """
        Doit être redéfini pour que le timer fasse une tâche plus spécifique.
        :return:
        """
        pass


class TimerJeu(TimerAbstrait):
    TEMPS_DISPERSION = 7000
    TEMPS_CHASSE = 20000
    TEMPS_EFFRAYE = 10000

    def __init__(self, jeu):
        TimerAbstrait.__init__(self)
        self.current_mode = Mode.CHASSE
        self.timer_fantome = TimerFantome()
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
        else:
            self.pause()  # Repartir le timer.
            self.update_mode()

    def mode_effraye(self):
        self.pause()
        self.timer_fantome.set_timer(TimerJeu.TEMPS_EFFRAYE)
        self.timer_fantome.acheve = False

    def update_mode(self):
        for fantome in self.jeu.fantomes:
            fantome.peur = False
            if fantome.mode != Mode.INACTIF and fantome.mode != Mode.RETOUR and fantome.mode != Mode.SORTIR:
                fantome.set_mode(self.current_mode)


class TimerFantome(TimerAbstrait):
    def __init__(self):
        TimerAbstrait.__init__(self)
        self.acheve = False

    def update(self):
        self.acheve = 8 / 10 * self.duree < self.current - self.debut
