# Importation


from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange, tqdm
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


def Plot2DSurface(table, name_file="2DPlot", name_title="2D plot", dpi=500):
    orig_map = plt.cm.get_cmap('gray')
    reversed_map = orig_map.reversed()
    plt.close("all")
    plt.imshow(table, origin='upper', cmap=reversed_map)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title(name_title)
    plt.savefig(name_file, dpi=dpi)


def PlotCat(table, taille, Cat_scratcher, name_title, name_file, alpha=None, bgColor='#000000', dpi=1000):
    echelle = ListedColormap(Cat_scratcher[0], len(Cat_scratcher[0]))

    Cat = np.zeros((taille, taille))

    for i in range(taille):
        for j in range(taille):
            s = table[i][j]
            for k in range(len(Cat_scratcher[1])-1):
                if Cat_scratcher[1][k] >= s > Cat_scratcher[1][k+1]:
                    Cat[i, j] = k + (k == len(Cat_scratcher)-2)

    plt.close("all")
    plt.imshow(np.zeros_like(Cat), cmap=ListedColormap([bgColor]), vmin=0, vmax=0)
    plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=7, alpha=alpha)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.title(name_title)
    plt.savefig(name_file, dpi=dpi)
    return Cat


def PlotNeon(BdP, taille, Der, Cat_scratcher):
    for inte, col, name in tqdm([(12, 6, "Dark"), (7, 9, "Middle"), (1, 11, "Light")]):
        intervalle = .025 * inte + 0.6
        col = "#" + 3 * "{0:02x}".format(col)
        alph = intervalle * Der / np.max(Der) + 1 - intervalle - .000000000000001
        # essayons d'appliquer un filtre visuel sur le alpha de la carte au tresor avec la derive en tant que parametre
        PlotCat(BdP, taille, Cat_scratcher, name_title=f"Carte Modifier {name}", name_file=f"Overworld/Neon/Carte{name}.jpg", alpha=alph,
                bgColor=col, dpi=4000)


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


def Bruit_Overworld(taille, pixels, precsision, amplitude, nb_vecteur, Cat_scratcher, Entre, Sortie):
    frames_bruit = []
    frames_carte = []

    resultats = []
    for Num_Bruit in trange(1, 9):
        temporaire = Perlin_2D(precsision, pixels, taille, nb_vecteur)
        if Num_Bruit == 1:
            temporaire += .7

        temporaire *= amplitude

        resultats.append(temporaire)

        Plot2DSurface(temporaire, name_title=f'Bruit de Perlin n°{Num_Bruit}', name_file=f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
        Cat = PlotCat(fonction_passage(sum(resultats), Entre, Sortie), taille, Cat_scratcher, name_title=f'Carte au Trésor avec {Num_Bruit} bruits', name_file=f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
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
    ax.plot([205, 25], [150, 150], 'b')
    ax.invert_yaxis()
    ax.invert_xaxis()
    plt.savefig("HeightMap_et_BdP_2D/Courbe_Plateau")
    return BdP


# Derivation


def Derivation(BdP):
    Der1_x = derivate(BdP, 1, 0)
    Der1_y = derivate(BdP, 0, 1)
    # Plot2DSurface(Der1_x, name_file="HeightMap_et_BdP_2D/Derivation/Der1X_2D.jpg", name_title="Der1 X 2D", dpi=1500)
    # Plot2DSurface(Der1_y, name_file="HeightMap_et_BdP_2D/Derivation/Der1Y_2D.jpg", name_title="Der1 Y 2D", dpi=1500)
    Der1_combined = Der1_y + Der1_x
    Plot2DSurface(Der1_combined, name_file="HeightMap_et_BdP_2D/Derivation/Der1ALL_2D.jpg", name_title="Der1 Combined 2D", dpi=4000)
    return Der1_combined


def Laplacien(BdP: np.ndarray):
    Der2_x = derivate(derivate(BdP, 1, 0), 1, 0)
    Der2_y = derivate(derivate(BdP, 0, 1), 0, 1)
    Der2_combined = Der2_y + Der2_x
    # Plot2DSurface(Der2_x, name_file="HeightMap_et_BdP_2D/Derivation/Der2X_2D.jpg", name_title="Der2 X 2D", dpi=1500)
    # Plot2DSurface(Der2_y, name_file="HeightMap_et_BdP_2D/Derivation/Der2Y_2D.jpg", name_title="Der2 Y 2D", dpi=1500)
    Plot2DSurface(Der2_combined, name_file="HeightMap_et_BdP_2D/Derivation/Der2ALL_2D.jpg", name_title="Der2 Combined 2D", dpi=5000)
    return Der2_combined


def derivate(tab: np.ndarray, dx, dy):
    der = np.zeros_like(tab)
    height, width = np.shape(der)
    for x in trange(height):
        for y in range(width):
            der[x, y] = abs(tab[max(0, x - dx), max(0, y - dy)]
                            - tab[min(height - 1, x + dx), min(width - 1, y + dy)])
    return der

