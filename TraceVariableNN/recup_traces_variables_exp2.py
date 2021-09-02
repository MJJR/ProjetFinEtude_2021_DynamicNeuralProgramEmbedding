'''
Created on August 14 2021

@author: Mathieu REDOR
'''

import json
import caledonia_util as cu
import json_util as ju
import tracer
import vocabulaire_util as vu

"""
TESTONS UN TRUC
"""
test_dico = set()
test_nb_pass = 0

#Objet qui permettra de traité les variables brutes
trace_vocab = vu.TraceVocabulary()

#On ouvre les fichiers json
code_eleves = open('NewCaledonia_5690.json',"r")
code_solutions = open('NewCaledonia_exercises_exp2.json',"r")

#On les charges dans ces variables
liste_code_eleves = json.load(code_eleves)
liste_code_solutions = json.load(code_solutions)

#On ouvre notre fichier pour écrire les traces brutes + metadonnées
metadonnees = open('TracesVariable_exp2.json',"w")

#Variables pour le traceur et les traces de variables
traceur = None
les_traces = None
liste_traces = []

#MANIP CODE ELEVES
nb_programme = 0
nb_cas_test = 0
la_fonction = None #Variable pour attraper la fonction du code


for programme in liste_code_eleves :

    """
    TEST
    """
    test_dico.add(programme["exercise_name"])

    try:
        print("Programme numéro : ",nb_programme)
        '''
        SI LE PROGRAMME EST INVALIDE AU NIVEAU DE LA SYNTAXE
        ALORS ON L'IGNORE AVEC UNE EXCEPTION
        '''
        #print("Identifiant eleve : ",programme["user"])
        #On récupère le nom de la Fonction
        #print("Identifiant exercice : ",programme["exercise_name"])
        nom_fonction = cu.grab_funcname_with_exercice_name(liste_code_solutions,programme["exercise_name"])
        #print("Nom de la fonction : ",nom_fonction)
        #À AJOUTER À LA FIN DE L'EXEC POUR ATTRAPER LA FONCTION POUR LE RÉEXECUTER
        grab = "\nla_fonction = "+ nom_fonction
        #print(programme["upload"])
        exec(programme["upload"]+grab)
        #TEST POUR EXECUTER SUR CAS DE TEST
        #Attraper les entrées de la fonction et executer
        cas_test = cu.grab_entries_fonction(liste_code_solutions,programme["exercise_name"])
        cas_test_exp2 = cu.grab_entries_fonction_exp2(liste_code_solutions,programme["exercise_name"])
        nb_cas_test=0
        #On mettra tous les executions des codes avec les cas de test d'origine en training, et le reste en test
        nb_cas_test_training = len(cas_test)
        for test in cas_test+cas_test_exp2:
            try :

                if cu.is_black_listed(programme,nb_cas_test) :
                    print("QUEL HORREUR !!!")
                    print(programme["user"])
                    test_nb_pass+=1
                else:
                    #print(programme["upload"])
                    traceur = tracer.Tracer()
                    #print(test)
                    print("numéro du cas de test = ", nb_cas_test)
                    """
                    /!\ Les entrées sont soit directement dans une liste, soit dans un dictionnaire de type {"__tuple__":xxx,"items":xxx}
                    """
                    if isinstance(test,dict):
                        #print('*test["items"] = ', *test["items"])
                        les_traces = traceur.get_trace_and_result(la_fonction,*test["items"])
                    else :
                        #print("test = ",test)
                        #print("TYPE DE TEST : ",type(test))
                        les_traces = traceur.get_trace_and_result(la_fonction,test)
                    #print(les_traces[1])
                    del traceur

                    #RÉCUPÉRER LES TRACES ET L'ÉCRIRE DANS LE FICHIER JSON PRÉVU À CET EFFET
                    if les_traces[1] != []:
                        liste_traces.append(ju.ajouter_metadonnee_exp2(programme,nb_programme,nb_cas_test,les_traces[1],trace_vocab,nb_cas_test<nb_cas_test_training))
                    else :
                        print("WARNING il y a une liste vide !!!")
                        print("Programme ID : ",programme["exercise_name"])
                        print(programme["upload"])
                        print("numéro du cas de test = ", nb_cas_test)
                        print("test = ",test)
                        test_nb_pass+=1
                nb_cas_test += 1

            except tracer.BoucleInfinie :
                print("BoucleInfinie sur le programme numéro ",nb_programme)
                #Pas de suppession du traceur, il n'est pas encore instancié dans ce cas de figure !
                test_nb_pass+=1
            except ValueError :
                print("ValueError sur le programme numéro ",nb_programme)
                del traceur
                test_nb_pass+=1

    #ERREUR DE SYNTAX SUR LE CODE => INUTILISABLE
    except SyntaxError :
        print("SyntaxError sur le programme numéro ",nb_programme)
        #l'instruction 'del traceur' mets une erreur comme quoi il n'est pas instancié
    #except NameError :
        #print("NameError sur le programme numéro ",nb_programme)
        #del traceur
    #except ValueError :
        #print("ValueError sur le programme numéro ",nb_programme)
        #del traceur
    #except TypeError :
        #print("TypeError sur le programme numéro ",nb_programme)
        #del traceur
    except tracer.BoucleInfinie :
        print("BoucleInfinie sur le programme numéro ",nb_programme)
        #Pas de suppession du traceur, il n'est pas encore instancié dans ce cas de figure !
    #print("Programme n°",nb_programme," OK")
    nb_programme +=1

#RÉCUPÉRER LES TRACES ET L'ÉCRIRE DANS LE FICHIER JSON PRÉVU À CET EFFET
liste_traces = trace_vocab.post_traitement_traces(liste_traces)

print("écriture dans le fichier json")
json.dump(liste_traces,metadonnees)


# FERMER LES FICHIERS C'EST IMPORTANT =)
code_eleves.close()
code_solutions.close()
metadonnees.close()

#RESUME
print("Taille de metadonne = ",len(liste_traces))
print("Taille test_dico = ",len(test_dico))
print("Nb code ignoré = ",test_nb_pass)
trace_vocab.affiche_etat_vocabulary()
