# -- coding: utf-8 --
'''
Created on 14 July, 2021

@author: Guillaume Cleuziou
'''
import numpy as np
from random import *

'''
Fonction de création :
_pst : de nb_variable listes de nb_programme
    liste numpy de taille aléatoire entre 3 et 10
_tl :
'''
def creer_liste_de_liste_aleatoire(nb_programme,nb_variable,nb_etiquette):
    i=0
    res_pst = []
    dico_pst = creer_dico_pst(nb_variable)


    res_tl = []
    res_l = np.random.randint(0,nb_etiquette,(nb_programme,))
    print("res_l : ",res_l)

    #Taille choisi aléatoirement
    taille =0

    while i<nb_programme:

        print("i : ",i)

        taille = randint(3,10)

        print("taille : ",taille)

        res_tl.append(taille)

        print("res_tl : ",res_tl)

        j=0

        while j<nb_variable:
            dico_pst[i].append(np.random.randint(0,10,taille))
            j+=1

        i+=1


    return res_pst, res_tl, res_l


def creer_dico_pst(nb_variable):
    i = 0
    res = {}
    while i<nb_variable:
        res[i] = []
        i+=1
    return res
