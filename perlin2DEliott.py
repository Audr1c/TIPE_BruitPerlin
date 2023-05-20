import numpy as np
import matplotlib.pyplot as plt


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


def f(x, y, M):
    return M[x, y]


def r(x, y):
    return x * 2 + y ** 2


def perlin(graine, taille):
    tab = np.linspace(1, 10, 1500, endpoint=False)

    # création de grille en utilisant le tableau 1d
    x, y = np.meshgrid(tab, tab)

    # On crée une permutation en fonction du nb de pixels
    # On utilise la fonction seed parce que numpy chiale si on le fait pas

    perm = np.arange(256, dtype=int)
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


def perlinfzej(graine, taille, hauteur):
<<<<<<< Updated upstream
=======
    precsision = 10
    amplitude = 100
    resultats = []
    for _ in trange(8):
        temporaire = perlin(precsision, taille)
        temporaire += 0.5
        temporaire *= amplitude
>>>>>>> Stashed changes

    # creation Base ( grosse forme)
    res1 = perlin(graine, taille)

    # creation petit bruit
    res2 = perlin(graine, taille)

    # si grosse :
    res1 += 0.5
    res1 **= 2
    res1 *= 200 
    res1 += 50

    # sinon
    res2 *= 2

    resultat = res1 + res2
    tab2 = np.linspace(0, taille, taille, endpoint=False)

    # création de grille en utilisant le tableau 1d
    X, Y = np.meshgrid(tab2, tab2)

    D = np.zeros((taille, taille))
    for i in range(taille):
        D[i] = resultat[i][0:taille]
    autre = D / taille
    autre *= 7


    plt.imshow(D, origin='upper', cmap='gray')
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title('Bruit de Perlin en 2D (seed = ' + str(graine) + ')')
    plt.savefig(f"2_Dimensions/Height_Map.jpg")
    T = np.array([[D[i, j] for i in range(taille)] for j in range(taille)])
    plt.close("all")
    ax = plt.axes(projection="3d")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    ax.plot_surface(X, Y, T, cmap='gray')
    plt.title('Heightmap (seed = ' + str(graine) + ')')
    plt.savefig("2_Dimensions/Height_map")


    return D, autre
