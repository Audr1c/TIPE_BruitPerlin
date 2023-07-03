## Importation


import os
import time
from random import randrange
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange
from matplotlib.colors import ListedColormap
import imageio
from nbtschematic import SchematicFile
from Grotte import *


## Fonction utile


def in_Nether(x, y, z):
    return 0 <= x < taille and 0 <= y < taille and 0 <= z < hauteur


def Gif_et_frame(Nether):
    frames = []
    for Num_Bruit in trange(taille):
        echelle = ListedColormap(['red', 'white'])
        plt.close("all")
        plt.imshow(Nether[Num_Bruit].T, origin='upper',
                   cmap=echelle)
        plt.xlabel('Y')
        plt.ylabel('Z')
        plt.colorbar()
        plt.title(f'Bruit de Perlin en 3D (Tranche n°{Num_Bruit})')
        plt.savefig(f"Nether_et_BdP_3D/Tranche/Bruit_{Num_Bruit}.jpg")
        file_name = f"Nether_et_BdP_3D/Tranche/Bruit_{Num_Bruit}.jpg"

        if os.path.exists(file_name):
            image_bruit = imageio.v2.imread(file_name)
            os.remove(file_name)
        else:
            raise Exception(f"File Not found {file_name}")
        frames.append(image_bruit)
    imageio.mimsave(f"Nether_et_BdP_3D/Bruit_3D.gif", frames, duration=100)


def lerp(a, b, x):
    # interpolation linéaire (produit scalaire)
    return a + x * (b - a)


def lissage(f):
    # Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3


def gradient3D(c, x, y, z):
    # Récupère les coords des vecteurs de gradient
    vecteurs = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1],
                        [-1, 0, -1], [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [-1, 1, 0], [0, -1, 1], [0, -1, -1]])
    co_gradient = vecteurs[c % 16]
    return co_gradient[:, :, :, 0] * x + co_gradient[:, :, :, 1] * y + co_gradient[:, :, :, 2] * z


## Bruit 3D


def Perlin3D(precsision):
    tab = np.linspace(1, precsision, taille, endpoint=False)
    tab1 = np.linspace(1, precsision, hauteur, endpoint=False)
    # création de grille en utilisant le tableau 1d
    x, y, z = np.meshgrid(tab, tab, tab1)

    # On crée une permutation en fonction du nb de taille
    # On utilise la fonction seed parce que numpy chiale si on le fait pas

    perm = np.arange(16 * (precsision // 3), dtype=int)
    np.random.shuffle(perm)

    # on fait un tableau 2d qu'on applatit
    # pour faire des produits scalaires correctement
    # (les tableaux numpy sont chiants)
    perm = np.stack([perm, perm, perm]).flatten()
    # Coordonnées de la grille
    xi, yi, zi = x.astype(int), y.astype(int), z.astype(int)

    # normes des vecteurs
    xg, yg, zg = x - xi, y - yi, z - zi
    # on lisse les normes (algo 2d perlin tu coco)
    xf, yf, zf = lissage(xg), lissage(yg), lissage(zg)

    # C'est le moment où on chiale
    # On chope les coords vecteur dans les 4 coins de la grille
    # (haut gauche/droite, bas gauche/droite)

    g000 = gradient3D(perm[perm[perm[xi] + yi] + zi], xg, yg, zg)
    g001 = gradient3D(perm[perm[perm[xi] + yi] + zi+1], xg, yg, zg-1)
    g010 = gradient3D(perm[perm[perm[xi] + yi+1] + zi], xg, yg-1, zg)
    g011 = gradient3D(perm[perm[perm[xi] + yi+1] + zi+1], xg, yg-1, zg-1)
    g100 = gradient3D(perm[perm[perm[xi+1] + yi] + zi], xg-1, yg, zg)
    g101 = gradient3D(perm[perm[perm[xi+1] + yi] + zi+1], xg-1, yg, zg-1)
    g110 = gradient3D(perm[perm[perm[xi+1] + yi+1] + zi], xg-1, yg-1, zg)
    g111 = gradient3D(perm[perm[perm[xi+1] + yi+1] + zi+1], xg-1, yg-1, zg-1)
    # On interpole linéairement pour faire une moyenne
    # C'est ce qui fait que la transition de couleurs des taille est clean
    x00 = lerp(g000, g100, xf)
    x10 = lerp(g010, g110, xf)
    x01 = lerp(g001, g101, xf)
    x11 = lerp(g011, g111, xf)

    xy0 = lerp(x00, x10, yf)
    xy1 = lerp(x01, x11, yf)

    resultat = lerp(xy0, xy1, zf)
    return resultat


def Bruit_Nether(precsision, amplitude):
    resultat = []
    for _ in trange(1, 6):
        temporaire = Perlin3D(precsision)

        temporaire *= amplitude

        resultat.append(temporaire)
        precsision *= 2
        amplitude //= 2
    resultat = sum(resultat)
    return resultat


## Minerai


def quartz(Nether, x, z, y):
    Xc1 = []
    Yc1 = []
    Zc1 = []
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if Nether[x+i, y+k, z+j] == -1 and random.random() < 0.6:
                    Nether[x+i, y+k, z+j] = 6
                    Xc1.append(x)
                    Yc1.append(y)
                    Zc1.append(z)
    return Xc1, Yc1, Zc1


def minerais(Nether, ax):
    NdC = ((taille**2)//(Chunks**2))
    print("quartz")
    NbMn = 17*NdC
    _, Yq = Perlin_1D(NbMn)
    _, Xq = Perlin_1D(NbMn)
    _, Zq = Perlin_1D(NbMn)
    Zq *= hauteur-4
    Yq *= taille
    Yq -= 4
    Xq *= taille
    Xq -= 4

    X = []
    Y = []
    Z = []
    for i in trange(NbMn):
        x, y, z = quartz(Nether, int(Xq[i]), int(Zq[i]), int(Yq[i]))
        X += x
        Y += y
        Z += z
    Xq = X
    Yq = Y
    Zq = Z

    ax.scatter(Xq, Yq, Zq, c='red', s=0.7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Quartz 3D')
    plt.savefig("Nether_et_BdP_3D/Quartz")
    plt.close()


## Grottes et murs


def Explose(Nether, x, z, y):
    for j in range(-2, 3):
        for k in range(-2, 3):
            for i in range(-2, 3):
                if in_Nether(x+i, y+k, z+j) and not (i, j) == (2, 2) and not (i, k) == (2, 2) and not (j, k) == (2, 2):
                    Nether[x+i, y+k, z+j] = 0


def Grotte(Nether, ax):

    _, Xg = Bruit_de_Grotte_sin(NbPt, fr, 2*amplitude_G, NdBG)
    _, Zg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    _, Yg = Bruit_de_Grotte_sin(NbPt, fr, 2*amplitude_G, NdBG)
    Xg += randrange(taille-2*amplitude_G)
    Yg += randrange(taille-2*amplitude_G)

    ax.scatter(Xg, Yg, Zg, s=.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_title('Grotte 3D')
    plt.savefig("Nether_et_BdP_3D/Grotte")

    for i in range((NbPt - 1) * fr + 1):
        Explose(Nether, int(Xg[i]), int(Zg[i]+150), int(Yg[i]))


def Mur(Nether):
    for x in trange(taille):
        for y in range(taille):
            Nether[x, y, 0] = -1
            Nether[x, y, hauteur-1] = -1
    for x in trange(taille):
        for z in range(hauteur):
            Nether[x, 0, z] = -1
            Nether[x, taille-1, z] = -1
            Nether[0, x, z] = -1
            Nether[taille-1, x, z] = -1


## Lave


def Lava(Nether):
    for x in trange(taille):
        for y in range(taille):
            for z in range(Hlave):
                if Nether[x, y, z] == 0:
                    Nether[x, y, z] = 3


## Convertion Minecraft


correspondanceID = {
    0: 0,  # Air
    -1: 87,  # Stone
    3: 11,  # Lava
    6: 153  # Quartz
}


def CreteMapSchem3D(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                # carte renversé
                sf.blocks[z, y, x] = correspondanceID[grid[x][y][z]]
    sf.save(f'Nether_et_BdP_3D/Map_Nether.schematic')

## Fonction finale


def Make_a_Nether(g):
    print('')
    print('Start Nether')

    # Timer et parametrage du random
    startAll = time.time()
    np.random.seed(g)
    print('')

    print(f"Graine: {g}")
    print('')

    # Bruit et Patron
    start = time.time()
    print("Start Bruit de Perlin et Patron")
    Nether = Bruit_Nether(3, 32)
    print(f"End Bruit de Perlin : {time.time() - start:.2f} s")
    print('')

    # Frames et GIF
    start = time.time()
    print("Start Frame et GIF")
    Nether //= 256
    Gif_et_frame(Nether)
    print(f"End Frame et GIF : {time.time() - start:.2f} s")
    print('')

    # Minerai
    start = time.time()
    print("Start Minerai")
    plt.close("all")
    ax = plt.axes(projection="3d")
    minerais(Nether, ax)
    print(f"End Minerai : {time.time() - start:.2f} s")
    print('')

    # Grotte
    start = time.time()
    print("Start Grotte")
    ax = plt.axes(projection="3d")
    for _ in range(nbGrotte):
        Grotte(Nether, ax)
    print(f"End Grotte : {time.time() - start:.2f} s")
    print('')

    # Lave
    start = time.time()
    print("Start Lave")
    Lava(Nether)
    print(f"End Lave : {time.time() - start:.2f} s")
    print('')

    # Mur
    start = time.time()
    print("Start Mur")
    Mur(Nether)
    print(f"End Mur : {time.time() - start:.2f} s")
    print('')

    # Schematic
    start = time.time()
    print("Start Schematic")
    CreteMapSchem3D(Nether, taille, taille, hauteur, g)
    print(f"End Schematic : {time.time() - start:.2f} s")
    print('')

    finTime = time.time() - startAll
    print(f"End Nether : {finTime:.2f} s")
    print('')


## Paramètres


# Dimensions et seed
Hlave = 30
taille = 400
hauteur = 128
Chunks = 16
g = randrange(10000)
# Grotte
NbPt = 4
fr = 128
amplitude_G = 64
NdBG = 6
nbGrotte = 10


## Création du Nether


Make_a_Nether(g)
