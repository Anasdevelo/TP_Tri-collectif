import numpy as np

from cell import *
from objet import *

class Agent:
    """Un	agent	se	déplace	aléatoirement	d’un	pas	(exprimé	en	nombre	i	(i>=	1)	de	cases,
dans	l’environnement	dans	les	8	directions	autour	de	la	case.	le	nombre	i	est	un
paramètre	que	l’on	fixe	selon	l’étendue	de	l’environnement	et	le	nombre	d’agents
disponibles. L'agent possède une mémoire d'un nombre des cells visitées précédemment."""

    ''' Pour les direction on a 8 directions possible pour un agent '''

    directions = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [1,-1], [-1,1], [-1,-1]]

    def __init__(self, env, cellule, kplus, kmoins, t, taux_erreur):
        # Environnement où prend place l'agent
        self.env = env
        # Cellule où se situe l'agent
        self.cellule = cellule
        # L'objet qu'il est en train de porter (None si aucun)
        self.objet = None
        # Constante de probabilite de prise
        self.kplus = kplus
        # Constante de probabilite de dépot
        self.kmoins = kmoins
        # Liste de taille t représentant la mémoire de l'agent
        self.memoire = ['O' for i in range(t)]
        # Taux d'erreur de discernement des objets (valeur par defaut = 0)
        self.taux_erreur = taux_erreur

    def f(self, type):
      """Calcule la proportion d'objet dans la memoire"""
      nbA = 0
      nbB = 0
      for o in self.memoire:
        if o == 'A':
          nbA += 1
        elif o == 'B':
          nbB += 1
      if type == 'A':
        return (nbA + nbB*self.taux_erreur)/len(self.memoire)
      else:
        return (nbB + nbA*self.taux_erreur)/len(self.memoire)

    def proba_prise(self, type):
      """Probabilite de saisir l'objet de type"""
      return (self.kplus/(self.kplus + self.f(type)))**2

    def proba_depot(self, type):
      """Probabilite de deposer l'objet de type"""
      f = self.f(type)
      return (f/(self.kmoins + f))**2

    def perception(self):
      """Renvoie les cellules voisines de l'agent disponible"""
      x = self.cellule.x
      y = self.cellule.y
      voisin_disponible = []
      for dir in Agent.directions:
        new_x = x+dir[0]
        new_y = y+dir[1]
        if new_x>=0 and new_x<self.env.M and new_y>=0 and new_y<self.env.M:
          cellule = self.env.tableau[new_x, new_y]
          if cellule.agent == None:
            voisin_disponible.append(cellule)
      return voisin_disponible

    def actualiser_memoire(self, cellule_suivante):
      """Actualise la mémoire de l'agent"""
      if cellule_suivante.objet == None:
        type = 'O'
      else:
        type = cellule_suivante.objet.type
      self.memoire = [type] + self.memoire[:-1]

    def move(self,cellule_suivante):
      """Deplacement de l'agent vers la cellule"""
      self.cellule.set_agent(None)
      cellule_suivante.set_agent(self)
      self.cellule = cellule_suivante
      self.actualiser_memoire(cellule_suivante)

    def prendre_objet(self):
      """Prend l'objet situé sur sa cellule"""
      self.objet = self.cellule.objet
      self.cellule.set_objet(None)

    def depot_objet(self):
      """Dépose l'objet sur sa cellule"""
      self.cellule.set_objet(self.objet)
      self.objet = None

    def choix_deplacement(self):
      """Choisi son déplacement de manière aléatoire"""
      voisin = self.perception()
      if len(voisin) == 0:
        return None
      return voisin[np.random.randint(len(voisin))]

    def action(self):
      """Enclenche l'action de l'agent"""
      new_cellule = self.choix_deplacement()
      if new_cellule != None:
        self.move(new_cellule)
        if self.objet == None:
          if self.cellule.objet != None:
            proba = self.proba_prise(self.cellule.objet.type)
            if np.random.rand() < proba:
              self.prendre_objet()
        else:
          if self.cellule.objet == None:
            proba = self.proba_depot(self.objet.type)
            if np.random.rand() < proba:
              self.depot_objet()