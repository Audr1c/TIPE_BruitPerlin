import numpy as np
from tqdm import trange

def lineaire(a, b, x):
    return a + x * (b - a)


def lissage(t):
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient3D(c, x, y, z):
    # Récupère les coords des vecteurs de gradient
    vecteurs = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1],
                        [-1, 0, -1], [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [-1, 1, 0], [0, -1, 1], [0, -1, -1]])
    co_gradient = vecteurs[c % 16]
    return co_gradient[:, :, :, 0] * x + co_gradient[:, :, :, 1] * y + co_gradient[:, :, :, 2] * z


# Bruit 3D


def Perlin3D(precsision, taille, hauteur):
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
    x_int, y_int, z_int = x.astype(int), y.astype(int), z.astype(int)

    # normes des vecteurs
    x_dec, y_dec, z_dec = x - x_int, y - y_int, z - z_int
    # on lisse les normes (algo 2d perlin tu coco)
    x_lis, y_lis, z_lis = lissage(x_dec), lissage(y_dec), lissage(z_dec)

    g000 = gradient3D(perm[perm[perm[x_int]   + y_int]   + z_int],   x_dec,   y_dec,   z_dec)
    g001 = gradient3D(perm[perm[perm[x_int]   + y_int]   + z_int+1], x_dec,   y_dec,   z_dec-1)
    g010 = gradient3D(perm[perm[perm[x_int]   + y_int+1] + z_int],   x_dec,   y_dec-1, z_dec)
    g011 = gradient3D(perm[perm[perm[x_int]   + y_int+1] + z_int+1], x_dec,   y_dec-1, z_dec-1)
    g100 = gradient3D(perm[perm[perm[x_int+1] + y_int]   + z_int],   x_dec-1, y_dec,   z_dec)
    g101 = gradient3D(perm[perm[perm[x_int+1] + y_int]   + z_int+1], x_dec-1, y_dec,   z_dec-1)
    g110 = gradient3D(perm[perm[perm[x_int+1] + y_int+1] + z_int],   x_dec-1, y_dec-1, z_dec)
    g111 = gradient3D(perm[perm[perm[x_int+1] + y_int+1] + z_int+1], x_dec-1, y_dec-1, z_dec-1)
    # On interpole linéairement pour faire une moyenne
    # C'est ce qui fait que la transition de couleurs des taille est clean
    x00 = lineaire(g000, g100, x_lis)
    x10 = lineaire(g010, g110, x_lis)
    x01 = lineaire(g001, g101, x_lis)
    x11 = lineaire(g011, g111, x_lis)

    xy0 = lineaire(x00, x10, y_lis)
    xy1 = lineaire(x01, x11, y_lis)

    resultat = lineaire(xy0, xy1, z_lis)
    return resultat


def Cave(Overworld, precsision, amplitude, nb_br, taille, hauteur):
    resultat = []
    for _ in trange(nb_br):
        temporaire = Perlin3D(precsision, taille, hauteur)
        temporaire += .5
        temporaire *= amplitude

        resultat.append(temporaire)
        precsision *= 2
        amplitude //= 2
    resultat = sum(resultat)
    return resultat//1


def mini_BdP_3D(x, z, y):
    None