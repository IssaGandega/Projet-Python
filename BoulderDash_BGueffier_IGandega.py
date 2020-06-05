import upemtk
from upemtk import *
from random import *
from time import *
timer = 0
score = 0
fichier = 'map.txt'

with open('map.txt') as taille:
    #Comptage du nombre de lignes 
    nb_lignes = len(taille.readlines()) 
    #Hauteur de la fenêtre (75 étant la taille des images)
    hauteur_fenetre = nb_lignes*75      

with open('map.txt') as taille:
    
    texte = taille.read()
    #Comptage du nombre d'élément par ligne
    nb_cases = len(texte)//nb_lignes    
    #Longueur de la fenêtre (...)
    longueur_fenetre = nb_cases * 75    

hauteur_case = hauteur_fenetre//nb_lignes  
longueur_case = longueur_fenetre//nb_cases



def generer_matrice(fichier):
    ''' permet de générer une matrice à l'aide
    du fichier txt que l'on entre''' 
    with open(fichier) as carte:      
        matrice = []
        #Création d'une matrice:
        for i in range(nb_lignes):
            matrice.append([])
            for j in range(nb_cases):
                char = carte.read(1)
                if char != '\n':
                    matrice[i].append(char)
    return matrice



def affiche_case(matrice):
    '''permet de générer la map à l'aide de la matrice'''
    efface_tout()
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):        
            #On teste chaque élément pour créer des "classes" pour chaque élément
            if matrice[i][j] == 'W':  
                image(longueur_case * j,hauteur_case* i, 'Images/mur.png', ancrage = 'nw')
            if matrice[i][j] == 'J':
                image(longueur_case * j,hauteur_case* i, 'Images/diam_menu.png', ancrage = 'nw')
            elif matrice[i][j] == 'G':
                image(longueur_case * j,hauteur_case* i, 'Images/sol.png', ancrage = 'nw')
            elif matrice[i][j] == 'D':
                image(longueur_case * j,hauteur_case* i, 'Images/diamant.png', ancrage = 'nw')
            elif matrice[i][j] == 'B':
                image(longueur_case * j,hauteur_case* i, 'Images/rocher.png', ancrage = 'nw')
            elif matrice[i][j] == '.':
                image(longueur_case * j,hauteur_case* i, 'Images/vide.png', ancrage = 'nw')
            elif matrice[i][j] == 'R':
                image(longueur_case * j,hauteur_case* i, 'Images/perso.png', ancrage = 'nw')
            elif matrice[i][j] == 'E':
                image(longueur_case * j,hauteur_case* i, 'Images/arriveebloc.png', ancrage = 'nw')
            elif matrice[i][j] == 'M':
                image(longueur_case * j,hauteur_case* i, 'Images/menu.png', ancrage = 'nw')
            elif matrice[i][j] == 'F':
                image(longueur_case * j,hauteur_case* i, 'Images/arrivee.png', ancrage = 'nw')
    upemtk.texte(10,10,('Temps:',int(timer)), couleur = 'yellow')
    upemtk.texte(10,85,('Score:',score), couleur = 'yellow')
    upemtk.texte(longueur_fenetre-200,10,(compteur,'x'), couleur = 'yellow')
                

def nm_touche():
    ''' permet de définir la touche pressée'''
    evenement = donne_evenement()       
    type_ev = type_evenement(evenement)
    if type_ev == 'Touche':
        nom_touche = touche(evenement)
        return nom_touche

def direction(matrice,nom_touche):
    ''' déplace le personnage selon la touche pressée'''
    efface_tout()
    test_score = False
    for i in range(len(matrice)):                   
        for j in range(len(matrice[i])):
            #Prise en compte de chaque mouvement et de déplacement de rocher:
            if nom_touche == "Right" and matrice[i][j] == 'R' and matrice[i][j+1] != 'W' and matrice[i][j+1] != 'E': 
                if matrice[i][j+1] == 'B':
                    if matrice[i][j+2] == '.':
                        matrice[i][j+2] = 'B'
                    else:
                        return matrice,test_score
                test_score = True
                matrice[i][j+1] = 'R'
                matrice[i][j] = '.'
                return matrice,test_score
            elif nom_touche == "Left" and  matrice[i][j] == 'R' and matrice[i][j-1] != 'W' and matrice[i][j-1] != 'E':
                if matrice[i][j-1] == 'B':
                    if matrice[i][j-2] == '.':
                        matrice[i][j-2] = 'B'
                    else:
                        return matrice,test_score
                test_score = True
                matrice[i][j-1] = 'R'
                matrice[i][j] = '.'
                return matrice,test_score
            elif nom_touche == "Up" and matrice[i][j] == 'R' and matrice[i-1][j] != 'W' and matrice[i-1][j] != 'B' and matrice[i-1][j] != 'E':
                test_score = True
                matrice[i-1][j] = 'R'
                matrice[i][j] = '.'
                return matrice,test_score
            elif nom_touche == "Down" and matrice[i][j] == 'R' and matrice[i+1][j] != 'W' and matrice[i+1][j] != 'B' and matrice[i+1][j] != 'E':
                test_score = True
                matrice[i+1][j] = 'R'
                matrice[i][j] = '.'
                return matrice,test_score
    return matrice,test_score

                
def gagner(matrice,drapeau):
    ''' permet de savoir s'y l'on a gagné
    le paramètre drapeau contient les coordonées
    de l'arrivée'''
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == 'R' and i == drapeau[0] and j == drapeau[1]:
                return 1
    return 0



def ligne_arrivee(matrice):
    ''' permet de trouver les coordonées de l'arrivée'''
    for i in range(len(matrice)):
        for j in range(len(matrice[i])): 
            if matrice[i][j] == 'E':      
                #On cherche la position de la ligne d'arrivée
                return (i,j)

    

def sauvegarder(matrice):
    ''' sauvegarde la matrice actuelle dans un fichier txt'''
    with open('save.txt','w') as save:
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                save.write(matrice[i][j])
            save.write('\n')
    with open ('score.txt','w') as scores:
        scores.write(str(score))
        scores.write('\n')
        scores.write(str(timer))
        scores.write('\n')
        scores.write(str(compteur))
    


def eboulement(matrice,meurt):
    ''' permet de gérer les éboulements et de laisser
    le temps au joueur d'y échapper grâce à meurt'''
    efface_tout()
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == 'B' and matrice[i+1][j] == '.' and matrice[i+2][j] == 'R':
                matrice[i][j] = '.'
                matrice[i+1][j] = 'B'
                matrice[i+2][j] = 'R'
                meurt = True
                return matrice,meurt
            elif matrice[i][j] == 'B' and matrice[i+1][j] == 'R' and meurt == True:
                matrice[i][j]= '.'
                matrice[i+1][j]= 'B'
                return matrice,meurt
            elif matrice[i][j] == 'D' and matrice[i+1][j] == '.' and matrice[i+2][j] == 'R':
                matrice[i][j] = '.'
                matrice[i+1][j] = 'D'
                matrice[i+2][j] = 'R'
                meurt = True
                return matrice,meurt
            elif matrice[i][j] == 'D' and matrice[i+1][j] == 'R' and meurt == True:
                matrice[i][j] = '.'
                matrice[i+1][j] = 'D'
                return matrice,meurt
            #On cherche dans la map où se trouve un rocher placé au-dessus d'une case vide
            elif matrice[i][j] == 'B' and matrice[i+1][j] == '.':    
                matrice[i+1][j] = 'B'
                matrice[i][j] = '.'
                return matrice,meurt
                #Déplacement de rocher si il y a 2 rochers empillés
            elif matrice[i][j] == 'B' and matrice [i+1][j] == 'B' and matrice [i][j+1] == '.' and matrice[i+1][j+1] == '.':     
                matrice[i][j] = '.'
                matrice[i][j+1] = 'B'
                return matrice,meurt
                #Idem
            elif matrice[i][j] == 'B' and matrice [i+1][j] == 'B' and matrice [i][j-1] == '.' and matrice[i+1][j-1] == '.':     
                matrice[i][j] = '.'
                matrice[i][j-1] = 'B'
                return matrice,meurt
            elif matrice[i][j] == 'D' and matrice[i+1][j] == '.':    
                matrice[i+1][j] = 'D'
                matrice[i][j] = '.'
                return matrice,meurt
    meurt = False
    return matrice,meurt
    


                
def debug(matrice):
    ''' gère le mode débug ( g )'''
    #On initialise une variable alea qui prendra comme valeur un déplacement
    meurt = False
    matrice,meurt = eboulement(matrice,meurt)
    alea=choice(["Right","Left","Up","Down"]) 
    sleep(0.15)
    matrice,test = direction(matrice,alea)
    gagne = gagner(matrice,drapeau)
    perdre = perdu(matrice)
    affiche_case(matrice)
    mise_a_jour()
    return matrice



def perdu(matrice):
    ''' vérifie si l'on a perdu'''
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == 'R':
                return 0
    return 1



def diamants(liste):
    ''' créé une liste contenant la position des diamants'''
    efface_tout()
    liste = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == 'D':
                liste.append((i,j))
    return (liste)
            

def map_random(matrice):
    ''' génère une matrice aléatoire'''
    mat = [[],[]]
    for i in range(len(matrice[0])):
        mat[0].append('M')
        mat[1].append('W')
    mat[0][-1] = 'J'
    for i in range(2,nb_lignes-1):
        mat.append([])
        mat[i].append('W')
        for j in range(1,len(mat[0])-1):
            rand = randint(0,100)
            if rand < 10:
                mat[i].append('D')
            elif rand >= 10 and rand < 15:
                mat[i].append('.')
            elif rand >= 15 and rand < 30:
                mat[i].append('B')
            elif rand >= 30:
                mat[i].append('G')
        mat[i].append('W')
    mat.append([])
    for i in range(len(matrice[0])):
        mat[-1].append('W')
    mat[4][3] = 'R'
    mat[7][12] = 'E'
    return mat
            
    

if __name__ == "__main__":
    
    jouer = False
    quitter = False
    cree_fenetre(400,500)
    while True:
        ligne(0,70,400,70,epaisseur=2)
        rectangle(50, 100, 350, 170, couleur='red', remplissage='red', epaisseur=1, tag='bouton1')
        rectangle(50, 200, 350, 270, couleur='blue', remplissage='blue', epaisseur=1, tag='bouton2')
        rectangle(50, 300, 350, 370, couleur='yellow', remplissage='yellow', epaisseur=1, tag='bouton3')
        upemtk.texte(200, 20, "Boulder Dash", couleur='black', ancrage='n', police='Helvetica', taille=24, tag='Titre')
        upemtk.texte(200, 120, "Jouer (map fichier)", couleur='blue', ancrage='n', police='Arial', taille=20, tag='texte1')
        upemtk.texte(200, 220, "Jouer (map aléatoire)", couleur='red', ancrage='n', police='Arial', taille=20, tag='texte2')
        upemtk.texte(200, 320, "Quitter", couleur='black', ancrage='n', police='Arial', taille=20, tag='texte3')
        upemtk.texte(0,500,"Créé par GUEFFIER Benjamin et GANDEGA Issa", couleur = 'grey',ancrage='sw',police="Arial",taille=12,tag="crédits")
        
        event = donne_evenement()
        type_ev = type_evenement(event)
        
        mise_a_jour()
        
        if type_ev == "ClicGauche":
            if clic_x(event) > 50 and clic_x(event) < 350:
                if clic_y(event) > 100 and clic_y(event) < 170:
                    jouer = True
                    matrice = generer_matrice('map.txt')
                    
        if type_ev == "ClicGauche":
            if clic_x(event) > 50 and clic_x(event) < 350:
                if clic_y(event) > 200 and clic_y(event) < 270:
                    jouer = True
                    matrice = generer_matrice(fichier)
                    matrice = map_random(matrice)
                    
        if type_ev == "ClicGauche":
            if clic_x(event) > 50 and clic_x(event) < 350:
                if clic_y(event) > 300 and clic_y(event) < 370:
                    quit()
    
    
        if jouer == True and quitter == False:
            break
        
    
    ferme_fenetre()
    
    
    cree_fenetre(longueur_fenetre-75,hauteur_fenetre)
    timer = 50
    score = 100
    compteur = 0
    k = 0
    sauvegarde = 'save.txt'
    affiche_case(matrice)
    gagne = 0
    perdre = 0
    drapeau = ligne_arrivee(matrice)
    liste_diam = []
    k = 1
    liste_diam = diamants(liste_diam)
    objectif = int((len(liste_diam)*2)//3)
    touches_jeu = ['Up','Down','Left','Right']
    temps_eboul = 0
    meurt = False
    
    while True:
                
        if perdre == 1:
            score = 0
            image((longueur_fenetre-75)//2,hauteur_fenetre//2, 'Images/perdu.png', ancrage = 'center')
            sleep(2.0)
            attente_touche()
            break
        if gagne == 1: 
            #Sortie de la boucle
            image((longueur_fenetre-75)//2,hauteur_fenetre//2, 'Images/gagne.png', ancrage = 'center')
            sleep(2.0)
            attente_touche()
            break

        #Appel de fonction
        temps= time()
        nom_touche=nm_touche()
        matrice,test = direction(matrice,nom_touche)
        temps_eboul+=1
        if temps_eboul == 1:
            temps_eboul = 0
            matrice,meurt = eboulement(matrice,meurt)
        if test == True:
            score -= 1
        new_list = diamants(liste_diam)
        old_compt = compteur
        compteur = len(liste_diam) - len(new_list)
        if old_compt != compteur:
            timer += 10
            score += 4
        affiche_case(matrice)
        mise_a_jour()
        if compteur >= objectif:
            for i in range(len(matrice)):
                for j in range(len(matrice[i])):
                    if matrice[i][j] == 'E':
                        matrice[i][j] = 'F'
        gagne = gagner(matrice,drapeau)
        perdre = perdu(matrice)
        new_temps = time()
        timer -= new_temps-temps
        if timer <= 0:
            perdre = 1
        
        #Mode débugage
        if nom_touche=="g":
            print("Mode débugage:")
            nom_touche=""
            while nom_touche != "g" or perdre == 1 or gagne == 1:
              matrice=debug(matrice)
              nom_touche=nm_touche()
        
        # Restart la map initiale
        elif nom_touche=="r":
            matrice = generer_matrice(fichier)
            liste_diam = diamants(liste_diam)
            new_list = diamants(liste_diam)
            compteur = 0
            timer = 50
            score = 100
        
        # Charger la map sauvegardée
        elif nom_touche == "c":
            matrice = generer_matrice(sauvegarde)
            liste_diam = diamants(liste_diam)
            new_list = diamants(liste_diam)
            with open ('score.txt') as scores:
                score = int(scores.readline())
                timer = float(scores.readline())
                compteur_save = int(scores.readline())
                score = score - 4*compteur
                timer = timer - 10*compteur
            compteur = compteur_save
                
                
            
        # Sauvegarder la map
        elif nom_touche == "s":
            sauvegarder(matrice)
        
        
        #Fin mode débugage          
        
            
            
    with open('scores.txt','r') as record:
        high = record.readline()
        if high != '':
            high = int(high)
        else:
            high = 0
    print('Score:',score,'/100')
    if score > high:
        print('Vous avez battu le highscore qui était de', high)
        with open('scores.txt','w') as scores:
            scores.write(str(score))
    efface_tout()
    
