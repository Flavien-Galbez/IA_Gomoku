# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:33:31 2019

@author: Flavien
"""

from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from random import randint


dim_case = [3,3]
dim=dim_case[0]*dim_case[1]

def afficher_sudoku(grille, numero_solution):
    print("\n La solution n°"+str(numero_solution)+" du sudoku est :")
    print("+"+("-"*dim_case[1]+"+")*dim_case[0])
    for index_ligne in range(dim):
        print('|',end="")
        for index_colonne in range(dim):
            if (grille[index_ligne][index_colonne].Value()!=0):
                print(grille[index_ligne][index_colonne].Value(), end="")
            else:
                print(" ", end="")
            if (index_colonne%dim_case[1]==dim_case[1]-1):
                print('|', end="")
        print()
        if (index_ligne%dim_case[0]==dim_case[0]-1):
            print(("+"+("-"*dim_case[1]+"+")*dim_case[0])*(index_ligne%dim_case[0]==dim_case[0]-1))
        
def afficher_grille_depart(grille):
    print("\n La grille de départ etait :")
    print("+"+("-"*dim_case[1]+"+")*dim_case[0])
    for index_ligne in range(dim):
        print('|',end="")
        for index_colonne in range(dim):
            if (grille[index_ligne][index_colonne]!=0):
                print(grille[index_ligne][index_colonne], end="")
            else:
                print(" ", end="")
            if (index_colonne%dim_case[1]==dim_case[1]-1):
                print('|', end="")
        print()
        if (index_ligne%dim_case[0]==dim_case[0]-1):
            print(("+"+("-"*dim_case[1]+"+")*dim_case[0])*(index_ligne%dim_case[0]==dim_case[0]-1))
            
def resolution_avec_saisie_des_cases_dans_le_code():
    solver = pywrapcp.Solver("sudoku_"+str(dim)+"x"+str(dim)+"avec_saisie_dans_le_code")
    # On code la grille de départ dans le dur, un zéro correspond à une case vide
    grille_depart = [
                    [0,2,0,0,5,3,0,0,0],
                    [0,7,0,0,0,2,0,4,0],
                    [8,0,6,0,0,0,0,0,0],
                    [0,4,1,0,0,0,0,0,2],
                    [0,0,0,5,0,7,0,0,0],
                    [9,0,0,0,0,0,8,1,0],
                    [0,0,0,0,0,0,1,0,4],
                    [0,1,0,3,0,0,0,2,0],
                    [0,0,0,8,9,0,0,6,0]
                    ]
    # On crée les variables
    grille = [[0 for i in range(dim)] for j in range(dim)]
    for index_ligne in range(dim):
        for index_colonne in range(dim):
            grille[index_ligne][index_colonne] = solver.IntVar(1, dim, "index_ligne"+str(index_ligne)+"index_colonne"+str(index_colonne))
    # On crée les contraintes
    #  2 fois le meme nombre sur une meme ligne
    for index_ligne in range(dim):
        for index_colonne1 in range(dim):
            for index_colonne2 in range(index_colonne1+1,dim):
                solver.Add(grille[index_ligne][index_colonne1] != grille[index_ligne][index_colonne2])
    #pas 2 fois le meme nombre sur une meme colonne
    for index_colonne in range(dim):
        for index_ligne1 in range(dim):
            for index_ligne2 in range(index_ligne1+1,dim):
                solver.Add(grille[index_ligne1][index_colonne] != grille[index_ligne2][index_colonne])
    #pas 2 fois le meme nombre dans une meme case
    for index_ligne in range(0,dim):
        for index_colonne in range(0,dim):
            for index_ligne_parcour in range((index_ligne//dim_case[0])*dim_case[0],((index_ligne//dim_case[0])+1)*dim_case[0]):
                for index_colonne_parcour in range((index_colonne//dim_case[1])*dim_case[1],((index_colonne//dim_case[1])+1)*dim_case[1]):
                    if(index_ligne_parcour!=index_ligne or index_colonne_parcour != index_colonne) :
                        solver.Add(grille[index_ligne_parcour][index_colonne_parcour]!=grille[index_ligne][index_colonne])
    #On place les cases de la grille en contrainte
    for index_ligne in range (0,dim):
        for index_colonne in range (0,dim):
            if (grille_depart[index_ligne][index_colonne]!=0):
                solver.Add(grille[index_ligne][index_colonne]==grille_depart[index_ligne][index_colonne])
    #On apelle le solver
    db = solver.Phase([grille[i//dim][i%dim] for i in range(dim*dim)], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    solver.Solve(db)
    if(afficher_les_differentes_solutions(solver, grille)==0):
        print("Aucune solution n'a été trouvee")
   
def saisir_difficulte ():
    print("Saisir la difficulte (nombre entre 1 et 5) :\n  1 - débutant\n  2 - facile\n  3 - moyen\n  4 - difficile\n  5 - tres difficile")
    difficulte=input()
    if (difficulte=="1"):
        return 50
    if (difficulte=="2"):
        return 40
    if (difficulte=="3"):
        return 33
    if (difficulte=="4"):
        return 26
    if (difficulte=="5"):
        return 17
    return saisir_difficulte()

def saisir_aboutissement ():
    print("Saisir si vous souhaitez que le programme s'arrete seulement s'il rencontre un sudoku resolvable (0 ou 1) :\n 0 - NON\n 1 - OUI")
    print("Attention ! Generer un sudoku aléatoirement résolvable pour les difficultés facile et débutant est difficile car très improbable et aboutira souvent sur un plantage")
    resolvable=input()
    if (resolvable=="0"):
        return False
    if (resolvable=="1"):
        return True
    return saisir_aboutissement()
    
def resolution_avec_saisie_des_cases_aleatoirement(nbcasesdifficulte,resolvable):
    solver = pywrapcp.Solver("sudoku_"+str(dim)+"x"+str(dim)+"avec_saisie_aleatoire")
    # On crée les variables
    grille = [[0 for i in range(dim)] for j in range(dim)]
    grille_depart = [[0 for i in range(dim)] for j in range(dim)]
    for index_ligne in range(dim):
        for index_colonne in range(dim):
            grille[index_ligne][index_colonne] = solver.IntVar(1, dim, "index_ligne"+str(index_ligne)+"index_colonne"+str(index_colonne))
    # On crée les contraintes
    #  2 fois le meme nombre sur une meme ligne
    for index_ligne in range(dim):
        for index_colonne1 in range(dim):
            for index_colonne2 in range(index_colonne1+1,dim):
                solver.Add(grille[index_ligne][index_colonne1] != grille[index_ligne][index_colonne2])
    #pas 2 fois le meme nombre sur une meme colonne
    for index_colonne in range(dim):
        for index_ligne1 in range(dim):
            for index_ligne2 in range(index_ligne1+1,dim):
                solver.Add(grille[index_ligne1][index_colonne] != grille[index_ligne2][index_colonne])
    #pas 2 fois le meme nombre dans une meme case
    for index_ligne in range(0,dim):
        for index_colonne in range(0,dim):
            for index_ligne_parcour in range((index_ligne//dim_case[0])*dim_case[0],((index_ligne//dim_case[0])+1)*dim_case[0]):
                for index_colonne_parcour in range((index_colonne//dim_case[1])*dim_case[1],((index_colonne//dim_case[1])+1)*dim_case[1]):
                    if(index_ligne_parcour!=index_ligne or index_colonne_parcour != index_colonne) :
                        solver.Add(grille[index_ligne_parcour][index_colonne_parcour]!=grille[index_ligne][index_colonne])
    #On place les cases de la grille en contrainte
    nbcasesremplies = 0
    while (nbcasesremplies <= nbcasesdifficulte):
        index_ligne_alea=randint(0,dim-1)
        index_colonne_alea=randint(0,dim-1)
        valeur_alea=randint(1,dim)
        if (case_valable(valeur_alea,index_ligne_alea,index_colonne_alea,grille_depart)):
            grille_depart[index_ligne_alea][index_colonne_alea]=valeur_alea                 #On rajoute la valeur dans la grille de départ
            solver.Add(grille[index_ligne_alea][index_colonne_alea]==valeur_alea)           #Et on la rajoute comme contrainte
            nbcasesremplies+=1
    #On appelle le solver
    db = solver.Phase([grille[i//dim][i%dim] for i in range(dim*dim)], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    solver.Solve(db)
    nb_solution = afficher_les_differentes_solutions(solver, grille)
    if (nb_solution==0 and resolvable==True):
        return resolution_avec_saisie_des_cases_aleatoirement(nbcasesdifficulte,resolvable)
    else:
        if (nb_solution==0):
            print("Aucune solution n'a ete trouvee")
        afficher_grille_depart(grille_depart)

def case_valable (valeur,index_ligne,index_colonne, grille) :
	#Permet de tester si la case est valable pour la création du sudoku (respect des règles)
    if grille[index_ligne][index_colonne]!=0:
        return False
    for index in range (0,9):
        if grille[index_ligne][index]==valeur or grille[index][index_colonne]==valeur:
            return False
        
    for index_ligne_parcour in range((index_ligne//dim_case[0])*dim_case[0],((index_ligne//dim_case[0])+1)*dim_case[0]):
        for index_colonne_parcour in range((index_colonne//dim_case[1])*dim_case[1],((index_colonne//dim_case[1])+1)*dim_case[1]):
            if grille[index_ligne_parcour][index_colonne_parcour]==valeur:
                return False      
    return True
        
def afficher_les_differentes_solutions(solver, grille):
    nb_solutions = 0
    while solver.NextSolution():
        nb_solutions += 1
        afficher_sudoku(grille, nb_solutions)
    if nb_solutions!=0:
        print("\n Le nombre de solutions trouvees est :", nb_solutions)
    return nb_solutions

def trouver_un_sudoku_adapte():
    difficulte=saisir_difficulte()
    #générer un sudoku aléatoirement pour les difficultés facile et débutant qui est résolvable est difficile car très improbable et aboutira sur un plantage
    #en difficulté facile le programme a réussi m'en générer un résolvable au bout de 7 essais
    resolvable = saisir_aboutissement() #si vrai le programe ne s'arretera pas avant d'avoir créer une grille résolvable
    resolution_avec_saisie_des_cases_aleatoirement(difficulte,resolvable)

#Méthode pour résoudre avec saisie dans le code
resolution_avec_saisie_des_cases_dans_le_code()
#Méthode pour trouver un sudoku résolvable ou non généré aléatoirement
trouver_un_sudoku_adapte()
    