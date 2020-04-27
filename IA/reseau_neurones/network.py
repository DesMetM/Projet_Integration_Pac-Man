from IA.reseau_neurones.layers import FCLayer, ActivationLayer
from IA.reseau_neurones.activations import sigmoid, sigmoid_derivee, tanh, tanh_derivee, relu, relu_derivee, bent_identity, \
    bent_identity_derivee
from IA.reseau_neurones.losses import mse, mse_derivee
import h5py
import numpy as np


class Reseau:
    """
    Cette classe est le réseau de neurones. Elle comprend toutes les couches ajoutées et se comporte selon la fonction
    de perte choisie dans « losses.py ».
    """
    ID_LAYERS = {FCLayer: 0, ActivationLayer: 1}
    ID_ACTIVATIONS = {sigmoid: 0, sigmoid_derivee: 1, tanh: 2, tanh_derivee: 3, relu: 4, relu_derivee: 5,
                      bent_identity: 6, bent_identity_derivee: 7}
    ID_LOSSES = {mse: 0, mse_derivee: 1}

    def __init__(self, loss, loss_derivee):
        self.layers = []
        self.loss = loss
        self.loss_derivee = loss_derivee

    def save(self, path):
        """
        Sauvegarde dans un fichier «.hdf5» les constantes du réseau.
        :param path: le chemin relatif du fichier où sauvegarder.
        :return: None
        """
        with h5py.File(path, 'w') as hf:
            weights = hf.create_group('weights')
            biases = hf.create_group('biases')
            layers = hf.create_group('layers')
            hf.create_dataset('losses', data=[Reseau.ID_LOSSES[self.loss], Reseau.ID_LOSSES[self.loss_derivee]])

            for i, l in enumerate(self.layers):
                if isinstance(l, FCLayer):
                    layers.create_dataset(str(i), data=[Reseau.ID_LAYERS[FCLayer]])
                    weights.create_dataset(str(i), l.weights.shape, data=l.weights)
                    biases.create_dataset(str(i), l.biases.shape, data=l.biases)

                elif isinstance(l, ActivationLayer):
                    layers.create_dataset(str(i),
                                          data=[Reseau.ID_LAYERS[ActivationLayer], Reseau.ID_ACTIVATIONS[l.activation],
                                                Reseau.ID_ACTIVATIONS[l.activation_derivee]])

    def load(self, path):
        """
        Charge les constantes d'un réseau sauvegardé dans un fichier «.hdf5».
        :param path: le chemin du fichier à charger.
        :return: None
        """
        self.layers.clear()

        with h5py.File(path, 'r') as hf:
            for i, loss in enumerate(hf['losses'][:]):
                fonction = 0
                for key, value in Reseau.ID_LOSSES.items():
                    if loss == value:
                        fonction = key
                        break
                if i == 0:
                    self.loss = fonction
                else:
                    self.loss_derivee = fonction

            for l in hf['layers']:
                if hf['layers/' + l][0] == Reseau.ID_LAYERS[FCLayer]:
                    self.layers.append(
                        FCLayer(weights=np.array(hf['weights/' + l]), biases=np.array(hf['biases/' + l])))

                elif hf['layers/' + l][0] == Reseau.ID_LAYERS[ActivationLayer]:
                    fonction = []
                    for activation in hf['layers/' + l][1:]:
                        for key, value in Reseau.ID_ACTIVATIONS.items():
                            if activation == value:
                                fonction.append(key)
                                break
                    self.layers.append(ActivationLayer(fonction[0], fonction[1]))

    def add(self, layer):
        """
        Ajoute une couche au réseau de neurones.
        :param layer: La couche à ajouter.
        :return: None
        """
        self.layers.append(layer)

    def predire(self, entree):
        """
        Fait une prédiction selon l'entrée. Chaque entrée doit être une ligne dans une matrice.
        :param entree: L'entrée du réseau.
        :return: Une liste de toutes les prédictions.
        """
        resultat = []

        for i in range(len(entree)):
            sortie = entree[i]
            for layer in self.layers:
                # La sortie d'une couche devient l'entrée de la prochaine.
                sortie = layer.forward_prop(sortie)
            resultat.append(sortie)

        return resultat

    def apprendre(self, entree, sortie_attendue, epochs=1, learning_rate=0.001,info=True):
        """
        Entraîne le réseau de neurones, c'est-à-dire qu'il ajuste ses paramètres pour mieux prédire.
        :param entree: L'entrée du réseau.
        :param sortie_attendue: La sortie qu'on veut que le réseau apprenne pour son entrée respetive.
        :param epochs: Le nombre de fois qu'on repasse sur l'entrée.
        :param learning_rate: Un scalaire pour ajuster la grandeur des ajustements des constantes des couches.
        :return: None
        """

        for i in range(epochs):
            err = 0
            for j in range(len(entree)):
                # Forward propagation
                sortie = entree[j]
                for layer in self.layers:
                    sortie = layer.forward_prop(sortie)

                # Calculer l'erreur
                err += self.loss(sortie_attendue[j], sortie)

                # Back propagation

                erreur_sortie = self.loss_derivee(sortie_attendue[j], sortie)
                for layer in reversed(self.layers):
                    erreur_sortie = layer.back_prop(erreur_sortie, learning_rate)

            err /= len(entree)
            if info:
                print('epoch %d/%d   erreur=%f' % (i + 1, epochs, err))
