## Importation

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from matplotlib.colors import ListedColormap
import imageio

## Fonctions utiles

def lerp(a, b, x):
    # interpolation linéaire (produit scalaire)
    return a + x * (b - a)

def lissage(f):
    # Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3

def gradient(c, x, y):
    # On chope les coords des vecteurs de gradient
    sq2 = sqrt(2)
    vecteurs = np.array([[0, 1], [0, -1], [1, 0], [-1, 0], [1 / sq2, 1 / sq2], [-1 / sq2, 1 / sq2], [1 / sq2, -1 / sq2], [-1 / sq2, -1 / sq2]])
    co_gradient = vecteurs[c % 8]
    return co_gradient[:, :, 0] * x + co_gradient[:, :, 1] * y

## Bruit de Perlin

def Perlin_2D(precsision, pixels, taille):
    
    new_precsision = 1 + (precsision - 1) * taille / pixels
    tab = np.linspace(1, new_precsision, taille, endpoint=False)
    perm = np.arange((16 * new_precsision // 5), dtype=int)

    # création de grille en utilisant le tableau 1d
    x, y = np.meshgrid(tab,tab)

    # On crée une permutation en fonction du nb de pixels
    # On utilise la fonction seed parce que numpy chiale si on le fait pas


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

    return resultat

def Bruit_Overworld(taille, pixels, precsision, amplitude):
    frames_bruit = []
    frames_carte = []

    resultats = []
    echelle = ListedColormap(['#141872','#0970a6', '#119fe9','#eeec7e', '#5df147', '#38be2a','#336e1c','#004704','white'], 8)
    orig_map=plt.cm.get_cmap('gray')
    reversed_map = orig_map.reversed()
    for Num_Bruit in trange(1,9):
        temporaire = Perlin_2D(precsision, pixels, taille)
        if Num_Bruit==1:
            temporaire += 1

        temporaire *= amplitude
        
        resultats.append(temporaire)
        
        plt.imshow(temporaire, origin='upper', cmap=reversed_map)
        plt.xlabel('Y')
        plt.ylabel('X')
        plt.colorbar()
        plt.title(f'Bruit de Perlin n°{Num_Bruit}')
        plt.savefig(f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")


        Cat = np.array([[0 for i in range(taille)] for j in range(taille)])
        Temp2 = sum(resultats)
        for i in range(taille):
            for j in range(taille):
                s=Temp2[i][j]
                if 256>=s>180:
                    Cat[i,j]=0
                elif 180>=s>165:
                    Cat[i,j]=1
                elif 165>=s>150:
                    Cat[i,j]=2
                elif 150>=s>147:
                    Cat[i,j]=3
                elif 147>=s>120:
                    Cat[i,j]=4
                elif 120>=s>90:
                    Cat[i,j]=5
                elif 90>=s>60:
                    Cat[i,j]=6
                elif 60>=s:
                    Cat[i,j]=8
    
        
        plt.close("all")
        plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=7)
        plt.xlabel('Y')
        plt.ylabel('X')
        plt.title(f'Carte au Trésor avec {Num_Bruit} bruits')
        plt.savefig(f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        image_bruit = imageio.v2.imread(f"HeightMap_et_BdP_2D/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
        frames_bruit.append(image_bruit)
        image_carte = imageio.v2.imread(f"Overworld/Cartes/carte_{Num_Bruit}.jpg")
        frames_carte.append(image_carte)

        precsision *= 2
        amplitude //= 2

    imageio.mimsave(f"Overworld/Evolution_Carte.gif", frames_carte, duration=500)
    imageio.mimsave(f"HeightMap_et_BdP_2D/Tout_les_bruits.gif", frames_bruit, duration=500)





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

    return resultat,Cat


def Bruit_Arbres(pixels, precsision):

    amplitude = 8
    resultats = []
    for _ in trange(1,4):
        temporaire = Perlin_2D(precsision, pixels, pixels)
        temporaire += .5

        temporaire *= amplitude
        
        resultats.append(temporaire)

        precsision *= 2
        amplitude //= 2

    resultat = sum(resultats)

    return resultat
