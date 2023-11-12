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


# Affichage


def Plot3DSuraface(table, taille):
    orig_map = plt.cm.get_cmap('gray')
    reversed_map = orig_map.reversed()
    tab2 = np.linspace(0, taille, taille, endpoint=True)

    # création de grille en utilisant le tableau 1d
    X, Y = np.meshgrid(tab2, tab2)

    plt.close("all")
    ax = plt.axes(projection="3d")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    ax.plot_surface(X, Y, table.T, cmap=reversed_map)
    plt.title('Heightmap')
    plt.savefig("HeightMap_et_BdP_2D/Height_map.jpg", bbox_inches='tight')


def Plot2DSurface(table, name_file="2DPlot", name_title="2D plot", dpi=100):
    orig_map = plt.cm.get_cmap('gray')
    reversed_map = orig_map.reversed()
    plt.close("all")
    plt.imshow(table, origin='upper', cmap=reversed_map)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title(name_title)
    plt.savefig(name_file, dpi=dpi)


def PlotCat(table, taille, name_title, name_file, alpha=None, bgColor='#000000'):
    echelle = ListedColormap(['#141872', '#0970a6', '#119fe9', '#eeec7e',
                              '#5df147', '#38be2a', '#336e1c', '#004704', 'white'], 8)

    Cat = np.zeros((taille, taille))

    for i in range(taille):
        for j in range(taille):
            s = table[i][j]
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
    plt.imshow(np.zeros_like(Cat), cmap=ListedColormap([bgColor]), vmin=0, vmax=0)
    plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=7, alpha=alpha)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.title(name_title)
    plt.savefig(name_file, dpi=500)
    return Cat


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


def Bruit_Overworld(taille, pixels, precsision, amplitude, nb_vecteur, Entre, Sortie):
    frames_bruit = []
    frames_carte = []

    resultats = []
    for Num_Bruit in trange(1, 9):
        temporaire = Perlin_2D(precsision, pixels, taille, nb_vecteur)
        if Num_Bruit == 1:
            temporaire += 1

        temporaire *= amplitude

        resultats.append(temporaire)

        Plot2DSurface(temporaire, name_title=f'Bruit de Perlin n°{Num_Bruit}', name_file=f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
        Cat = PlotCat(fonction_passage(sum(resultats), Entre, Sortie), taille, name_title=f'Carte au Trésor avec {Num_Bruit} bruits', name_file=f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        image_bruit = imageio.v2.imread(f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
        frames_bruit.append(image_bruit)
        image_carte = imageio.v2.imread(f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        frames_carte.append(image_carte)

        precsision *= 2
        amplitude //= 2

    imageio.mimsave(f"Overworld/Evolution_Carte.gif", frames_carte, duration=500)
    imageio.mimsave(f"HeightMap_et_BdP_2D/Tout_les_bruits.gif", frames_bruit, duration=500)

    resultat = sum(resultats)
    resultat = fonction_passage(resultat, Entre, Sortie)
    Plot2DSurface(resultat, name_file=f"HeightMap_et_BdP_2D/Bruit_2D_map.jpg", name_title='Bruit de Perlin en 2D',)
    Plot3DSuraface(resultat, taille)
    return resultat, Cat


def Bruit_Arbres(pixels, precsision):

    amplitude = 12
    resultats = []
    for _ in range(1, 4):
        temporaire = Perlin_2D(precsision, pixels, pixels, 8)
        temporaire += .5

        temporaire *= amplitude

        resultats.append(temporaire)

        precsision *= 2
        amplitude //= 2

    resultat = sum(resultats)

    return ((resultat - 3)//6)*6


# Plateau

def miniAfine(x1, x2, y1, y2, x):
    pente = (y2 - y1) / (x2 - x1)
    x -= x1
    y = pente * x
    y += y1
    return y


def fonction_passage(BdP, Entre, Sortie):
    for x in range(len(BdP)):
        for y in range(len(BdP[x])):
            for i in range(1, len(Entre)):
                if Entre[i-1] >= BdP[x, y] > Entre[i]:
                    BdP[x, y] = int(miniAfine(Entre[i-1], Entre[i], Sortie[i-1], Sortie[i], BdP[x, y]))
    plt.close("all")
    ax = plt.axes()
    ax.plot(Entre[1:-1], Sortie[1:-1], 'r')
    ax.plot([190, 60], [150, 150], 'b')
    ax.invert_yaxis()
    ax.invert_xaxis()
    plt.savefig("HeightMap_et_BdP_2D/Courbe_Plateau")
    return BdP


def derivate(tab: np.ndarray, dx, dy):
    der = np.zeros_like(tab)
    height, width = np.shape(der)
    for x in range(height):
        for y in range(width):
            der[x, y] = abs(tab[max(0, x - dx), max(0, y - dy)]
                            - tab[min(height - 1, x + dx), min(width - 1, y + dy)])
    return der
