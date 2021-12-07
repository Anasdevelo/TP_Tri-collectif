import numpy as np

from agents import *
from objet import *

class Cell:
    """Case du tableau; elle peut contenir un objet (A ou B ou C), un agent ou les deux.
       Attribute :
         - x,y : Coordonnée du la cellule sur le plateau
         - agent : l'agent sur la cell ou None si aucun
         - objet : A, B ou None si aucun
         - taux : le taux de phéromone sur la case"""

    def __init__(self, x, y, agent, objet):
        self.x = x
        self.y = y
        self.agent = agent
        self.objet : Objet = objet
        self.taux = 0

    def set_agent(self, agent):
        self.agent = agent

    def set_objet(self, objet):
        self.objet = objet

    def get_pheromone(self):
        return self.taux

    def set_pheromone(self, n):
        self.taux = n

    def attenuation_pheromone(self, r):
        self.set_pheromone(self.get_pheromone()*(1-r))