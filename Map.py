## Importations

import time
import numpy
from numpy.random import rand
from matplotlib.colors import ListedColormap
import imageio
from tqdm import trange
from perlin2DEliott import *
from perlin1DEliott import *
from nbtschematic import SchematicFile

## Carte

def Patron_carte(BruitP2D):
    eau = []
    sable = []
    CarteListe3D = [[[1 for y in range(Taille)] for z in range(hauteur)] for x in trange(Taille)]

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

    return CarteListe3D, sable, eau

## Images

def sauvegarder_grille(grille: list, g, i, nom_de_fichier: str) -> None:
    echelle = ListedColormap(['white', 'gray', 'green', 'brown', 'blue', 'yellow', 'black', 'red', 'aqua', 'gold', '0.3', '0.8','beige'], 12)
    plt.matshow(grille, cmap=echelle, vmin=0, vmax=12)
    plt.title(f"x={i} g={g}")  # 'x=' + str(i) + ' g=' + str(g)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_de_fichier)

def frames(CarteListe3D):
    for i in trange(Taille):
        sauvegarder_grille(CarteListe3D[i], graine, i, f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        plt.close()

def gif():
    frames = []
    for i in trange(Taille):
        image = imageio.v2.imread(f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        frames.append(image)
    imageio.mimsave(f"Affichage_de_la_map/GIF.gif", frames, duration=7)

## Minerais

def diamant(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x+i][z+k][y+j]==1 and random.random()<0.4:
                    C[x+i][z+k][y+j] = 8

def charbon(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 6

def redstone(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 7

def iron(C, x, z, y):
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 12

def gold(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x+i][z+k][y+j]==1 and random.random()<0.5:
                    C[x+i][z+k][y+j] = 9

def minerais(CarteListe3D, ax):
    h = ((Taille**2)/2500)

    # charbon
    print("charbon")
    k = int(15*h)
    _, Yc = liste_aleatoire(k, Taille - 4, k)
    _, Xc = liste_aleatoire(k, Taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 4, k)
    Zc = [i + hauteur // 2 for i in Z]
    for i in trange(k):
        charbon(CarteListe3D, int(Xc[i]), int(Zc[i]), int(Yc[i]))

    # redstone
    print("redstone")
    k = int(11*h)
    _, Yr = liste_aleatoire(k, Taille - 4, k)
    _, Xr = liste_aleatoire(k, Taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 4 - 4, k)
    Zr = [i + 3*(hauteur // 4) for i in Z]
    for i in trange(k):
        redstone(CarteListe3D, int(Xr[i]), int(Zr[i]), int(Yr[i]))

    # fer
    print("fer")
    k = int(11*h)
    _, Yi = liste_aleatoire(k, Taille - 3, k)
    _, Xi = liste_aleatoire(k, Taille - 3, k)
    _, Z = liste_aleatoire(k, hauteur // 3 - 3, k)
    Zi = [i + 2*(hauteur // 3) for i in Z]
    for i in trange(k):
        iron(CarteListe3D, int(Xi[i]), int(Zi[i]), int(Yi[i]))

    # or
    print("or")
    k = int(8*h)
    _, Yo = liste_aleatoire(k, Taille - 2, k)
    _, Xo = liste_aleatoire(k, Taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 2, k)
    Zo = [i + hauteur // 2 for i in Z]
    for i in trange(k):
        gold(CarteListe3D, int(Xo[i]), int(Zo[i]), int(Yo[i]))

    # diamant
    print("diamant")
    k = int(5*h)
    _, Yd = liste_aleatoire(k, Taille - 2, k)
    _, Xd = liste_aleatoire(k, Taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 5 - 2, k)
    Zd = [i + 4 * (hauteur // 5) for i in Z]
    for i in trange(k):
        diamant(CarteListe3D, int(Xd[i]), int(Zd[i]), int(Yd[i]))

    ax.scatter(Xr, Yr, Zr, c='red', s=0.7)
    ax.scatter(Xi, Yi, Zi, c='beige', s=0.7)
    ax.scatter(Xo, Yo, Zo, c='gold', s=0.7)
    ax.scatter(Xc, Yc, Zc, c='black', s=0.7)
    ax.scatter(Xd, Yd, Zd, c='aqua', s=0.7)

## Grottes

def explose(C, x, z, y):

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

def grotte(CarteListe3D, ax):
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

    ax.scatter(Xg, Yg, Zg, s=.8)

    for i in range((u - 1) * alpha + 1):
        explose(CarteListe3D, int(Xg[i]), int(Zg[i]), int(Yg[i]))

def grotte_3D(ax):

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Grotte seed=' + str(graine))
    plt.savefig("Affichage_de_la_map/Grotte")

## Eau

def Eau(CarteListe3D, eau):
    for e in eau:
            x, y, z = e
            CarteListe3D[x][z][y] = 4

def troue(C, sable):
    tot = len(sable)
    ex_sable = []
    for e in sable:
        x, y, z = e
        if C[x][z][y] == 0:
            ex_sable.append(e)
    return ex_sable

def percolation(C, ex_sable):
    for (x, y, z) in ex_sable:
        C[x][z][y] = 4
    while len(ex_sable) != 0:
        e = ex_sable[0]
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

## Conversion pour Minecraft

correspondanceID = {0 : 0,  # white = Air
                    1 : 1,  # gray = Stone
                    2 : 2,  # green = Grass
                    3 : 3,  # brown = Dirt
                    4 : 9,  # blue = Water
                    5 : 12,  # yellow = Sand
                    6 : 16,  # black = Coal
                    7 : 73,  # red = Redstone
                    8 : 56,  # aqua = Diamond
                    9 : 14,  # gold = Gold
                    10: 7,  # noir = Bedrock
                    11: 80,  # = neige
                    12: 15,
                    }

def creteMapSchem(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))  # z = hauteur faux mais pas grave
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                sf.blocks[z, y, x] = correspondanceID[grid[x][-z - 1][y]]  # carte renversé
    sf.save(f'OutSchem/Carte{graine}.schematic')

## Fonction final

def fait_une_map(graine):
    
    # Timer et parametrage du random
    startAll = time.time()
    random.seed(graine)
    np.random.seed(graine)
    print('')

    print(f"Graine: {graine}")
    print('')

    # Bruit
    start = time.time()
    print("Start Bruit Perlin")
    M  = Bruit_de_map(graine, Taille, hauteur)
    print(f"End Bruit Perlin TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Patron
    start = time.time()
    print("Start Patron")
    Map, sable, eau = Patron_carte(M)
    print(f"End Patron TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Minerai
    start = time.time()
    print("Start Minerai")
    plt.close("all")
    ax = plt.axes(projection="3d")
    minerais(Map, ax)
    print(f"End Minerai TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Grotte
    start = time.time()
    print("Start Grotte")
    for _ in trange(nbGrotte):
        grotte(Map, ax)
    grotte_3D(ax)
    print(f"End Grotte TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Eau
    start = time.time()
    print("Start Eau")
    Eau(Map, eau)
    ex_sable = troue(Map, sable)
    percolation(Map, ex_sable)
    print(f"End Eau TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Frame
    start = time.time()
    print("Start Frame")
    frames(Map)
    print(f"End Frame TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # GIF
    start = time.time()
    print("Start Gif")
    gif()
    print(f"End Gif TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Schematic
    start = time.time()
    print("Start Schematic")
    creteMapSchem(Map, Taille, Taille, hauteur, graine)
    print(f"End Schematic TimeToFinish: {time.time() - start:.2f} s")
    print('')

    finTime = time.time() - startAll
    print(f"Program Finished in {finTime:.2f} s")
    print('')

## Paramètres de la carte

alpha = 400
Hneige = 60
Heau = 150
nbGrotte = 10
Taille = 500
hauteur = 256
graine = randrange(10000)

## Création de la carte

fait_une_map(graine)
