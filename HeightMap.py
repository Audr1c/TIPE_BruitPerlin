# Importation


from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from matplotlib.colors import ListedColormap
import imageio


# Fonctions utiles


def lineaire(a, b, x):
    # interpolation linéaire
    return a + x * (b - a)


def lissage(t):
    # Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(c, x, y, nb_vecteur):
    vecteurs = np.array([[sin((k*2*pi)/nb_vecteur), cos((k*2*pi)/nb_vecteur)] for k in range(nb_vecteur)])
    co_gradient = vecteurs[c % nb_vecteur]
    return co_gradient[:, :, 0] * x + co_gradient[:, :, 1] * y


# Bruit de Perlin


def Perlin_2D(precsision, pixels, taille, nb_vecteur):
    new_precsision = 1 + (precsision - 1) * taille / pixels

    perm = np.arange((16 * new_precsision // 5), dtype=int)
    np.random.shuffle(perm)
    perm = np.stack([perm, perm]).flatten()


    tab = np.linspace(1, new_precsision, taille, endpoint=False)
    x, y = np.meshgrid(tab, tab)
    # Coordonnées de la grille
    x_int, y_int = x.astype(int), y.astype(int)
    # normes des vecteurs
    x_dec, y_dec = x - x_int, y - y_int

    # On chope les coords vecteur dans les 4 coins de la grille
    # (haut gauche/droite, bas gauche/droite)

    n00 = gradient(perm[perm[x_int]     + y_int],     x_dec,     y_dec,     nb_vecteur)
    n10 = gradient(perm[perm[x_int + 1] + y_int],     x_dec - 1, y_dec,     nb_vecteur)
    n01 = gradient(perm[perm[x_int]     + y_int + 1], x_dec,     y_dec - 1, nb_vecteur)
    n11 = gradient(perm[perm[x_int + 1] + y_int + 1], x_dec - 1, y_dec - 1, nb_vecteur)
    
    x_lis, y_lis = lissage(x_dec), lissage(y_dec)
    x1 = lineaire(n00, n10, x_lis)
    x2 = lineaire(n01, n11, x_lis)
    
    resultat = lineaire(x1, x2, y_lis)
    return resultat


def Bruit_Overworld(taille, pixels, precsision, amplitude, nb_vecteur):
    frames_bruit = []
    frames_carte = []

    resultats = []
    echelle = ListedColormap(['#141872', '#0970a6', '#119fe9', '#eeec7e',
                             '#5df147', '#38be2a', '#336e1c', '#004704', 'white'], 8)
    orig_map = plt.cm.get_cmap('gray')
    reversed_map = orig_map.reversed()
    for Num_Bruit in trange(1, 9):
        temporaire = Perlin_2D(precsision, pixels, taille, nb_vecteur)
        if Num_Bruit == 1:
            temporaire += 1

        temporaire *= amplitude

        resultats.append(temporaire)

        plt.imshow(temporaire, origin='upper', cmap=reversed_map)
        plt.xlabel('Y')
        plt.ylabel('X')
        plt.colorbar()
        plt.title(f'Bruit de Perlin n°{Num_Bruit}')
        plt.savefig(
            f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")

        Cat = np.array([[0 for i in range(taille)] for j in range(taille)])
        Temp2 = sum(resultats)
        Temp2 = fonction_passage(Temp2, Entre, Sortie)
        for i in range(taille):
            for j in range(taille):
                s = Temp2[i][j]
                if 256 >= s > 180:
                    Cat[i, j] = 0
                elif 180 >= s > 165:
                    Cat[i, j] = 1
                elif 165 >= s > 150:
                    Cat[i, j] = 2
                elif 150 >= s > 147:
                    Cat[i, j] = 3
                elif 147 >= s > 120:
                    Cat[i, j] = 4
                elif 120 >= s > 90:
                    Cat[i, j] = 5
                elif 90 >= s > 60:
                    Cat[i, j] = 6
                elif 60 >= s:
                    Cat[i, j] = 8

        plt.close("all")
        plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=7)
        plt.xlabel('Y')
        plt.ylabel('X')
        plt.title(f'Carte au Trésor avec {Num_Bruit} bruits')
        plt.savefig(f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        image_bruit = imageio.v2.imread(
            f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
        frames_bruit.append(image_bruit)
        image_carte = imageio.v2.imread(
            f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        frames_carte.append(image_carte)

        precsision *= 2
        amplitude //= 2

    imageio.mimsave(f"Overworld/Evolution_Carte.gif",
                    frames_carte, duration=500)
    imageio.mimsave(f"HeightMap_et_BdP_2D/Tout_les_bruits.gif",
                    frames_bruit, duration=500)

    resultat = sum(resultats)
    tab2 = np.linspace(0, taille, taille, endpoint=True)

    # création de grille en utilisant le tableau 1d
    X, Y = np.meshgrid(tab2, tab2)

    plt.imshow(resultat, origin='upper', cmap=reversed_map)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title('Bruit de Perlin en 2D')
    plt.savefig(f"HeightMap_et_BdP_2D/Bruit_2D_map.jpg")

    plt.close("all")
    ax = plt.axes(projection="3d")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    ax.plot_surface(X, Y, resultat.T, cmap=reversed_map)
    plt.title('Heightmap')
    plt.savefig("HeightMap_et_BdP_2D/Height_map")

    return fonction_passage(resultat, Entre, Sortie), Cat


def Bruit_Arbres(pixels, precsision):

    amplitude = 8
    resultats = []
    for _ in range(1, 4):
        temporaire = Perlin_2D(precsision, pixels, pixels, 8)
        temporaire += .5

        temporaire *= amplitude

        resultats.append(temporaire)

        precsision *= 2
        amplitude //= 2

    resultat = sum(resultats)

    return resultat


# Plateau

def miniAfine(x1, x2, y1, y2, x):
    pente = (y2 - y1) / (x2 - x1)
    x -= x1
    y = pente * x
    y += y1
    return y


def fonction_passage(BdP, Entre, Sortie):
    for i in range(1, len(Entre)):
        for x in range(len(BdP)):
            for y in range(len(BdP[x])):
                if Entre[i-1] >= BdP[x, y] > Entre[i]:
                    BdP[x, y] = int(miniAfine(Entre[i-1], Entre[i], Sortie[i-1], Sortie[i], BdP[x, y]))
    plt.close("all")
    ax = plt.axes()
    ax.plot(Entre[1:-1], Sortie[1:-1], 'r')
    ax.invert_yaxis()
    ax.invert_xaxis()
    plt.savefig("HeightMap_et_BdP_2D/Courbe_Plateau")
    return BdP


Entre = [256, 170, 155, 150, 130, 110, 105, 80, 0]
Sortie = [200, 200, 190, 150, 146, 140, 90, 70, 70]