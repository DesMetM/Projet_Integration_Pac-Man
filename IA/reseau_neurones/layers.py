import numpy as np


class Layer:
    """
    Classe abstraite d'une couche du réseau de neurones.
    """

    def __init__(self):
        self.entree = None
        self.sortie = None

    def forward_prop(self, entree):
        """
        Calcule la sortie de la couche.
        :param entree: Entrée de la couche.
        :return: la sortie de la couche.
        """
        raise NotImplementedError

    def back_prop(self, erreur_sortie, learning_rate):
        """
        Calcule la dérivée de la fonction d'erreur par rapport à l'entrée de la couche.
        :param erreur_sortie: Dérivée de la fonction d'erreur par rapport à la sortie.
        :param learning_rate: Un scalaire pour ajuster la grandeur des ajustements des constantes de la couche.
        :return: la dérivée de la fonction d'erreur par rapport à l'entrée de la couche.
        """
        raise NotImplementedError

    def __eq__(self, other):
        """
        Deux couches sont égales s'ils ont les mêmes comportements pour prédire.
        :param other: Une autre couche.
        :return: «True» si et seulement si les deux couches sont égales.
        """
        raise NotImplementedError


class FCLayer(Layer):
    """
    Classe d'une couche où est-ce-que les neurones d'entrée sont complètement connectés
    aux neurones de sortie (Fully Connected Layer), c'est-à-dire que chaque neurone d'entrée est connecté à chaque
    neurone de sortie.
    """

    def __init__(self, dim_entree=0, dim_sortie=0, weights=None, biases=None):
        super(Layer).__init__()
        if weights is None or biases is None:
            self.weights = np.random.rand(dim_entree, dim_sortie) - 0.5
            self.biases = np.random.rand(1, dim_sortie) - 0.5
        else:
            self.weights = weights
            self.biases = biases

    def forward_prop(self, entree):
        self.entree = entree
        self.sortie = np.dot(self.entree, self.weights) + self.biases
        return self.sortie

    def back_prop(self, erreur_sortie, learning_rate):
        erreur_entree = np.dot(erreur_sortie, self.weights.T)
        erreur_weights = np.dot(self.entree.T, erreur_sortie)

        self.weights -= learning_rate * erreur_weights
        self.biases -= learning_rate * erreur_sortie
        return erreur_entree

    def __eq__(self, other):
        return isinstance(other, FCLayer) and np.all(np.equal(self.weights, other.weights)) and np.all(
            np.equal(self.biases, other.biases))

    def __repr__(self):
        return "Entrée : " + str(self.weights.shape[0]) + "Sortie : " + str(self.weights.shape[1])


class ActivationLayer(Layer):
    """
    Classe d'une couche d'activation où est-ce qu'on passe les entrées de la couche précédente dans une fonction
    d'activation de « activations.py ».
    """

    def __init__(self, activation, activation_derivee):
        super(Layer).__init__()
        self.activation = activation
        self.activation_derivee = activation_derivee

    def forward_prop(self, entree):
        self.entree = entree
        self.sortie = self.activation(self.entree)
        return self.sortie

    def back_prop(self, erreur_sortie, learning_rate):
        return self.activation_derivee(self.entree) * erreur_sortie

    def __eq__(self, other):
        return isinstance(other, ActivationLayer) and self.activation == other.activation and \
               self.activation_derivee == other.activation_derivee
