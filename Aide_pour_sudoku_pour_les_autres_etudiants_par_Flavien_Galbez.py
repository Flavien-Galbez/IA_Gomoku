# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 17:52:42 2019

@author: Flavien
"""
from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from random import randint #servira pour génerer la case aléatoire demandé en seconde partie


dim_case = [3,3]
dim=dim_case[0]*dim_case[1]

def afficher_sudoku(grille, numero_solution):
    #Je mets ici ma fonction d'affichage afin de mettre en évidence l'écriture de l'affichage en Python et avec ortools
    #Cependant plusieurs méthode existe et j'invite à la réécrire
    print("\n La solution n°"+str(numero_solution)+" du sudoku est :")
    print("+"+("-"*dim_case[1]+"+")*dim_case[0])
    for index_ligne in range(dim):
        print('|',end="") #par défault en Python un print renvoie à la ligne (se termine par un "\n") si on ne veut pas que cela soit le cas il faut l'indiquer par un "end=..."
        for index_colonne in range(dim):
            if (grille[index_ligne][index_colonne].Value()!=0): #.Value permet de récupérer la valeur
                print(grille[index_ligne][index_colonne].Value(), end="")
            else:
                print(" ", end="")
            if (index_colonne%dim_case[1]==dim_case[1]-1):
                print('|', end="")
        print()
        if (index_ligne%dim_case[0]==dim_case[0]-1):
            print(("+"+("-"*dim_case[1]+"+")*dim_case[0])*(index_ligne%dim_case[0]==dim_case[0]-1))
        

            
def resolution_avec_saisie_des_cases_dans_le_code():
    solver = pywrapcp.Solver("sudoku_"+str(dim)+"x"+str(dim))
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
    
        #Même logique que précédement ici, plusieurs solutions existent c'est pour ça que je laisse chercher
    
    #On place les cases de la grille en contrainte
    solver.Add(grille[3][0] == 2)
    solver.Add(grille[2][1] == 8)
    solver.Add(grille[4][1] == 5)
    solver.Add(grille[5][1] == 1)
    solver.Add(grille[6][1] == 3)
    solver.Add(grille[1][2] == 6)
    solver.Add(grille[3][2] == 3)
    solver.Add(grille[4][2] == 8)
    solver.Add(grille[7][2] == 2)
    solver.Add(grille[1][3] == 4)
    solver.Add(grille[6][3] == 1)
    solver.Add(grille[8][3] == 8)
    solver.Add(grille[1][4] == 8)
    solver.Add(grille[2][4] == 3)
    solver.Add(grille[4][4] == 4)
    solver.Add(grille[6][4] == 2)
    solver.Add(grille[7][4] == 5)
    solver.Add(grille[0][5] == 7)
    solver.Add(grille[2][5] == 2)
    solver.Add(grille[7][5] == 4)
    solver.Add(grille[2][6] == 7)
    solver.Add(grille[4][6] == 1)
    solver.Add(grille[5][6] == 2)
    solver.Add(grille[7][6] == 6)
    solver.Add(grille[2][7] == 5)
    solver.Add(grille[3][7] == 4)
    solver.Add(grille[4][7] == 6)
    solver.Add(grille[6][7] == 8)
    solver.Add(grille[5][8] == 5)

    #On apelle le solver
    db = solver.Phase([grille[i//dim][i%dim] for i in range(dim*dim)], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    solver.Solve(db)
    afficher_les_differentes_solutions(solver, grille)
    
        
def afficher_les_differentes_solutions(solver, grille):
    nb_solutions = 0
    while solver.NextSolution(): #permet de passer à la grille suivante
        nb_solutions += 1
        afficher_sudoku(grille, nb_solutions)
    print("\n Le nombre de solutions trouvees est :", nb_solutions)
