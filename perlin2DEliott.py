## Importation
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from matplotlib.colors import ListedColormap

## Fonctions utiles
def lerp(a, b, x):
    "interpolation linéaire (produit scalaire)"
    return a + x * (b - a)

def lissage(f):
    "Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)"
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3

def gradient(c, x, y):
    "On chope les coords des vecteurs de gradient"
    vecteurs = np.array([[0, 1], [0, -1], [1, 0], [-1, 0], [1 / 2, 1 / 2], [-1 / 2, 1 / 2], [1 / 2, -1 / 2], [-1 / 2, -1 / 2]])
    co_gradient = vecteurs[c % 8]
    return co_gradient[:, :, 0] * x + co_gradient[:, :, 1] * y

## Bruit de Perlin

def Perlin(precsision, pixels):
    tab = np.linspace(1, precsision, pixels, endpoint=False)

    # création de grille en utilisant le tableau 1d
    x, y = np.meshgrid(tab, tab)

    # On crée une permutation en fonction du nb de pixels
    # On utilise la fonction seed parce que numpy chiale si on le fait pas

    perm = np.arange(16 * (precsision // 10), dtype=int)
    np.random.shuffle(perm)

    # on fait un tableau 2d qu'on applatit
    # pour faire des produits scalaires correctement
    # (les tableaux numpy sont chiants)
    perm = np.stack([perm, perm]).flatten()
    # Coordonnées de la grille
    xi, yi = x.astype(int), y.astype(int)

    # normes des vecteurs
    xg, yg = x - xi, y - yi
    # on lisse les normes (algo 2d perlin tu coco)
    xf, yf = lissage(xg), lissage(yg)

    # C'est le moment où on chiale
    # On chope les coords vecteur dans les 4 coins de la grille
    # (haut gauche/droite, bas gauche/droite)

    n00 = gradient(perm[perm[xi] + yi], xg, yg)
    n01 = gradient(perm[perm[xi] + yi + 1], xg, yg - 1)
    n11 = gradient(perm[perm[xi + 1] + yi + 1], xg - 1, yg - 1)
    n10 = gradient(perm[perm[xi + 1] + yi], xg - 1, yg)

    # On interpole linéairement pour faire une moyenne
    # C'est ce qui fait que la transition de couleurs des pixels est clean
    x1 = lerp(n00, n10, xf)
    x2 = lerp(n01, n11, xf)

    plt.close("all")
    resultat = lerp(x1, x2, yf)

    """
    """

    return resultat

def Bruit_de_map(graine, taille, hauteur, pixels, precsision, amplitude):
    resultats = []
    for _ in trange(7):
        temporaire = Perlin(precsision, pixels)
        temporaire += 0.5
        temporaire *= amplitude

        precsision *= 2
        amplitude /= 2

        resultats.append(temporaire)

    resultat = sum(resultats)
    tab2 = np.linspace(0, taille, taille, endpoint=False)

    # création de grille en utilisant le tableau 1d
    X, Y = np.meshgrid(tab2, tab2)

    D = np.zeros((taille, taille))
    for i in range(taille):
        D[i] = resultat[i][0:taille]

    plt.imshow(D, origin='upper', cmap='gray')
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title('Bruit de Perlin en 2D (seed = ' + str(graine) + ')')
    plt.savefig(f"2_Dimensions/Height_Map.jpg")

    T = np.array([[0 for i in range(taille)] for j in range(taille)])
    for i in range(taille):
        for j in range(taille):
            s=D[i,j]
            if 256>=s>180:
                T[i,j]=0
            elif 180>=s>160:
                T[i,j]=1
            elif 160>=s>150:
                T[i,j]=2
            elif 150>=s>147:
                T[i,j]=3
            elif 147>=s>120:
                T[i,j]=4
            elif 120>=s>90:
                T[i,j]=5
            elif 90>=s>60:
                T[i,j]=6
            elif 60>=s:
                T[i,j]=7
    
    echelle = ListedColormap(['#141872','#0970a6', '#119fe9','#eeec7e', '#5df147', '#38be2a','#336e1c','white'], 7)
    plt.close("all")
    plt.imshow(T, origin='upper', cmap=echelle, vmin=0, vmax=7)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.title('Carte au Trésor (seed = ' + str(graine) + ')')
    plt.savefig(f"2_Dimensions/Carte_au_Trésor.jpg")

    plt.close("all")
    ax = plt.axes(projection="3d")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    ax.plot_surface(X, Y, D, cmap='gray')
    plt.title('Heightmap (seed = ' + str(graine) + ')')
    plt.savefig("2_Dimensions/Height_map")

    return D
