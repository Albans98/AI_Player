# -*- coding: utf-8 -*-
"""
Created on Thu May 9, 2019

@authors: Alban STEFF & Soumaya SABRY 
         Fanny ZHONG & Alexandre SALOU

Description : le code est divisé en 4 parties:
                1-Celle des petites fonctions qui aident a la construcion de min max
                   comme Actions , Utility, AfficherGrill ...etc
                2-Celle des fonctions MinMax en ajoutant la profondeur
                3-Celle des fonctions MinMax en ajoutant la coupure de Alpha et Beta
                4-Menu pour le choix d'algorithme à utiliser (entre partie 2 et 3 )
"""

#%%##############################################################################################################
#######################################  Partie 1 <Petites fonctions>  ##########################################
#################################################################################################################

# initial :
## fonction qui initialise la grille en fonction d'une taille et du symbole du premier joueur
def initial (taille, sysQuiCommence):
    grille = [[" " for i in range(taille)]for j in range(taille)] #initialisation de la grille vide
    grille[int((taille-1)/2)][int((taille-1)/2)] =sysQuiCommence #placement du premier symbole au centre
    return grille


# Affichage_grille :
## affiche la matrice sous la forme de plateau de jeu
def Affichage_grille(grille):
    print("      1   2   3   4   5   6   7   8   9  10  11  12  13  14  15")
    lettre = "@"
    for i in range (len(grille)): 
        lettre = chr(ord(lettre) + 1) # lettre=A puis B puis C,...(ord() retourne le code du caractere, chr() retourne le caractere)
        for j in range (len(grille)):
            if j == 0:
                print(lettre + " : | " + grille[i][j], end =' | ') # affichage des lettres 
            else:
                print(grille[i][j], end =' | ')
        print()
        
# Score : 
## fonction qui évalue la valeur de chaque case de la grille
## retourne un dictionnaire ayant pour clés des couples (i,j) correspondant aux index de chaque case
## les valeurs associées aux clés correspondent aux scores attribués chaque case
## ex : grille_score[(0,0)] contient la valeur de la case [0,0]
## methode d'évaluation : 
## pour chaque case, on prend les 4 voisins (en ligne/colonne/diagonale)
## on analyse ces 5 cases via la fonction verif_tronc_5()
def score(grille):
    grille_score = {} #initialisation du dictionnaire
    
    for i in range(15):
        for j in range(15):
            grille_score[(i,j)]=0
            
    cases_a_verif = [" "," "," "," "," "] #on fait l'analyse en prenant 5 cases à la fois
    # vertical
    for i in range(2, 13):
        for j in range(0, 15):
            for k in range(5):
                cases_a_verif[k] = grille[i+k-2][j]; #case_a_verif contient plusieurs symboles
            result_score_tronc_5 = verif_tronc_5(cases_a_verif); #result_score_tronc_5 va contenir les scores de case_a_verif 
            for k in range(5):
                if grille_score[(i+k-2,j)] < result_score_tronc_5[k]: #si les scores de grille_score sont inférieurs à ceux que l'on vient de calculer
                    grille_score[(i+k-2,j)] = result_score_tronc_5[k]; #on remplace les scores
    # horizontal
    for i in range(0, 15):
        for j in range(2, 13):
            for k in range(5):
                cases_a_verif[k] = grille[i][j+k-2];
            result_score_tronc_5 = verif_tronc_5(cases_a_verif);
            for k in range(5):
                if grille_score[(i,j+k-2)] < result_score_tronc_5[k]:
                    grille_score[(i,j+k-2)] = result_score_tronc_5[k];
    # diagonale 1
    for i in range(2, 13):
        for j in range(2, 13):
            for k in range(5):
                cases_a_verif[k] = grille[i+k-2][j+k-2];
            result_score_tronc_5 = verif_tronc_5(cases_a_verif);
            for k in range(5):
                if grille_score[(i+k-2,j+k-2)] < result_score_tronc_5[k]:
                    grille_score[(i+k-2,j+k-2)] = result_score_tronc_5[k];
    # diagonale 2
    for i in range(2,13):
        for j in range(2,13):
            for k in range(5):
                cases_a_verif[k] = grille[i-k+4-2][j+k-2];
            result_score_tronc_5 = verif_tronc_5(cases_a_verif);
            for k in range(5):
                if grille_score[(i-k+4-2,j+k-2)] < result_score_tronc_5[k]:
                    grille_score[(i-k+4-2,j+k-2)] = result_score_tronc_5[k];
    return grille_score; #retourne un dictionnaire


# verif_tronc_5 :
## Cette fonction analyse 5 cases et renvoie 5 scores pour ces 5 cases
## Le score est calculé en fonction du nombre de symboles ennemis ou alliés
def verif_tronc_5(cases): #cases contient les symboles sur le tronc que l'on analyse
    scores = [0,0,0,0,0]; #chaque score de chaque case du tronc
    nbrCasesX = 0;
    nbrCasesO = 0;
    for i in range(5):
        if cases[i] == "x":
            nbrCasesX = nbrCasesX + 1; #compte le nombre de cases alliées dans le tronc
        elif cases[i] == "o":
            nbrCasesO = nbrCasesO + 1; #compte le nombre de cases adverses
    if nbrCasesX > 0:
        if nbrCasesO > 0:  #s'il y a au moins une case ennemie,
            return scores; #on retourne [0,0,0,0,0]
        else: #s'il n'y a pas de case ennemie
            for i in range(5):
                if cases[i] == " ": #s'il y a une case vide
                    scores[i] = nbrCasesX / 5.0; #on divise le nombre de case par 5

    if nbrCasesO > 0: #meme logique
        if nbrCasesX > 0:
            return scores;
        else:
            for i in range(5):
                if cases[i] == " ":
                    scores[i] = nbrCasesO / 5.0;
    return scores;
    

# Actions :
## Retourne une liste d'index des cases sur lesquelles il est le plus interessant de jouer (top 5)
def Actions(grille): 
    liste_index = []
    #1 appel de la fonction score
    #2 definir les 10 premiers scores en tant que meilleurs scores, stocker leurs indices (les ajouter à la liste)
    #3 a partir du 11eme score : 
    #4 si le score est plus eleve qu'un des scores deja stockés, on remplace les indices
    
    grille_score={}
    grille_score = score(grille) #1
    compteur_initialisation = 0 #va servir a definir les 10 premiers scores
    Top = 5
    for i in range(len(grille)):
        for j in range(len(grille)):

            if compteur_initialisation < Top: #2
                liste_index.append((i,j))
                compteur_initialisation +=1
            else: #3
                 for k in range(Top) :
                     if ( grille_score[(i,j)] > grille_score[liste_index[k]] ): #4
                         liste_index[k]=(i,j)
                         break
            
    return liste_index       

# Resultat :
## Applique un changement sur la grille entrée en paramètre et retourne la grille modifiée
## index contient un seul couple de [i,j] et non l'ensemble des couples
def Resultat(index, grille, symbole):
    #1:redefinition d'une nouvelle matrice (sinon pb avec les pointeurs)
    nv_grille=[[" "for i in range(len(grille))]for j in range(len(grille))]
    for i in range(len(grille)):
      for j in range(len(grille)):
           nv_grille[i][j] = grille[i][j] #copie des valeurs
           
    #2:ajout de la modification
    nv_grille[index[0]][index[1]] = symbole 
    
    return nv_grille


# Verifier_lignes && Verifier_colonnes &&  VerifieDiag :
## Petites fonctions aidant a la construction de la fonction Terminal
## Elles vérifient s'il y a un gagnant, et si oui, quel est son symbole
def Verifier_lignes(grille):
    compteur = 0
    for i in range(0, len(grille)):
        for j in range(0, len(grille[i]) - 4):
            compteur = 0
            if grille [i][j] != " ":                     #si la case a un symbole
                for k in range(1, 5):                    # on parcourt les cases suivantes (en ligne)
                    if grille[i][j] == grille[i][j + k]: # si on a le meme symbole
                        compteur += 1                    # on incremente le compteur
                if compteur == 4:                        # si a la fin on a trouvé 4 autres cases identiques
                    return [True, grille[i][j]]          # on renvoie 'true' et le symbole du gagnant
    return [False, " "]

def Verifier_colonnes(grille):
    compteur = 0
    for i in range(0, len(grille)):
        for j in range(0, len(grille[i]) - 4):
            compteur = 0
            if grille [j][i] != " ":
                for k in range(1, 5):
                    if grille[j][i] == grille[j + k][i]:
                        compteur += 1
                if compteur == 4:
                    return [True, grille[j][i]]
    return [False, " "]

def VerifieDiag(liste):
    sys = " "
    sontEgal= False
    for i in range(len(liste)-4):
        sys=liste[i]
        if sys != " ":
            sontEgal= True
            for j in range(5):
                if liste[i+j] != sys:
                    sontEgal= False 
            if sontEgal== True:
                return [sontEgal, sys]
            
    return [sontEgal, sys]

def VerifieDiagTTGrill(Grill):
    res= [False, " "]
    
    for k in range(-10,11):
        l= []
        for i in range (len(Grill)):
            for j in range (len(Grill)):
                if (i-j) == k: 
                    l.append(Grill[i][j])
        res=VerifieDiag(l)
        if res[0] == True:
            return res
    
    if res[0] == False :
        for k in range(4,24):
            l= []
            for i in range (len(Grill)):
                for j in range (len(Grill)):
                    if (i+j) == k: 
                        l.append(Grill[i][j])
            res=VerifieDiag(l)
            if res[0] == True:
                return res
    return res

# Terminal_Test :
## fonction retournant un booléen (true si la partie est finie, false sinon)
## ainsi que le symbole du vainqueur (retourne " " s'il n'y a pas de vainqueur)
def Terminal_Test(grille):
    resultat = Verifier_lignes(grille) #dans le cas où il y a un gagnant
    if resultat[0] == True:
        return [True, resultat[1]]
    resultat = Verifier_colonnes(grille)
    if resultat[0] == True:
        return [True, resultat[1]]
    
    resultat = VerifieDiagTTGrill(grille)
    if resultat[0] == True:
        return [True, resultat[1]]
    
    compteur = 0
    for i in range(0, len(grille[0])): # dans le cas où il n'y a pas de gagnant
        if " " not in grille[i]: #s'il n'y a pas de case vide 
            compteur = compteur + 1 # on incremente le compteur
    if compteur == 15: # si aucune ligne n'a de case vide (toutes les lignes sont completes)
        return [True, " "] # partie finie, aucun gagnant
    
    return [False, " "]

#Utility :
## fonction qui attribue un score à une grille entiere (qui depend du symbole si gagnant)
def Utility(fini,symbole,grille):
    if (fini==True): #jeu fini <=> il y a un gagnant <=> symbole != ' '

        if symbole == "x":
            return 1000
        if symbole == "o": 
            return -1000
        if symbole == " ": 
            return 0
    else: #aucun gagnant mais compteur atteint
        somme_score=0 #somme des scores de toutes les cases
        grille_score = score(grille)
        for i in range(15):
            for j in range(15):
                somme_score+=grille_score[(i,j)] #somme les scores de toutes les cases
        return somme_score
    
    
#%%##############################################################################################################
############################################  Partie 2 <MinMax>  ################################################
#################################################################################################################

# minvalue :
## on considère que l'IA joue x et que le joueur joue o 
## on a appliqué l'idee de profondeur pour ameliorer le resultat de Minimax_Decision
def minvalue(state, profondeur):
    result = Terminal_Test(state);
    if  result[0]==True or profondeur > 3: # si partie finie ou profondeur supérieure à 5
        return Utility(result[0], result[1], state) # calcul du score
    v = 2000000 # infini
    act = Actions(state)
    for a in act : #pour chaque index de case avec le meilleur score
        maxf = maxvalue(Resultat(a, state, "o"), (profondeur + 1)) #appel de maxvalue avec la grille qui possede la possibilité de jeu de "o"
                                                                   #l'IA va considérer que "o" joue bien -> maxvalue
        v = min([v, maxf]) # on attribue la plus petite valeur
    return v

# maxvalue :
## logique inverse de la fonction minvalue
def maxvalue(state, profondeur): 
    result = Terminal_Test(state)
    if  result[0]==True or profondeur > 3 :
        return Utility(result[0], result[1], state)
    v = -2000000 # -infini
    act = Actions(state)
    for a in act :
        minf = minvalue(Resultat(a, state, "x"), (profondeur + 1))
        v = max([v, minf])
    return v

from tqdm import tqdm #barre de progression

# Minimax_Decision :
## on passe en parametre une grille (après que "o" ait joué)
## renvoie la grille après avoir joué
def Minimax_Decision(state):
    actions = Actions(state) #on recupere les actions possibles
    min_actions = []
    for i in tqdm(range(len(actions))):
        min_actions.append(minvalue(Resultat(actions[i], state, "x"), 0)) #appel de minvalue pour chaque possibilité
    maxV = max(min_actions) # on prend le max des valeurs de chaque possibilité
    positionA = min_actions.index(maxV) # on garde la grille ayant le score max
    return actions[positionA] # on retourne cette nouvelle grille

    
#%%###############################################################################################################
#####################################  Partie 3 <MinMax avec Alpha_Beta >  #######################################
##################################################################################################################

# max_value_AB
## version plus optimisée de maxvalue (plus rapide)
def max_value_AB(state, alpha, beta, profondeur):
    result = Terminal_Test(state)
    if  result[0]==True or profondeur > 3:
        return Utility(result[0], result[1], state)
    v = -2000000 # -infini
    act = Actions(state)
    for a in act :
        minf = min_value_AB(Resultat(a, state, "x"), alpha, beta, (profondeur + 1))
        v = max(v, minf)
    if v >= beta: # si v est plus grand que beta, pas besoin de verifier les autres possiblités
        return v
    alpha = max(alpha, v)
    return v

def min_value_AB(state, alpha, beta, profondeur):
    result = Terminal_Test(state);
    if  result[0]==True or profondeur > 3:
        return Utility(result[0], result[1], state)
    v = 2000000 # infini
    act = Actions(state)
    for a in act :
        maxf = max_value_AB(Resultat(a, state, "o"), alpha, beta, (profondeur + 1))
        v = min(v, maxf)
    if v <= alpha:
        return v
    beta = min(beta, v)
    return v

# Alpha_Beta_Search
## application de l'algorithme alpa-beta
## remplace la fonction Minimax_Decision
def Alpha_Beta_Search(state):
    actions = Actions(state)
    alpha = -2000000 # -infini
    beta = 2000000 # +infini
    min_actions = []
    for i in tqdm(range(len(actions))): # barre de progression
        min_actions.append(min_value_AB(Resultat(actions[i], state, "x"), alpha, beta, 0))
    
    maxV = max(min_actions)
    positionA = min_actions.index(maxV)
    return actions[positionA]

#%%##############################################################################################################
###########################################  Partie 4 <Choix du main >  #########################################
#################################################################################################################
import random
def Menu():
    
    choix_algo = input("Choix de l'IA \n1-MinMax\n2-AlphaBeta\n\t==>")

    choix_Qui_commence = input("Qui commence la partie?\n 1 - Le joueur\n 2 - L'IA\n\t==>");
    if int(choix_Qui_commence) == 1:
        print("le joueur a le pion NOIR de le symbole <o> \nl'IA a le pion BLANC le symbole <x>")
        sysQuiCommence = "o" # l'IA commence
        tour = 0 # numéro du tour actuel
    if int(choix_Qui_commence) == 2:
        print("le joueur a le pion BLANC de le symbole <o> \nl'IA a le pion NOIR le symbole <x>")
        sysQuiCommence = "x" 
        tour = 1 # numéro du tour actuel
        # pour permettre de décaler le tour de l'utilisateur
    input("Appuyez sur une touche pour commencer")
    
    grille_ini = initial(15,sysQuiCommence)
    tour = tour + 1 # tour suivant
    for i in range(2):
        Affichage_grille(grille_ini)
        tour_utilisateur = (tour%2 == 0)
        if tour_utilisateur:
            print("\n\nC'est au tour du joueur");
            choix_case = input("\nVeuillez choisir la case (par ex. 'D7'). \nAvec la première lettre en majuscules !\n\t==>")
            choix_case_ligne = ord(choix_case[0]) - 65 # numéro de la case à partir du code ascii
            choix_case_colonne = int(choix_case[:0] + choix_case[1:])-1
            grille_ini[choix_case_ligne][choix_case_colonne] = "o"

        else:
            print("\n\nC'est au tour de l'IA");
            if i == 0 : # 2eme tour (joueur a commencé)
                 x = random.randint(0, 5) # l'IA peut jouer où il veut
                 y = random.randint(0, 5)
            if i == 1 : #3eme tour (IA a commencé)
                x = random.randint(0, 3)
                y = random.randint(0, 3)
            print("le IA a joué au ==>",chr(x+65),str(y+1))
            grille_ini[x][y] = "x"
            
        
        tour = tour + 1
    match_termine = False
    vainqueur = "?"
    while(match_termine == False):

        Affichage_grille(grille_ini)

        tour_utilisateur = (tour%2 == 0)

        if tour_utilisateur:
            print("\n\nC'est au tour du joueur");
            choix_case = input("\nVeuillez choisir la case (par ex. 'D7'). \nAvec la première lettre en majuscules !\n\t==>")
            choix_case_ligne = ord(choix_case[0]) - 65 # numéro de la case à partir du code ascii
            choix_case_colonne = int(choix_case[:0] + choix_case[1:])-1
            grille_ini[choix_case_ligne][choix_case_colonne] = "o"

        else:
            print("\n\nC'est au tour de l'IA");
            print("\nL'IA se met à réfléchir...");

            case_AI = [0,0]
            if int(choix_algo) == 1:
                case_AI = Minimax_Decision(grille_ini) 
            if int(choix_algo) == 2:
                case_AI = Alpha_Beta_Search(grille_ini) 
            print("le IA a joué au ==>",chr(case_AI[0]+ 65),str(case_AI[1]+1))
            grille_ini[case_AI[0]][case_AI[1]] = "x"
            

        result = Terminal_Test(grille_ini)
        match_termine = result[0]
        vainqueur = result[1]
        tour = tour + 1
    Affichage_grille(grille_ini)
    print(vainqueur, end = ' ')
    print("a gagné!!!")

    choix_reco = input("Tapez 1 pour recommencer")
    if int(choix_reco) == 1:
        Menu()


Menu();
        
