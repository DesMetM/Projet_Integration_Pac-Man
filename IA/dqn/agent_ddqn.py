from IA.reseau_neurones.network import Reseau
from IA.reseau_neurones.layers import FCLayer, ActivationLayer
from IA.reseau_neurones.losses import mse, mse_derivee
from IA.reseau_neurones.activations import relu, relu_derivee, bent_identity, bent_identity_derivee
from IA.dqn.replay_buffer import PrioritizedReplayBuffer
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

        self.network = self._build_network()
        self.target_network = self._build_network()
        self.target_network.set_weights(self.network.get_weights())

    def _build_network(self):
        network = Reseau(mse, mse_derivee)
        network.add(FCLayer(self.state_size, 24))
        network.add(ActivationLayer(relu, relu_derivee))
        network.add(FCLayer(24, 24))
        network.add(ActivationLayer(relu, relu_derivee))
        network.add(FCLayer(24, self.action_size))
        network.add(ActivationLayer(bent_identity, bent_identity_derivee))
        return network

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        act_values = self.network.predire(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size, a=0.0):
        experiences, importances, indices = self.replay_buffer.sample(batch_size, priority_scale=a)
        errors = []

        for (state, action, reward, next_state, done), importance in zip(experiences, importances):
            q_values = np.array(self.network.predire(state))
            q_value_before = q_values[0][0][action]

            if done:
                q_values[0][0][action] = reward
            else:
                future_reward = np.amax(self.network.predire(next_state)[0])
                q_values[0][0][action] = reward + self.gamma * future_reward

            self.network.apprendre(state, q_values, epochs=1,
                                   learning_rate=self.learning_rate * importance ** (1 - self.epsilon), info=False)
            errors.append(q_values[0][0][action] - q_value_before)

        self.update_weights()
        self.replay_buffer.set_priorities(indices, errors)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_weights(self):
        weights = self.network.get_weights()
        target_weights = self.target_network.get_weights()

        target_weights = weights * self.tau + target_weights * (1 - self.tau)

        self.target_network.set_weights(target_weights)

    def load(self, name):
        self.network.load(name)

    def save(self, name):
        self.network.save(name)