import numpy as np
import matplotlib.pyplot as plt

from cell import *
from objet import *
from agents import *

class Environnement:
    """ Notre environnement	représenté par	une	grille	(matrice NxM) disposé des agents et des objets.
           on initialise l'environnement
           - nA : Nombre d'objet de type A
           - nB : Nombre d'objet de type B
           - nAgent : Nombre d'agent
           - kplus : Constante de probabilite de prise
           - kmoins : Constante de probabilite de dépot
           - t : Mémoire des agents
           - taux_erreur : Pourcentage d'erreur dans la reconnaissance d'objet"""

    def __init__(self, M, N, nA, nB, nAgent, kplus, kmoins, t, taux_erreur=0):
        
        # Nombre de lignes du tableau
        self.M = M
        # Nombre de colonnes du tableau 
        self.N = N
        self.init_tableau(M, N, nA, nB, nAgent, kplus, kmoins, t, taux_erreur)

    def init_tableau(self, M, N, nA, nB, nAgent, kplus, kmoins, t, taux_erreur):
        self.tableau = np.zeros((M,N),dtype=Cell)
        #Création des cellules vides
        for i in range(M):
            for j in range(N):
                self.tableau[i,j] = Cell(i, j, None, None)

        #Placement aléatoire des objets A
        for k in range(nA):
            x = np.random.randint(M)
            y = np.random.randint(N)
            while self.tableau[x,y].objet != None:
                x = np.random.randint(M)
                y = np.random.randint(N)
            self.tableau[x,y].set_objet(Objet('A'))
        
        #Placement aléatoire des objets B
        for k in range(nB):
            x = np.random.randint(M)
            y = np.random.randint(N)
            while self.tableau[x,y].objet != None:
                x = np.random.randint(M)
                y = np.random.randint(N)
            self.tableau[x,y].set_objet(Objet('B'))
               
        #Placement aléatoire des agents
        for k in range(nAgent):
            x = np.random.randint(M)
            y = np.random.randint(N)
            while self.tableau[x,y].agent != None:
                x = np.random.randint(M)
                y = np.random.randint(N)
            self.tableau[x,y].set_agent(Agent(self, self.tableau[x, y], kplus, kmoins, t, taux_erreur))

    def coord_agents(self):
        """Renvoie les coordonnées de tous les agents sur le terrain, cette fonction sert pour la représentation graphique"""
        X = []
        Y = []
        for i in range(self.M):
            for j in range(self.N):
                if self.tableau[i,j].agent != None:
                    X.append(i)
                    Y.append(j)
        return (X,Y)

    def coord_objet(self, type):
        """Renvoie les coordonnées de tous les objets de type, fonction à but graphique"""
        X = []
        Y = []
        for i in range(self.M):
            for j in range(self.N):
                if self.tableau[i,j].objet != None:
                    if self.tableau[i,j].objet.type == type:
                        X.append(i)
                        Y.append(j)
        return (X,Y)

    def run_without_saving(self, n, plots, fig, animation_speed, animation_freq):
        """Fonction qui lance la simulation et actualise le graphique"""
        for k in range(n):
            for i in range(self.M):
                for j in range(self.N):
                    if self.tableau[i,j].agent != None:
                        self.tableau[i,j].agent.action()

            #Actualise le graphique a une fréquence donnée et un vitesse donnée
            if k%animation_freq == 0:
                (X,Y) = self.coord_objet('A')
                plots[0].set_data(X,Y)

                (X,Y) = self.coord_objet('B')
                plots[1].set_data(X,Y)

                (X,Y) = self.coord_agents()
                plots[2].set_data(X,Y)

                #Permet d'actualiser le graphique
                plt.pause(animation_speed)

    def run_with_saving(self, n):
        """Fonction qui lance la simulation et renvoie toutes les données à animer"""
        XA = []
        YA = []
        XB = []
        YB = []
        Xagent = []
        Yagent = []
        for k in range(n):
            for i in range(self.M):
                for j in range(self.N):
                    if self.tableau[i,j].agent != None:
                        self.tableau[i,j].agent.action()

            (X,Y) = self.coord_agents()
            Xagent.append(X)
            Yagent.append(Y)
            (X,Y) = self.coord_objet('A')
            XA.append(X)
            YA.append(Y)
            (X,Y) = self.coord_objet('B')
            XB.append(X)
            YB.append(Y)
        return(XA, YA, XB, YB, Xagent, Yagent)