import numpy as np


def mse(sortie_attendue, sortie):
    """
    Calcule la moyenne des erreurs au carré (Mean Squared Error).
    :param sortie_attendue: La sortie qu'on voulait obtenir du réseau de neurones.
    :param sortie: La sortie du réseau de neurones.
    :return: la moyenne des erreurs au carré.
    """
    return np.mean(np.power(sortie - sortie_attendue, 2))


def mse_derivee(sortie_attendue, sortie):
    """
    Dérivée de la fonction « mse » par rapport à la sortie du réseau de neurones.
    :param sortie_attendue: La sortie qu'on voulait obtenir du réseau de neurones.
    :param sortie: La sortie du réseau de neurones.
    :return: La dérivée de la fontion « mse » par rapport à la sortie du réseau de neurones.
    """
    return 2 * (sortie - sortie_attendue) / sortie_attendue.size
