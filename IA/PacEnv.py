import gym
from gym import spaces
import numpy as np
import pandas as pd

class PacEnv(gym.Env):

  """
  Le df est un dataframe(Pandas) qui va contenir les infos que l'Ia a besoin, donc la position des fantômes, 
  sa position(je crois), le score actuel, etc. Il gardera en mémoire le dernier score enregistré pour voir si son 
  score a augmenté et ainsi déterminer sa récompense(Je ne crois pas que c'est ici que cela se fera tho)
  """
  def __init__(self):
    super(PacEnv, self).__init__()

    self.action_space = spaces.Box(low=np.array([0]), high=np.array([3]), dtype=np.int32)

    # self.observation_space =

  def step(self, action):
    # Take action
      """Dans ce cas-ci, il faudrait feed au jeu l'action que l'IA a choisi. Il va choisir
      une valeur entre 0 et 3 qui représente chacun une direction"""
    # Determine new state
      """ On regarde ce que le move a fait. Est-ce Pac est mort? Est-ce que Pac a eu des points? Si oui cb?"""
    # Determine reward linked with outcome(?)
      """Dependemment du nouveau state, donc de ce qui s'est passé avec l'action, on attribue un reward. De base, 
      toute les actions ont une reward de -1 pour motiver l'IA à travailler rapidement. Il reste à déterminer
      ce que vaut de plus les autres résultats(mort, points, etc)"""
    # Determine if game finished
      """Vérifier si la partie est terminée. La partie est terminée si tous les points sont mangés ou si le Pac n'a
      plus de vies."""
    # Evaluate new state
      """Évalue son état actuel pour que le model puisse prendre la prochaine action"""
    # return new_state, reward, done, None
    pass

  def reset(self):
    # posPac, posFant, nbPts tous remis à depart
    pass

  def render(self, mode='human'):
    pass