## Importation

from random import randrange
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange
from matplotlib.colors import ListedColormap
import imageio
from nbtschematic import SchematicFile
from perlin1DEliott import *

## Fonction utile

def lerp(a, b, x):
    "interpolation linéaire (produit scalaire)"
    return a + x * (b - a)

def lissage(f):
    "Lisse le bordel (à changer pour obtenir autre chose qu'un labyrinthe)"
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3

def gradient3D(c, x, y, z):
    "On chope les coords des vecteurs de gradient"
    vecteurs = np.array([[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],[1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],[0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1],[1,1,0],[-1,1,0],[0,-1,1],[0,-1,-1]])
    co_gradient = vecteurs[c % 16]
    return co_gradient[:, :, :, 0] * x + co_gradient[:, :, :, 1] * y + co_gradient[:, :, :, 2] * z

## Bruit 3D

def Perlin3D(precsision):
    tab = np.linspace(1, precsision, taille, endpoint=False)
    tab1 = np.linspace(1, precsision, hauteur, endpoint=False)
    # création de grille en utilisant le tableau 1d
    x, y, z= np.meshgrid(tab, tab, tab1)

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
    x00 = lerp(g000 , g100, xf)
    x10 = lerp(g010 , g110, xf)
    x01 = lerp(g001 , g101, xf)
    x11 = lerp(g011 , g111, xf)

    xy0 = lerp(x00 , x10, yf)
    xy1 = lerp(x01 , x11, yf)

  
    resultat = lerp(xy0, xy1, zf)
    return resultat

def Bruit_Nether(precsision, amplitude):
    resultat=[]
    for Num_Bruit in trange(1,4):
        temporaire = Perlin3D(precsision)

        temporaire *= amplitude
        
        resultat.append(temporaire)
        precsision*=2
        amplitude//=2
    resultat= sum(resultat)
    frames_bruit = []
    if False:
        for Num_Bruit in trange(taille):
            
            plt.close("all")
            plt.imshow(resultat[Num_Bruit], origin='upper', cmap='gray')
            plt.xlabel('Y')
            plt.ylabel('X')
            plt.colorbar()
            plt.title(f'Bruit de Perlin en 2D (seed = {str(Num_Bruit)}) ')
            plt.savefig(f"2_Dimensions/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
            image_bruit = imageio.v2.imread(f"2_Dimensions/Bruits/Bruit_{Num_Bruit}_Amplitudes.jpg")
            frames_bruit.append(image_bruit)
        imageio.mimsave(f"2_Dimensions/Tout_les_bruits.gif", frames_bruit, duration=500)
        resultat //= 1
        print(f'max: {np.max(resultat):.2f}, min: {np.min(resultat):}')
    return resultat
    
## Détails

def Percolation(C, Robinet):
    while Robinet:    # Percolation tant que tous les voisins ne sont pas remplis
        (x, y, z) = Robinet[0]  # Prends le premier

        # Regarde les voisins, si ils sont vides, on met de l'eau et on les ajoutes à Robinet pour ragarder les voisins des voisins
        if C[x,y,z+1] == 0 and z <= Hlave:
            Robinet.append((x, y, z + 1))
            C[x,y,z+1] = 3
        if x != 0 and C[x-1,y,z] == 0:
            Robinet.append((x - 1, y, z))
            C[x-1,y,z] = 3
        if x != taille - 1 and C[x+1,y,z] == 0:
            Robinet.append((x + 1, y, z))
            C[x+1,y,z] = 3
        if y != 0 and C[x,y-1,z] == 0:
            Robinet.append((x, y - 1, z))
            C[x,y-1,z] = 3
        if y != taille - 1 and C[x,y-1,z] == 0:
            Robinet.append((x, y + 1, z))
            C[x,y+1,z] = 3
        if z - 1 !=0 and C[x,y,z-1] == 0:
            Robinet.append((x, y, z - 1))
            C[x,y,z-1] = 3
        Robinet.pop(0)  # Enlève l'élément qui a été étudié pour que la boucle finisse
        print(f"\r Longueur de Robinet : {len(Robinet)}", end="")
    print()

def Lava(Map):
    Robinet=[]
    for x in range(taille):
        for y in range(taille):
            if Map[x,y,Hlave]==0:
                Map[x,y,Hlave]=3
                Robinet.append((x,y,Hlave))
    Percolation(Map,Robinet)

def quartz(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i,y+k,z+j]==1 and random.random()<0.6:
                    C[x+i,y+k,z+j] = 6

def minerais(CarteListe3D):
    h = ((taille**2)//400)

    # charbon
    print("charbon")
    k = 15*h
    _, Yc = liste_aleatoire(k, taille - 4, k)
    _, Xc = liste_aleatoire(k, taille - 4, k)
    _, Zc = liste_aleatoire(k, hauteur - 4, k)
    for i in trange(k):
        quartz(CarteListe3D, int(Xc[i]), int(Zc[i]), int(Yc[i]))



## Convertion Minecraft

correspondanceID = {
                    0 : 0,  # Air
                    -1 : 87,  # Stone
                    3 : 11,
                    6 : 153
                    }

def CreteMapSchem3D(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))  # z = hauteur faux mais pas grave
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                sf.blocks[z, y, x] = correspondanceID[grid[x][y][z]]  # carte renversé
    sf.save(f'OutSchem/Carte{graine}.schematic')

def nether(g):
    print(g)
    np.random.seed(g)
    r=Bruit_Nether(3, 128)
    r//=256
    minerais(r)
    Lava(r)
    CreteMapSchem3D(r,taille,taille,hauteur,g)

Hlave=30
taille=400
hauteur=200
g=randrange(10000)

nether(g)