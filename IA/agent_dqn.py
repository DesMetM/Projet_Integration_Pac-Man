from _collections import deque
from IA.reseau_neurones.network import Reseau
from IA.reseau_neurones.layers import FCLayer, ActivationLayer
from IA.reseau_neurones.losses import mse, mse_derivee
from IA.reseau_neurones.activations import relu, relu_derivee, bent_identity, bent_identity_derivee
import numpy as np
import random


class AgentDQN:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.memory = deque(maxlen=2000)

        self.gamma = 0.92

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.learning_rate = 0.001

        self.reseau = self._build_reseau()

    def _build_reseau(self):
        reseau = Reseau(mse, mse_derivee)
        reseau.add(FCLayer(self.state_size, 24))
        reseau.add(ActivationLayer(relu, relu_derivee))
        reseau.add(FCLayer(24, 24))
        reseau.add(ActivationLayer(relu, relu_derivee))
        reseau.add(FCLayer(24, 24))
        reseau.add(ActivationLayer(relu, relu_derivee))
        reseau.add(FCLayer(24, self.action_size))
        reseau.add(ActivationLayer(bent_identity, bent_identity_derivee))
        return reseau

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        act_values = self.reseau.predire(state)
        return np.argmax(act_values[0]).item()

    def predict(self, state):
        actions = self.reseau.predire(state)[0]
        action = np.argmax(actions).item()
        print(actions, action, sep="\n")
        return action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward

            if not done:
                target = reward + self.gamma * np.amax(self.reseau.predire(next_state)[0])

            targetf = np.array(self.reseau.predire(state))
            targetf[0][0][action] = target

            self.reseau.apprendre(state, targetf, epochs=1, learning_rate=self.learning_rate, info=False)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.reseau.load(name)

    def save(self, name):
        self.reseau.save(name)
