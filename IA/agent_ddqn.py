from IA.reseau_neurones.network import Reseau
from IA.reseau_neurones.layers import FCLayer, ActivationLayer
from IA.reseau_neurones.losses import mse, mse_derivee
from IA.reseau_neurones.activations import relu, relu_derivee, bent_identity, bent_identity_derivee
from IA.replay_buffer import PrioritizedReplayBuffer
import numpy as np
import random


class AgentDDQN:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.replay_buffer = PrioritizedReplayBuffer(100000)

        self.gamma = 0.95

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.tau = 0.10
        self.learning_rate = 0.001

        self.model = self._build_model()
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())

    def _build_model(self):
        model = Reseau(mse, mse_derivee)
        model.add(FCLayer(self.state_size, 24))
        model.add(ActivationLayer(relu, relu_derivee))
        model.add(FCLayer(24, 24))
        model.add(ActivationLayer(relu, relu_derivee))
        model.add(FCLayer(24, self.action_size))
        model.add(ActivationLayer(bent_identity, bent_identity_derivee))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        act_values = self.model.predire(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size, a=0.0):
        experiences, importances, indices = self.replay_buffer.sample(batch_size, priority_scale=a)
        errors = []

        for (state, action, reward, next_state, done), importance in zip(experiences, importances):
            q_values = np.array(self.model.predire(state))

            if done:
                q_values[0][0][action] = reward
            else:
                future_action = np.argmax(self.model.predire(next_state)[0])
                q_values[0][0][action] = reward + self.gamma * self.target_model.predire(next_state)[0][0][
                    future_action]

            self.model.apprendre(state, q_values, epochs=1,
                                 learning_rate=self.learning_rate * importance ** (1 - self.epsilon), info=False)
            errors.append(q_values[0][0][action] - self.target_model.predire(state)[0][0][action])

        self.update_weights()
        self.replay_buffer.set_priorities(indices, errors)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_weights(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()

        target_weights = weights * self.tau + target_weights * (1 - self.tau)

        self.target_model.set_weights(target_weights)

    def load(self, name):
        self.model.load(name)

    def save(self, name):
        self.model.save(name)