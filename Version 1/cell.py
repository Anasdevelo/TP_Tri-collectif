import numpy as np

from agents import *
from objet import *

class Cell:

    """C'est une case de notre grille, elle peut contient soit un objet A ou B, soit un agent soit les deux."""

    def __init__(self, x, y, agent, objet):
        # Coordonnée du la cellule sur la grille
        self.x = x
        # Coordonnée du la cellule sur la grille
        self.y = y
        # l'agent sur la cell ou None si aucun
        self.agent = agent
        # A, B ou None si aucun
        self.objet = objet

    def set_agent(self, agent):
        self.agent = agent

    def set_objet(self, objet):
        self.objet = objet