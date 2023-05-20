import time

import numpy
import numpy as np
import matplotlib.pyplot as plt
import random
from random import randrange
from numpy.random import rand
from matplotlib.colors import ListedColormap
from mpl_toolkits import mplot3d
import imageio
from tqdm import trange

from perlin2DEliott import *
from perlin1DEliott import *


## Fonctions prédéfinies
def sauvegarder_grille(grille: list, g, i, nom_de_fichier: str) -> None:
    echelle = ListedColormap(['white', 'gray', 'green', 'brown', 'blue', 'yellow', 'black', 'red', 'aqua', 'gold'], 9)
    plt.matshow(grille, cmap=echelle, vmin=0, vmax=9)
    plt.title('x=' + str(i) + ' g=' + str(g))
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_de_fichier)


def afficher_grille(grille: list) -> None:
    echelle = ListedColormap(['white', 'gray', 'green', 'brown', 'blue', 'yellow', 'black'], 6)
    plt.matshow(grille, cmap=echelle)  # vmin=0,vmax=6
    plt.colorbar()
    plt.title('e=' + str(i))
    plt.show()
    return None


## Eléments suplémentaire sur la carte

def diamant(C, x, z, y):
    C[x][z][y] = 8
    if random_int() % 2 == 0:
        C[x + 1][z][y] = 8
    if random_int() % 2 == 1:
        C[x + 1][z + 1][y] = 8
    if random_int() % 2 == 1:
        C[x + 1][z][y + 1] = 8
    if random_int() == 0:
        C[x + 1][z + 1][y + 1] = 8
    if random_int() == 0:
        C[x][z + 1][y] = 8
    if random_int() % 2 == 1:
        C[x][z][y + 1] = 8
    if random_int() == 0:
        C[x][z + 1][y + 1] = 8


def charbon(C, B, x, z, y):
    if z > B[x][y]:
        C[x][z][y] = 6
        C[x + 1][z][y] = 6
        C[x - 1][z][y] = 6
        C[x][z + 1][y] = 6
        C[x][z - 1][y] = 6
        C[x][z][y + 1] = 6
        C[x][z][y - 1] = 6


def gold(C, x, z, y):
    C[x][z][y] = 9
    C[x + 1][z][y] = 9
    if random_int() % 2 == 1:
        C[x + 1][z + 1][y] = 9
    if random_int() % 2 == 1:
        C[x + 1][z][y + 1] = 9
    if random_int() % 2 == 0:
        C[x + 1][z + 1][y + 1] = 9
    if random_int() == 0:
        C[x][z + 1][y] = 9
    if random_int() % 2 == 1:
        C[x][z][y + 1] = 9
    if random_int() == 0:
        C[x][z + 1][y + 1] = 9


def explose(C, x, z, y):  # fait disparaitre les blocs autour du bloc de coordonnées

    # regarde si le bloc n'est pas trop près des bords

    if z < 1 or z > hauteur - 2 or y < 1 or y > Taille - 2 or x < 1 or x > Taille - 2:

        return C

    # fait l'explosion

    else:  # explose un cube de 3*3 autour du cube

        C[x][z][y] = 0
        C[x][z + 1][y] = 0
        C[x][z - 1][y] = 0
        C[x][z + 1][y + 1] = 0
        C[x][z][y + 1] = 0
        C[x][z - 1][y + 1] = 0
        C[x][z + 1][y - 1] = 0
        C[x][z][y - 1] = 0
        C[x][z - 1][y - 1] = 0

        C[x + 1][z][y] = 0
        C[x + 1][z + 1][y] = 0
        C[x + 1][z - 1][y] = 0
        C[x + 1][z + 1][y + 1] = 0
        C[x + 1][z][y + 1] = 0
        C[x + 1][z - 1][y + 1] = 0
        C[x + 1][z + 1][y - 1] = 0
        C[x + 1][z][y - 1] = 0
        C[x + 1][z - 1][y - 1] = 0

        C[x - 1][z][y] = 0
        C[x - 1][z + 1][y] = 0
        C[x - 1][z - 1][y] = 0
        C[x - 1][z + 1][y + 1] = 0
        C[x - 1][z][y + 1] = 0
        C[x - 1][z - 1][y + 1] = 0
        C[x - 1][z + 1][y - 1] = 0
        C[x - 1][z][y - 1] = 0
        C[x - 1][z - 1][y - 1] = 0

        if z != 1 and z != hauteur - 2 and y != 1 and y != Taille - 2 and x != 1 and x != Taille - 2:  # explose un bloc de 5*5 sans les arretes si le bloc n'est pas trop près des bords

            C[x + 2][z][y] = 0
            C[x + 2][z + 1][y] = 0
            C[x + 2][z - 1][y] = 0
            C[x + 2][z + 1][y + 1] = 0
            C[x + 2][z][y + 1] = 0
            C[x + 2][z - 1][y + 1] = 0
            C[x + 2][z + 1][y - 1] = 0
            C[x + 2][z][y - 1] = 0
            C[x + 2][z - 1][y - 1] = 0

            C[x - 2][z][y] = 0
            C[x - 2][z + 1][y] = 0
            C[x - 2][z - 1][y] = 0
            C[x - 2][z + 1][y + 1] = 0
            C[x - 2][z][y + 1] = 0
            C[x - 2][z - 1][y + 1] = 0
            C[x - 2][z + 1][y - 1] = 0
            C[x - 2][z][y - 1] = 0
            C[x - 2][z - 1][y - 1] = 0

            C[x + 1][z + 2][y + 1] = 0
            C[x - 1][z + 2][y + 1] = 0
            C[x][z + 2][y + 1] = 0
            C[x + 1][z + 2][y] = 0
            C[x - 1][z + 2][y] = 0
            C[x][z + 2][y] = 0
            C[x + 1][z + 2][y - 1] = 0
            C[x - 1][z + 2][y - 1] = 0
            C[x][z + 2][y - 1] = 0

            C[x + 1][z - 2][y + 1] = 0
            C[x - 1][z - 2][y + 1] = 0
            C[x][z - 2][y + 1] = 0
            C[x + 1][z - 2][y] = 0
            C[x - 1][z - 2][y] = 0
            C[x][z - 2][y] = 0
            C[x + 1][z - 2][y - 1] = 0
            C[x - 1][z - 2][y - 1] = 0
            C[x][z - 2][y - 1] = 0

            C[x + 1][z + 1][y + 2] = 0
            C[x - 1][z + 1][y + 2] = 0
            C[x][z + 1][y + 2] = 0
            C[x + 1][z][y + 2] = 0
            C[x - 1][z][y + 2] = 0
            C[x][z][y + 2] = 0
            C[x + 1][z - 1][y + 2] = 0
            C[x - 1][z - 1][y + 2] = 0
            C[x][z - 1][y + 2] = 0

            C[x + 1][z + 1][y - 2] = 0
            C[x - 1][z + 1][y - 2] = 0
            C[x][z + 1][y - 2] = 0
            C[x + 1][z][y - 2] = 0
            C[x - 1][z][y - 2] = 0
            C[x][z][y - 2] = 0
            C[x + 1][z - 1][y - 2] = 0
            C[x - 1][z - 1][y - 2] = 0
            C[x][z - 1][y - 2] = 0

        return C


def troue(C, sable):
    tot = len(sable)
    ex_sable = []
    for e in sable:
        x, y, z = e
        if C[x][z][y] == 0:
            ex_sable.append(e)
    return ex_sable


stonks = []


def percolation(C, ex_sable):
    while len(ex_sable) != 0:
        e = ex_sable[0]
        stonks.append(len(ex_sable))
        x, y, z = e
        C[x][z][y] = 4

        if z != hauteur - 1 and C[x][z + 1][y] == 0 and not (x, y, z + 1) in ex_sable:
            ex_sable.append((x, y, z + 1))
        if x != 0 and C[x - 1][z][y] == 0 and not (x - 1, y, z) in ex_sable:
            ex_sable.append((x - 1, y, z))
        if x != Taille - 1 and C[x + 1][z][y] == 0 and not (x + 1, y, z) in ex_sable:
            ex_sable.append((x + 1, y, z))
        if y != 0 and C[x][z][y - 1] == 0 and not (x, y - 1, z) in ex_sable:
            ex_sable.append((x, y - 1, z))
        if y != Taille - 1 and C[x][z][y + 1] == 0 and not (x, y + 1, z) in ex_sable:
            ex_sable.append((x, y + 1, z))
        ex_sable.pop(0)
        if z - 1 >= hauteur // 3 and C[x][z - 1][y] == 0 and not (x, y, z - 1) in ex_sable:
            ex_sable.append((x, y, z - 1))

    # plt.plot([i for i in range(len(stonks))],stonks)
    # plt.show()


#


def Patron_carte(BruitP2D, autre):
    eau = []
    sable = []
<<<<<<< Updated upstream
    CarteListe3D = [[[1 for y in range(Taille)] for z in range(hauteur)] for x in range(Taille)]
    Heau = 130
=======
    print("Creation Tablaux vide")
    CarteListe3D = [[[1 for y in range(Taille)] for z in range(hauteur)] for x in trange(Taille)]
    print("Fin creation Tablaux vide")
    Heau = 110
>>>>>>> Stashed changes
    for x in trange(Taille):
        for y in range(Taille):
            Hsurface = int(BruitP2D[x, y])
            if Hsurface >= Heau:
                z = 0
                while z < Hsurface:
                    if z < Heau:
                        CarteListe3D[x][z][y] = 0
                    else:
                        eau.append((x, y, z))
                    z += 1
                sable.append((x, y, z))
                a = 7 - int(autre[x, y])
                for i in range(a):
                    CarteListe3D[x][z + i][y] = 5
            else:
                z = 0
                while z < Hsurface:
                    CarteListe3D[x][z][y] = 0
                    z += 1
                CarteListe3D[x][z][y] = 2
                z += 1
                a = 7 - int(autre[x, y])
                for i in range(a):
                    if z + i >= Heau:
                        CarteListe3D[x][z + i][y] = 5
                    else:
                        CarteListe3D[x][z + i][y] = 3
            if random.random() < 1 / 3:
                CarteListe3D[x][hauteur - 3][y] = 6
            if random.random() < 1 / 2:
                CarteListe3D[x][hauteur - 2][y] = 6
            CarteListe3D[x][hauteur - 1][y] = 6

    return CarteListe3D, sable, eau


def minerais(CarteListe3D, BruitP2D, ax):
    h = (Taille // 50) ** 2

    # charbon
    k = random_int() + 4
    k *= h
    Ac, Yc = liste_aleatoire(k, Taille - 2, k)
    Ac, Xc = liste_aleatoire(k, Taille - 2, k)
    Ac, Z = liste_aleatoire(k, hauteur // 2 - 1, k)
    Zc = [i + hauteur // 2 for i in Z]
    for i in range(k):
        charbon(CarteListe3D, BruitP2D, int(Xc[i] + 1), int(Zc[i]), int(Yc[i] + 1))

    # or
    k = random_int() + 2
    k *= h
    Ao, Yo = liste_aleatoire(k, Taille - 1, k)
    Ao, Xo = liste_aleatoire(k, Taille - 1, k)
    Ao, Z = liste_aleatoire(k, Taille // 2 - 1, k)
    Zo = [i + 0 for i in Z]
    for i in range(k):
        gold(CarteListe3D, int(Xo[i]), int(Zo[i]), int(Yo[i]))

    # diamant
    k = random_int()
    k *= h
    Ad, Yd = liste_aleatoire(k, Taille - 1, k)
    Ad, Xd = liste_aleatoire(k, Taille - 1, k)
    Ad, Z = liste_aleatoire(k, hauteur // 5 - 1, k)
    Zd = [i + 4 * (hauteur // 5) for i in Z]
    for i in range(k):
        diamant(CarteListe3D, int(Xd[i]), int(Zd[i]), int(Yd[i]))

    ax.scatter(Xo, Yo, Zo, c='gold')
    ax.scatter(Xc, Yc, Zc, c='black')
    ax.scatter(Xd, Yd, Zd, c='aqua')


def grotte(CarteListe3D, ax):
    numy = numpy.array(CarteListe3D)
<<<<<<< Updated upstream
    alpha = 100
=======
    alpha = Taille//10
>>>>>>> Stashed changes
    u = 5
    _, Xg = liste_aleatoire_spline1(Taille, Taille, u, alpha)
    _, Zg = liste_aleatoire_spline1(Taille, hauteur, u, alpha)
    _, Yg = liste_aleatoire_spline1(Taille, Taille, u, alpha)

    '''
    plt.close("all")
    plt.plot(Ag, Zg, 'y', label='Sur Z')
    plt.plot(Ag, Xg, 'r', label='Sur X')
    plt.plot(Ag, Yg, 'b', label='Sur Y')
    plt.title('Grotte (seed = ' + str(graine) + ')')
    plt.legend(loc=0)
    plt.savefig("Affichage_de_la_map/Grotte1_sur_les_axes ")
    plt.close()
    '''

    ax.scatter(Xg, Yg, Zg, linewidths=.2)

    for i in range((u - 1) * alpha + 1):
        explose(CarteListe3D, int(Xg[i]), int(Zg[i]) + Taille // 2, int(Yg[i]))


def ajout_detail(graine, CarteListe3D, BruitP2D, sable, eau):
    plt.close("all")
    ax = plt.axes(projection="3d")

    minerais(CarteListe3D, BruitP2D, ax)

    nbGrotte = 4
    # grotte 1
    for _ in trange(nbGrotte):
        grotte(CarteListe3D, ax)

    # eau
    for e in eau:
        x, y, z = e
        CarteListe3D[x][z][y] = 4
    ex_sable = troue(CarteListe3D, sable)
    percolation(CarteListe3D, ex_sable)

    # frames
    for i in trange(Taille):
        #sauvegarder_grille(CarteListe3D[i], graine, i, f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        plt.close()

    # grotte 3D

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Grotte seed=' + str(graine))
    plt.savefig("Affichage_de_la_map/Grotte")


def gif():
    frames = []
    for i in trange(Taille):
        image = imageio.v2.imread(f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        frames.append(image)
    imageio.mimsave(f"Affichage_de_la_map/GIF.gif", frames, duration=7)


def fait_une_map(graine):
    startAll = time.time()
    random.seed(graine)
    np.random.seed(graine)

    print(f"Graine: {graine}")

    start = time.time()
    print("Start Bruit Perlin")
    M, autre = perlinfzej(graine, Taille, hauteur)

    print(f"End Bruit Perlin TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Patron")
    N, sable, eau = Patron_carte(M, autre)
    print(f"End Patron TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Detail")
    ajout_detail(graine, N, M, sable, eau)
    print(f"End Detail TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Gif")
    #gif()
    print(f"End Gif TimeToFinish: {time.time() - start:.2f} s")

    finTime = time.time() - startAll
    plt.show()
    print(f"Program Finished in {finTime:.2f} s")


##
## Modélisation de la carte
Taille = 500
hauteur = 300
graine = randrange(10000)
fait_une_map(8490)

# prendre un bruit de perlin en basse resolution et faire **5
# ajouter un bruit de perlin tres leger max 3 bloc entre min et max
