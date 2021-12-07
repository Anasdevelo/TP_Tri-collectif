import numpy as np

from cell import *
from objet import *

class Agent:
    """Agent dans le tableau. Peut se déplacer dans le tableau, ramasser/déposer un objet avec une probabilité. Possède une mémoire d'un nombre des cells visitées précédemment.
       Attribut :
         - env : Environnement où prend place l'agent
         - cellule : Cellule où se situe l'agent
         - objet : L'objet qu'il est en train de porter (None si aucun)
         - kplus : Constante de probabilite de prise
         - kmoins : Constante de probabilite de dépot
         - memoire : Liste de taille t représentant la mémoire de l'agent
         - etat : Etat de l'agent (Free, Help, Follow, Looking for, Leader)
         - quantite : quantite de pheromone envoyee
         - leader : Agent leader si il est en follow
         - follower : Agent suiveur si il est leader
         - time_waiting : Depuis combien de temps l'agent attend de l'aide
         - temps_attente : temps d'attente avant d'abandonner la recherche d'aide"""

    directions = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [1,-1], [-1,1], [-1,-1]]

    def __init__(self, env, cellule, kplus, kmoins, t, S, temps_attente):
        self.env = env
        self.cellule = cellule
        self.objet = None
        self.kplus = kplus
        self.kmoins = kmoins
        self.memoire = ['O' for i in range(t)]
        self.etat = "free"
        self.quantite = S
        self.leader : Agent = None
        self.follower : Agent = None
        self.time_waiting = 0
        self.temps_attente = temps_attente

    def f(self, type):
      """Calcule la proportion d'objet dans la memoire"""
      nbA = 0
      nbB = 0
      nbC = 0
      for o in self.memoire:
        if o == 'A':
          nbA += 1
        elif o == 'B':
          nbB += 1
        elif o == 'C':
          nbC += 1
      if type == 'A':
        return (nbA)/len(self.memoire)
      elif type == 'B':
        return (nbB)/len(self.memoire)
      else:
        return (nbC)/len(self.memoire)

    def proba_prise(self, type):
      """Probabilite de saisir l'objet de type"""
      return (self.kplus/(self.kplus + self.f(type)))**2

    def proba_depot(self, type):
      """Probabilite de deposer l'objet de type"""
      f = self.f(type)
      return (f/(self.kmoins + f))**2

    def perception(self):
      """Renvoie les cellules voisines de l'agent"""
      x = self.cellule.x
      y = self.cellule.y
      voisin = []
      for dir in Agent.directions:
        new_x = x+dir[0]
        new_y = y+dir[1]
        if new_x>=0 and new_x<self.env.M and new_y>=0 and new_y<self.env.M:
          cellule = self.env.tableau[new_x, new_y]
          voisin.append(cellule)
      return voisin

    def mouvement_disponible(self):
      """Renvoie les cellules voisines disponible pour un mouvement"""
      voisin = self.perception()
      voisin_disponible = []
      for cell in voisin:
        if cell.agent == None:
          voisin_disponible.append(cell)
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
      if cellule_suivante != None:
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

    def emission_pheromone(self):
      """Envoie de la pheromone sur les cellules disponibles"""
      voisin = self.perception()
      self.cellule.set_pheromone(self.cellule.get_pheromone() + self.quantite)
      for cell in voisin:
        cell.set_pheromone(cell.get_pheromone() + self.quantite/2)

    def choix_deplacement(self):
      """Choisi son déplacement de manière aléatoire"""
      if self.etat == "free" or self.etat == "leader": #il choisi son deplacement aleatoirement
        mouvement_disponible = self.mouvement_disponible()
        if len(mouvement_disponible) == 0:
          return None
        return mouvement_disponible[np.random.randint(len(mouvement_disponible))]

      elif self.etat == "Looking for": #il recherche le max de phéromone, s'il se situe deja dessus il redevient free
        voisin = self.perception()
        for cell in voisin:
          if cell.agent != None:
            if cell.agent.etat == "help":
              self.etat = "follow"
              self.leader = cell.agent
              cell.agent.etat = "leader"
              cell.agent.follower = self
              cell.agent.time_waiting = 0
              return None
        mouvement_disponible = self.mouvement_disponible()
        if len(mouvement_disponible) == 0:
          return None
        new_cell = None
        max_pheromone = 0
        for cell in mouvement_disponible:
          if cell.get_pheromone() > max_pheromone:
            new_cell = cell
            max_pheromone = cell.get_pheromone()
        if max_pheromone < self.cellule.get_pheromone():
          self.etat = "free"
          return mouvement_disponible[np.random.randint(len(mouvement_disponible))]
        else:
          return new_cell

      else:
        return None

    def action(self):
      """Enclenche l'action de l'agent"""
      new_cellule = self.choix_deplacement()
      if self.etat == "free": #Si l'agent est free, il agit comme avant sauf s'il tombe sur un objet C et qu'il veut le ramasser
        if new_cellule != None:
          self.move(new_cellule)
          if self.objet != None:
            if self.cellule.objet == None:
              proba = self.proba_depot(self.objet.type)
              if np.random.rand() < proba:
                self.depot_objet()
          else:
            if self.cellule.objet != None:
              proba = self.proba_prise(self.cellule.objet.type)
              if np.random.rand() < proba:
                if self.cellule.objet.type != 'C':
                  self.prendre_objet()
                else:
                  self.etat = "help"
                  self.emission_pheromone()
            else:
              taux_pheromone = self.cellule.get_pheromone()
              if taux_pheromone > 20:
                self.etat = "Looking for"

      elif self.etat == "follow": #Si il est follow, new_cellule == None sauf au tout début où new_cellule est la position du leader
        self.move(new_cellule)

      elif self.etat == "leader": #Si il est leader alors il se comporte comme un free (mais seulement avec les objets C)
        if self.objet == None:
          self.prendre_objet()
        else:
          if new_cellule != None:
            old_cell = self.cellule
            self.move(new_cellule)
            self.follower.move(old_cell)
            if self.cellule.objet == None:
              proba = self.proba_depot(self.objet.type)
              if np.random.rand() < proba:
                self.depot_objet()
                self.etat = "free"
                self.follower.etat = "free"
                self.follower.leader = None
                self.follower = None

      elif self.etat == "Looking for": #Si il est en looking for, new_cellule est le max de phéromone des voisins
        self.move(new_cellule)

      else: #Si il est en help, il continue de demander de l'aide jusqu'à un changement
        self.time_waiting += 1
        if self.time_waiting > self.temps_attente:
          self.etat = "free"
          self.time_waiting = 0
        else:
          self.emission_pheromone()
          self.memoire = ['O'] + self.memoire[:-1]