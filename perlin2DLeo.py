import random

import matplotlib.pyplot as plt
import numpy as np


def lerp(a, b, x):
    "interpolation linéaire (produit scalaire)"
    return a + x * (b - a)


def lissage(f):
    "Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)"
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3


def gradient(c, x, y):
    "On chope les coords des vecteurs de gradient"
    vecteurs = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    co_gradient = vecteurs[c % 4]
    return co_gradient[:, :, 0] * x + co_gradient[:, :, 1] * y


def perlin(x, y, seed=0):
    # On crée une permutation en fonction du nb de pixels
    # On utilise la fonction seed parce que numpy chiale si on le fait pas
    np.random.seed(seed)
    perm = np.arange(num, dtype=int)
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
    return lerp(x1, x2, yf)


# tableau classique de 500 points sur [1;10]
num2 = 20
tab = np.linspace(1, num2, 500, endpoint=False)
num = 16 * (num2//10)
# création de grille en utilisant le tableau 1d
x, y = np.meshgrid(tab, tab)
resultat = perlin(x, y, seed=random.randint(0,500))
plt.imshow(resultat, origin='upper')
plt.colorbar()
plt.savefig(f"2_Dimensions/Height_MapLeo{num2}.jpg")
plt.show()

