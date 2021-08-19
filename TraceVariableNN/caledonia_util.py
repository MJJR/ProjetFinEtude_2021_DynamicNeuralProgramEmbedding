'''
Created on August 11 2021

@author: Mathieu REDOR

Script utilitaire en python pour utiliser les fichiers Caledonia du projet
'''

'''
grab_funcname_with_exercices_name

Fonction qui permet d'attraper le nom de la fonction dans
le fichier des cas de test à partir de la variable
exercises name des code des élèves

@liste_solutions : la variable contenant le fichier json charger
contenant les cas de test

@exercises_name : l'identifiant de l'exercise de la tentative de l'élève

'''
def grab_funcname_with_exercice_name(liste_code_solutions,exercise_name):
    res = None
    for solution in liste_code_solutions:
        if solution["exo_name"] == exercise_name :
            res = solution["funcname"]
    return res

'''
'''
def grab_entries_fonction(liste_code_solutions,funcname):
    res = None
    for solution in liste_code_solutions:
        if solution["funcname"] == funcname :
            res = solution["entries"]
    return res


def is_black_listed(programme,nb_cas_test):
    res = False
    if programme["user"] == "userdId_38" and programme["exercise_name"] == "d7c83a7fb9b49e28804e55955ad06968" and nb_cas_test == 3 :
        res = True
    elif programme["user"] == "userdId_21" and programme["exercise_name"] == "3355182ef981952e841618c19103ef09" and nb_cas_test in [0,1,2,3,4,5] :
        res = True
    elif programme["user"] == "userdId_15" and programme["exercise_name"] == "864911b08708fc8bae69311a8ddd3da7" and nb_cas_test in [0,1,2,3,4,5,6] :
        res = True
    return res
