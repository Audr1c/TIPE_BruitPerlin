import time

import numpy

from numpy.random import rand
from matplotlib.colors import ListedColormap

import imageio
from tqdm import trange

from perlin2DEliott import *
from perlin1DEliott import *

from nbtschematic import SchematicFile


## Fonctions prédéfinies
def sauvegarder_grille(grille: list, g, i, nom_de_fichier: str) -> None:
    echelle = ListedColormap(
        ['white', 'gray', 'green', 'brown', 'blue', 'yellow', 'black', 'red', 'aqua', 'gold', '0.3', '0.8', 'beige'],
        12)
    plt.matshow(grille, cmap=echelle, vmin=0, vmax=12)
    plt.title(f"x={i} g={g}")  # 'x=' + str(i) + ' g=' + str(g)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_de_fichier)


## Eléments suplémentaire sur la carte

def diamant(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x + i][z + k][y + j] == 1 and random.random() < 0.4:
                    C[x + i][z + k][y + j] = 8


def charbon(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x + i][z + k][y + j] == 1 and random.random() < 0.6:
                    C[x + i][z + k][y + j] = 6


def redstone(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x + i][z + k][y + j] == 1 and random.random() < 0.6:
                    C[x + i][z + k][y + j] = 7


def iron(C, x, z, y):
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x + i][z + k][y + j] == 1 and random.random() < 0.6:
                    C[x + i][z + k][y + j] = 12


def gold(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x + i][z + k][y + j] == 1 and random.random() < 0.5:
                    C[x + i][z + k][y + j] = 9


def explose(C, x, z, y):  # fait disparaitre les blocs autour du bloc de coordonnées

    # regarde si le bloc n'est pas trop près des bords

    if z < 1 or z > hauteur - 2 or y < 1 or y > Taille - 2 or x < 1 or x > Taille - 2:

        return None

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


def troue(C, sable):
    tot = len(sable)
    ex_sable = []
    for e in sable:
        x, y, z = e
        if C[x][z][y] == 0:
            ex_sable.append(e)
    return ex_sable


stonks = []


def percolation(C, ex_sable, Heau):
    for (x, y, z) in ex_sable:
        C[x][z][y] = 4
    while len(ex_sable) != 0:
        e = ex_sable[0]
        stonks.append(len(ex_sable))
        x, y, z = e

        if z != hauteur - 1 and C[x][z + 1][y] == 0:
            ex_sable.append((x, y, z + 1))
            C[x][z + 1][y] = 4
        if x != 0 and C[x - 1][z][y] == 0:
            ex_sable.append((x - 1, y, z))
            C[x - 1][z][y] = 4
        if x != Taille - 1 and C[x + 1][z][y] == 0:
            ex_sable.append((x + 1, y, z))
            C[x + 1][z][y] = 4
        if y != 0 and C[x][z][y - 1] == 0:
            ex_sable.append((x, y - 1, z))
            C[x][z][y - 1] = 4
        if y != Taille - 1 and C[x][z][y + 1] == 0:
            ex_sable.append((x, y + 1, z))
            C[x][z][y + 1] = 4
        if z - 1 >= hauteur // 3 and C[x][z - 1][y] == 0 and z > Heau:
            ex_sable.append((x, y, z - 1))
            C[x][z - 1][y] = 4
        ex_sable.pop(0)
        print(f"\r percolation taille pile {len(ex_sable)}", end="")
    # plt.plot([i for i in range(len(stonks))],stonks)
    # plt.show()


#


def Patron_carte(BruitP2D, autre):
    eau = []
    sable = []
    print("Creation tableaux vide")
    CarteListe3D = [[[1 for y in range(Taille)] for z in range(hauteur)] for x in trange(Taille)]
    print("fin creation tablaux")

    for x in trange(Taille):
        for y in range(Taille):
            Hsurface = int(BruitP2D[x, y])
            z = 0
            while z < Hsurface:
                CarteListe3D[x][z][y] = 0
                if z >= Heau:
                    eau.append((x, y, z))
                z += 1
            if z < Hneige:
                CarteListe3D[x][z][y] = 11
            elif z < Heau - 4:
                CarteListe3D[x][z][y] = 2
            else:
                CarteListe3D[x][z][y] = 5
                if z >= Heau:
                    sable.append((x, y, z))
            z += 1
            a = 3
            for i in range(a):
                if z + i >= Heau - 4:
                    CarteListe3D[x][z + i][y] = 5
                else:
                    CarteListe3D[x][z + i][y] = 3
            if random.random() < 1 / 3:
                CarteListe3D[x][hauteur - 3][y] = 10
            if random.random() < 1 / 2:
                CarteListe3D[x][hauteur - 2][y] = 10
            CarteListe3D[x][hauteur - 1][y] = 10

    return CarteListe3D, sable, eau, Heau


def minerais(CarteListe3D, ax):
    h = ((Taille ** 2) / 2500)

    # charbon
    k = int(15 * h)
    _, Yc = liste_aleatoire(k, Taille - 4, k)
    _, Xc = liste_aleatoire(k, Taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 4, k)
    Zc = [i + hauteur // 2 for i in Z]
    for i in range(k):
        charbon(CarteListe3D, int(Xc[i]), int(Zc[i]), int(Yc[i]))

    # redstone
    k = int(11 * h)
    _, Yr = liste_aleatoire(k, Taille - 4, k)
    _, Xr = liste_aleatoire(k, Taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 4 - 4, k)
    Zr = [i + 3 * (hauteur // 4) for i in Z]
    for i in range(k):
        redstone(CarteListe3D, int(Xr[i]), int(Zr[i]), int(Yr[i]))

    # fer
    k = int(11 * h)
    _, Yi = liste_aleatoire(k, Taille - 3, k)
    _, Xi = liste_aleatoire(k, Taille - 3, k)
    _, Z = liste_aleatoire(k, hauteur // 3 - 3, k)
    Zi = [i + 2 * (hauteur // 3) for i in Z]
    for i in range(k):
        iron(CarteListe3D, int(Xi[i]), int(Zi[i]), int(Yi[i]))

    # or
    k = int(8 * h)
    _, Yo = liste_aleatoire(k, Taille - 2, k)
    _, Xo = liste_aleatoire(k, Taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 2, k)
    Zo = [i + hauteur // 2 for i in Z]
    for i in range(k):
        gold(CarteListe3D, int(Xo[i]), int(Zo[i]), int(Yo[i]))

    # diamant
    k = int(5 * h)
    _, Yd = liste_aleatoire(k, Taille - 2, k)
    _, Xd = liste_aleatoire(k, Taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 5 - 2, k)
    Zd = [i + 4 * (hauteur // 5) for i in Z]
    for i in range(k):
        diamant(CarteListe3D, int(Xd[i]), int(Zd[i]), int(Yd[i]))

    ax.scatter(Xr, Yr, Zr, c='red', s=0.7)
    ax.scatter(Xi, Yi, Zi, c='beige', s=0.7)
    ax.scatter(Xo, Yo, Zo, c='gold', s=0.7)
    ax.scatter(Xc, Yc, Zc, c='black', s=0.7)
    ax.scatter(Xd, Yd, Zd, c='aqua', s=0.7)


def grotte(CarteListe3D, ax):
    alpha = 200
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
        explose(CarteListe3D, int(Xg[i]), int(Zg[i]), int(Yg[i]))


def ajout_detail(graine, CarteListe3D, BruitP2D, sable, eau, Heau):
    plt.close("all")
    ax = plt.axes(projection="3d")

    minerais(CarteListe3D, ax)

    # grotte 1
    for _ in trange(nbGrotte):
        grotte(CarteListe3D, ax)

    # eau
    for e in eau:
        x, y, z = e
        CarteListe3D[x][z][y] = 4
    ex_sable = troue(CarteListe3D, sable)
    percolation(CarteListe3D, ex_sable, Heau)

    # frames
    for i in trange(Taille):
        sauvegarder_grille(CarteListe3D[i], graine, i, f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        plt.close()

    # grotte 3D

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Grotte seed=' + str(graine))
    plt.savefig("Affichage_de_la_map/Grotte")

    return CarteListe3D


def gif():
    frames = []
    for i in trange(Taille):
        image = imageio.v2.imread(f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        frames.append(image)
    imageio.mimsave(f"Affichage_de_la_map/GIF.gif", frames, duration=7)


correspondanceID = {0: 0,  # white = Air
                    1: 1,  # gray = Stone
                    2: 2,  # green = Grass
                    3: 3,  # brown = Dirt
                    4: 9,  # blue = Water
                    5: 12,  # yellow = Sand
                    6: 16,  # black = Coal
                    7: 73,  # red = Redstone
                    8: 56,  # aqua = Diamond
                    9: 14,  # gold = Gold
                    10: 7,  # noir = Bedrock
                    11: 80,  # = neige
                    }


def creteMapSchem(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))  # z = hauteur faux mais pas grave
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                sf.blocks[z, y, x] = correspondanceID[grid[x][-z - 1][y]]  # carte renversé
    print("Exporting in :", f'OutSchem/Carte{graine}.schematic ...')
    sf.save(f'OutSchem/Carte{graine}.schematic')
    print("Done.")


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
    N, sable, eau, Heau = Patron_carte(M, autre)
    print(f"End Patron TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Detail")
    finished = ajout_detail(graine, N, M, sable, eau, Heau)
    print(f"End Detail TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Gif")
    gif()
    print(f"End Gif TimeToFinish: {time.time() - start:.2f} s")

    start = time.time()
    print("Start Schematic")
    creteMapSchem(finished, Taille, Taille, hauteur, graine)
    print(f"End Schematic TimeToFinish: {time.time() - start:.2f} s")

    finTime = time.time() - startAll
    plt.show()
    print(f"Program Finished in {finTime:.2f} s")


##
## Modélisation de la carte
Hneige = 80
Heau = 150
nbGrotte = 8
Taille = 200
hauteur = 256
graine = randrange(10000)
fait_une_map(graine)

# prendre un bruit de perlin en basse resolution et faire **5
# ajouter un bruit de perlin tres leger max 3 bloc entre min et max
