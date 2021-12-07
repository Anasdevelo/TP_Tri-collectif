import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from environnement import *

#initialisation des paramètres du tri
M = 50
N = 50
nA = 50
nB = 50
nC = 50
nAgent = 100
kplus = 0.1
kmoins = 0.3
t = 10
S = 10
att_pheromone = 0.2
temps_attente = 10
nbTour = 5000

#les paramètres d'animation(vous pouvez modifier les deux parametres)
animation_speed = 0.01 #temps entre 2 images (en seconde )
animation_freq = 1 #Nombre de tour entre 2 images

jeu = Environnement(M,N,nA,nB,nC,nAgent,kplus,kmoins,t, S, att_pheromone, temps_attente)

fig, ax = plt.subplots()

#l'utilisateur peut sauvegarder l'animation,alors:
reponse_user = input("Voulez-vous sauvegarder l'animation (y/n, defaut n)?  ")
savefile = reponse_user == 'y'
# Si l'utilisateur choisit de sauvergarder le programme prendra plus de temps à démarrer, et pour un nbTour trop élevé avec un animation_freq trop faible, le programme risque de ne pas fini

#Plot du début
(XA, YA) = jeu.coord_objet('A')
(XB, YB) = jeu.coord_objet('B')
(XC, YC) = jeu.coord_objet('C')
(Xagent, Yagent) = jeu.coord_agents()
plot = ax.plot(XA, YA, 'bo', XB, YB, 'ro', XC, YC, 'go', Xagent, Yagent, 'k1')
fig.suptitle('Taille mémoire = '+str(t))


if not savefile:
    #Permet d'actualiser le graphique
    plt.pause(animation_speed)

    jeu.run_without_saving(nbTour, plot, fig, animation_speed, animation_freq)

    #Plot de fin
    (XA, YA) = jeu.coord_objet('A')
    (XB, YB) = jeu.coord_objet('B')
    (XC, YC) = jeu.coord_objet('C')
    (Xagent, Yagent) = jeu.coord_agents()
    plot[0].set_data(XA,YA)
    plot[1].set_data(XB,YB)
    plot[2].set_data(XC, YC)
    plot[3].set_data(Xagent,Yagent)
else:
    XA, YA, XB, YB, XC, YC, Xagent, Yagent = jeu.run_with_saving(nbTour)

    def update(i):
        actual_i = i*animation_freq
        if actual_i < nbTour:
            plot[0].set_data(XA[actual_i], YA[actual_i])
            plot[1].set_data(XB[actual_i], YB[actual_i])
            plot[2].set_data(XC[actual_i], YC[actual_i])
            plot[3].set_data(Xagent[actual_i], Yagent[actual_i])
        else:
            plot[0].set_data(XA[-1], YA[-1])
            plot[1].set_data(XB[-1], YB[-1])
            plot[2].set_data(XC[-1], YC[-1])
            plot[3].set_data(Xagent[-1], Yagent[-1])

    animation = anim.FuncAnimation(fig, update, frames = nbTour//animation_freq +1 , interval = animation_speed*1000, repeat = False)

    #Saving animation
    f = r"animation.gif"
    writergif = anim.PillowWriter(fps=int(1/animation_speed))
    animation.save(f, writer=writergif)

plt.show()
