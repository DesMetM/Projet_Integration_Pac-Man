import unittest
import numpy as np
from reseau_neurones.layers import FCLayer, ActivationLayer
from reseau_neurones.network import Reseau
from reseau_neurones.losses import mse, mse_derivee
from reseau_neurones.activations import sigmoid, sigmoid_derivee, tanh, tanh_derivee


class MyTestCase(unittest.TestCase):
    def test_xor(self):
        reseau = Reseau(mse, mse_derivee)
        reseau.add(FCLayer(2, 3))
        reseau.add(ActivationLayer(tanh, tanh_derivee))
        reseau.add(FCLayer(3, 1))
        reseau.add(ActivationLayer(tanh, tanh_derivee))

        entree = np.array([[[1, 1]], [[1, 0]], [[0, 1]], [[0, 0]]])
        sortie_attendue = np.array([[[0]], [[1]], [[1]], [[0]]])

        reseau.apprendre(entree, sortie_attendue, epochs=1000, learning_rate=0.1)

        predicted = reseau.predire(entree)
        for i in range(4):
            if i == 0 or i == 3:
                self.assertFalse(np.all(predicted[i] > 0.9))
            else:
                self.assertTrue(np.all(predicted[i] > 0.9))

    def test_save_load(self):
        reseau = Reseau(mse, mse_derivee)
        reseau.add(FCLayer(2, 3))
        reseau.add(ActivationLayer(tanh, tanh_derivee))
        reseau.add(FCLayer(3, 1))
        reseau.add(ActivationLayer(tanh, tanh_derivee))

        reseau.save('test.hdf5')
        layers = reseau.layers

        reseau = Reseau(mse, mse_derivee)
        reseau.loss = None
        reseau.loss_derivee = None

        self.assertEqual(0, len(reseau.layers))

        reseau.load("test.hdf5")

        self.assertTrue(callable(reseau.loss))
        self.assertTrue(callable(reseau.loss_derivee))
        self.assertFalse(reseau.loss == reseau.loss_derivee)

        for l1, l2 in zip(layers, reseau.layers):
            self.assertEqual(l1, l2)


if __name__ == '__main__':
    unittest.main()
