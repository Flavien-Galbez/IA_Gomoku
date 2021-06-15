"""
Created on Tue Apr 16 13:43:09 2019

@author: Flavien
"""


import numpy as np
import random

#profondeur = 3 #Le calcul avec une profondeur 3 est plus rapide mais  moins précis donc l'IA a plus de chance de perdre
profondeur = 4 #Le calcul peut être extrememment long avec une profondeur 4 mais il est nettement meilleur que avec une profondeur de 3

# Permet d'obtenir le tableau des actions disponibles
def actionsJoueur(tab):
    result=[[False for i in range(len(tab[0]))] for j in range(len(tab[1]))]
    for i in range(len(tab[0])):
        for j in range(len(tab[1])):
            if(tab[i][j]==0) :
                result[i][j]=True
    return result

# Permet de réduire le nombre de calcul en inspectant seulement les voisins des cases déjà remplies
def actions(tab):
    result=[[False for i in range(len(tab[0]))] for j in range(len(tab[1]))]
    for i in range(len(tab[0])):
        for j in range(len(tab[1])):
            if(tab[i][j]==0) :
                if(not result[i][j]) :
                    for Voisin_ligne in range(i-1,i+2): 
                        for Voisin_colonne in range(j-1,j+2):
                            if (Voisin_ligne>=0 and Voisin_ligne<len(tab[0]) and Voisin_colonne>=0 and Voisin_colonne<len(tab[1])):
                                if(tab[Voisin_ligne][Voisin_colonne]!=0): 
                                    result[i][j] = True                              
    return result


# Permet de tester si le jeu est terminé et donne une valeur selon le gagnant +1/-1 ou 0 si égalité ou non terminé
def TerminalTest(tab):
    #Retourne cela si non terminal
    result= False
    valeur_res=0
    
    # Victoire avec les colonnes ?
    val=0
    j=0
    while (j<len(tab[1]) and result==False):
        i=0
        compteur=0
        while (i<len(tab[0]) and result==False):
            if(tab[i][j]!=0):
                if(val!=tab[i][j]):
                    val=tab[i][j]
                    compteur=1
                else:
                    compteur+=1
                if(compteur>=5):
                    result=True
                    valeur_res=val
            i+=1
        j+=1
           
    # Victoire avec les lignes ?
    val=0
    i=0
    while (i<len(tab[0]) and result==False):
        j=0
        compteur=0
        while (j<len(tab[1]) and result==False):
            if(tab[i][j]!=0):
                if(val!=tab[i][j]):
                    val=tab[i][j]
                    compteur=1
                else:
                    compteur+=1
                if(compteur>=5):
                    result=True
                    valeur_res=val
            j+=1
        i+=1
    
    # Victoire avec la première diagonale ?
    i=0
    while(i<len(tab[0])-5 and result==False):
        j=0
        while(j<len(tab[0])-5 and result==False):
            if(tab[i][j]==tab[i+1][j+1] and tab[i][j]==tab[i+2][j+2] and tab[i][j]==tab[i+3][j+3] and tab[i][j]==tab[i+4][j+4] and tab[i][j]!=0):
                result=True
                valeur_res=tab[i][j]
            j+=1
        i+=1
        
    # Victoire avec la seconde diagonale ? 
    i=4
    while(i<len(tab[0]) and result==False):
        j=0
        while(j<len(tab[0])-5 and result==False):
            if(tab[i][j]==tab[i-1][j+1] and tab[i][j]==tab[i-2][j+2] and tab[i][j]==tab[i-3][j+3] and tab[i][j]==tab[i-4][j+4] and tab[i][j]!=0):
                result=True
                valeur_res=tab[i][j]
            j+=1
        i+=1
        
    #Cas d'égalité
    if(result==False):
        test=True
        i=0
        while(i<len(tab[0]) and test==True):
            j=0
            while (j<len(tab[1]) and test==True):
                if (tab[i][j]==0): test=False
                j+=1
            i+=1
        if test==True: result=True
        
    return ([result,valeur_res])


def heuristic(tab):
    resultat=0
    if (TerminalTest(tab)[0]): #En cas de victoire on renvoit une heuristique maximale/minimale
        resultat=10000000000000*TerminalTest(tab)[1]
    else:
    #Colonne
        for j in range (0,len(tab[1])):
            for i in range (0,len(tab[0])):
                if(tab[i][j]!=0):
                    val=tab[i][j]
                    compteurprec=0
                    compteursuiv=0
                    chaineprec=0
                    chainesuiv=0
                    test_chaine=True
                    victoire_possible=0
                    for parcours in range(0,5): #On regarde les cases apres la case courante
                        if(i+parcours<len(tab[0])):
                            victoire_possible+=1
                            if(tab[i+parcours][j]==val):
                                compteursuiv+=1 #On augmente la "dangerosité" de la case s'il y a un pion de la même couleur sur le parcours
                                if(test_chaine==True):
                                    chainesuiv+=1
                            elif(tab[i+parcours][j]!=0):
                                victoire_possible-=1 #On s'arrete si on rencontre une case possedant un pion d'une autre couleur
                                break
                            else:
                                test_chaine=False
                    test_chaine=True
                    victoire_possible-=1
                    for parcours in range(0,5): #On regarde les cases avant la case courante
                        if(i-parcours>=0):
                            victoire_possible+=1
                            if(tab[i-parcours][j]==val):
                                compteurprec+=1
                                if(test_chaine==True):
                                    chaineprec+=1
                            elif(tab[i-parcours][j]!=0):
                                victoire_possible-=1
                                break
                            else:
                                test_chaine=False
                        
                    if(victoire_possible<5): #On ne prends pas en compte l'alignement de cette case s'il n'est pas possible d'aboutir sur un groupe de 5
                        compteurprec=0
                        compteursuiv=0
                
                    if(val==1):
                        if(compteursuiv!=0):
                            resultat+= 100**(chainesuiv-2)+compteursuiv-2
                        if(compteurprec!=0):
                            resultat+= 100**(chaineprec-2)+compteurprec-2
                    if(val==-1):
                        if(compteursuiv!=0):
                            resultat-= 200**(chainesuiv-2)+compteursuiv-2
                        if(compteurprec!=0):
                            resultat-= 200**(chaineprec-2)+compteurprec-2
                
    #Ligne
    #Même principe que pour les colonnes
        for i in range (0,len(tab[0])):
            for j in range (0,len(tab[1])):
                if(tab[i][j]!=0):
                    val=tab[i][j]
                    compteurprec=0
                    compteursuiv=0
                    chaineprec=0
                    chainesuiv=0
                    test_chaine=True
                    victoire_possible=0
                    for parcours in range(0,5):
                        if(j+parcours<len(tab[1])):
                            victoire_possible+=1
                            if(tab[i][j+parcours]==val):
                                compteursuiv+=1
                                if(test_chaine==True):
                                    chainesuiv+=1
                            elif(tab[i][j+parcours]!=0):
                                victoire_possible-=1
                                break
                            else:
                                test_chaine=False
                    test_chaine=True
                    victoire_possible-=1
                    for parcours in range(0,5):
                        if(j-parcours>=0):
                            victoire_possible+=1
                            if(tab[i][j-parcours]==val):
                                compteurprec+=1
                                if(test_chaine==True):
                                    chaineprec+=1
                            elif(tab[i][j-parcours]!=0):
                                victoire_possible-=1
                                break
                            else:
                                test_chaine=False
                        
                    if(victoire_possible<5):
                        compteurprec=0
                        compteursuiv=0
                
                    if(val==1):
                        if(compteursuiv!=0):
                            resultat+= 100**(chainesuiv-1)+compteursuiv-2
                        if(compteurprec!=0):
                            resultat+= 100**(chaineprec-1)+compteurprec-2
                    if(val==-1):
                        if(compteursuiv!=0):
                            resultat-= 200**(chainesuiv-1)+compteursuiv-2
                        if(compteurprec!=0):
                            resultat-= 200*(chaineprec-1)+compteurprec-2
   # Première diagonnale 
   # Même principe que précédement
        for i in range (0,len(tab[0])):
            for j in range (0,len(tab[1])):
                val=tab[i][j]
                compteurprec=0
                compteursuiv=0
                chaineprec=0
                chainesuiv=0
                test_chaine=True
                victoire_possible=0
                for parcours in range(0,5):
                    if(i+parcours<len(tab[0]) and j+parcours<len(tab[1])):
                        victoire_possible+=1
                        if(tab[i+parcours][j+parcours]==val):
                            compteursuiv+=1
                            if(test_chaine==True):
                                chainesuiv+=1
                        elif(tab[i+parcours][j+parcours]!=0):
                            victoire_possible-=1
                            break
                        else:
                            test_chaine=False
                test_chaine=True
                victoire_possible-=1
                for parcours in range(0,5):
                    if(i-parcours>=0 and j-parcours>=0):
                        victoire_possible+=1
                        if(tab[i-parcours][j-parcours]==val):
                            compteurprec+=1
                            if(test_chaine==True):
                                chaineprec+=1
                        elif(tab[i-parcours][j-parcours]!=0):
                            victoire_possible-=1
                            break
                        else:
                            test_chaine=False
                    
                if(victoire_possible<5):
                    compteurprec=0
                    compteursuiv=0
                
                if(val==1):
                    if(compteursuiv!=0):
                        resultat+= 100**(chainesuiv-1)+compteursuiv-2
                    if(compteurprec!=0):
                        resultat+= 100**(chaineprec-1)+compteurprec-2
                if(val==-1):
                    if(compteursuiv!=0):
                        resultat-= 200**(chainesuiv-1)+compteursuiv-2
                    if(compteurprec!=0):
                        resultat-= 200**(chaineprec-1)+compteurprec-2
                        
    # Deuxième diagonnale 
    # Même principe que précédement
        for i in range (0,len(tab[0])):
            for j in range (0,len(tab[1])):
                val=tab[i][j]
                compteurprec=0
                compteursuiv=0
                chaineprec=0
                chainesuiv=0
                test_chaine=True
                victoire_possible=0
                for parcours in range(0,5):
                    if(i+parcours<len(tab[0]) and j-parcours>=0):
                        victoire_possible+=1
                        if(tab[i+parcours][j-parcours]==val):
                            compteursuiv+=1
                            if(test_chaine==True):
                                chainesuiv+=1
                        elif(tab[i+parcours][j-parcours]!=0):
                            victoire_possible-=1
                            break
                        else:
                            test_chaine=False
                test_chaine=True
                victoire_possible-=1
                for parcours in range(0,5):
                    if(i-parcours>=0 and j+parcours<len(tab[1])):
                        victoire_possible+=1
                        if(tab[i-parcours][j+parcours]==val):
                            compteurprec+=1
                            if(test_chaine==True):
                                chaineprec+=1
                        elif(tab[i-parcours][j+parcours]!=0):
                            victoire_possible-=1
                            break
                        else:
                            test_chaine=False
                    
                if(victoire_possible<5):
                    compteurprec=0
                    compteursuiv=0
                
                if(val==1):
                    if(compteursuiv!=0):
                        resultat+= 100**(chainesuiv-1)+compteursuiv-2
                    if(compteurprec!=0):
                        resultat+= 100**(chaineprec-1)+compteurprec-2
                if(val==-1):
                    if(compteursuiv!=0):
                        resultat-= 200**(chainesuiv-1)+compteursuiv-2
                    if(compteurprec!=0):
                        resultat-= 200**(chaineprec-1)+compteurprec-2
                        
    return resultat

#Algorithme de MinMax
def minmax(tab,depth,alpha,beta):
    bestMoves=[]
    bestScore=-np.inf #Permet d'avoir un bestScore cohérent avec un premier bestScore > à cette valleur d'initialisation
    position_possible=actions(tab)
    for i in range(len(tab[0])):
        for j in range(len(tab[1])):
            if(position_possible[i][j]):
                tab[i][j]=1
                mScore=MIN(tab,depth-1,alpha,beta)
                #print('i: '+str(chr(ord('A')+i))+' j: '+str(j+1)+' | score: '+str(mScore)) #Permet de connaitre le score par case
                if(mScore==bestScore):
                    bestMoves.append([i,j]) #On rajoute à la liste la position en cas d'égalité avec le BestScore
                elif(mScore>bestScore):
                    bestMoves[:]=[] #On vide la liste
                    bestMoves.append([i,j]) #On lui apprend la nouvelle position
                    bestScore=mScore   #On met à jour le bestScore       
                tab[i][j]=0
    alea=random.randint(0,len(bestMoves)-1)
    tab[bestMoves[alea][0]][bestMoves[alea][1]]=1
    print('Choix de l\'IA : '+ str(chr(ord('A')+bestMoves[alea][0]))+str(bestMoves[alea][1]+1))

# Fonction de maximisation
def MAX(tab,depth,alpha,beta):
    r=TerminalTest(tab)
    if (r[0]): return r[1]
    elif (depth==0) :return heuristic(tab)
    else :
        bestScore=-np.inf #Permet d'avoir un besrScore cohérent avec un premier bestScore > à cette valleur d'initialisation
        pos=actions(tab)
        for i in range(len(tab[0])):
            for j in range(len(tab[1])):
                if(pos[i][j]):
                    tab[i][j]=1
                    mScore=MIN(tab,depth-1,alpha,beta)
                    if(mScore>bestScore):
                        bestScore=mScore
                        alpha=max(alpha,mScore)
                    tab[i][j]=0
                    if alpha>=beta : break
        return bestScore

# Fonction de minimalisation
def MIN(tab,depth,alpha,beta):
    r=TerminalTest(tab)
    if (r[0]): return r[1]
    elif (depth==0) :return heuristic(tab)
    else :
        worstScore=np.inf #Permet d'avoir un worstScore cohérent avec un premier worstScore < à cette valleur d'initialisation
        pos=actions(tab)
        for i in range(len(tab[0])):
            for j in range(len(tab[1])):
                if(pos[i][j]):
                    tab[i][j]=-1
                    mScore=MAX(tab,depth-1,alpha,beta)
                    if(mScore<worstScore):
                        worstScore=mScore
                        beta=min(beta,mScore)
                    tab[i][j]=0
                    if alpha>=beta : break
        return worstScore
                    
# Permet à l'utilisateur de jouer son coup en vérifiant si la case est libre (la saisie est sécurisée)
def tourJoueur(tab,debut):
    i=-1
    j=-1
    action_possible=actionsJoueur(tab)
    valide = False
    while(valide == False):
        while(i<0 or i>=len(tab[0]) or j<0 or j>=len(tab[1]) or (debut and ((i>3 and i<11))and(j>3 and j<11))):
            try:
                i=int(ord(input("Entrer la lettre de ligne à jouer (A à O) : ")))-65
            except :
                i=-1
            try :
                j= int(input("Entrer le numero de colonne à jouer (1 à 15) : "))-1
            except :
                j=-1
        valide = action_possible[i][j]
        if (valide): tab[i][j]=-1
        else :
            i=-1
            j=-1
    return tab

# Affichage de la grille du gomoku
def AfficherGrille(tab): 
    print()
    print("     1 2 3 4 5 6 7 8 9 10 ...... 15 ")
    print("    -------------------------------")
    for i in range(len(tab[0])):
        print (chr(ord('A')+i), end='')
        print (" - ", end='|')
        for j in range(len(tab[::][0])):
            if(tab[i][j])==1: print('X',end='')
            elif(tab[i][j])==-1 : print('O',end='')
            else : print('.',end='')
            print('|',end='')
        print()
    print("    -------------------------------\n")
    
#Programme du jeu
def jeuGomoku():
    
    tab=[[0 for _ in range(15)] for _ in range(15)]
    
    #demande qui commence en premier
    premier=''
    while(not (premier=='1' or premier=='0')): premier=input("Voulez vous commencer ?\n 0-NON\n 1-OUI\n")
    AfficherGrille(tab)
    
    #tour 1 joueur 1
    if premier=='1':tab[7][7]=-1
    else :tab[7][7]=1
    AfficherGrille(tab)
    
    #tour 1 joueur 2
    if premier=='1':
        minmax(tab,profondeur,-np.inf,np.inf)
    else : tab=tourJoueur(tab,False)
    AfficherGrille(tab)
    
    #tour 2 joueur 1
    if premier=='1': tab=tourJoueur(tab,True) # le seul cas où on mettra 'True' dans cette fonction, cela empeche le joueur de placer dans le carrée de 7 cases autour du millieu
    else: 
        ialea=-1 #On choisit aleatoirement la position pour le deuxième tour de l'IA quand elle joue en première en respectant les règles
        jalea=-1
        while(((ialea>3 and ialea<11)and(jalea>3 and jalea<11)) or tab[ialea][jalea]!=0):
            ialea=random.randint(0,len(tab[0])-1)
            jalea=random.randint(0,len(tab[1])-1)
        tab[ialea][jalea]=1
    AfficherGrille(tab)
    
    term=[False,0]
    while(term[0]==False) :
        #Tour joueur s'il commence en deuxième
        if premier=='0' :
            tab=tourJoueur(tab,False)
            AfficherGrille(tab)
            term=TerminalTest(tab)
        if term[0] : break
        #Tour IA
        print(" L'IA est en train de choisir son coup ...\n")
        minmax(tab,profondeur,-np.inf,np.inf)
        AfficherGrille(tab)
        term=TerminalTest(tab)
        if term[0] : break
        #Tour joueur s'il commence en premier
        if premier=='1' :
            tab=tourJoueur(tab,False)
            AfficherGrille(tab)        
    if(term[1]==1) : print("Victoire de l'IA !")
    elif(term[1]==-1) : print("Victoire de l'humain !") 
    else : print("Egalité !")
    
jeuGomoku()

