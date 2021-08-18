'''
Created on August 5 2021

@author: Mathieu REDOR
'''
#TEST POUR MANIPULER LES TROIS FICHIER JSON
import json
import caledonia_util as cu
import json_util as ju
import tracer

#On ouvre les fichiers json
code_eleves_partie_un = open('NewCaledonia_5690.json',"r")
code_eleves_partie_deux = open('NewCaledonia_1014.json',"r")
code_solutions = open('NewCaledonia_exercises.json',"r")

#On les charges dans ces variables
liste_code_eleves_partie_un = json.load(code_eleves_partie_un)
liste_code_eleves_partie_deux = json.load(code_eleves_partie_deux)
liste_code_solutions = json.load(code_solutions)

#On ouvre notre fichier pour écrire les traces brutes + metadonnées
metadonnees = open('TracesVariableBrutes.json',"w")

#Variables pour le traceur et les traces de variables
traceur = None
les_traces = None
liste_traces = []

#MANIP CODE ELEVES
nb_programme = 0
nb_cas_test = 0
la_fonction = None #Variable pour attraper la fonction du code

for programme in liste_code_eleves_partie_un +liste_code_eleves_partie_deux :



    try:

        print("Programme numéro : ",nb_programme)

        '''
        SI LE PROGRAMME EST INVALIDE AU NIVEAU DE LA SYNTAXE
        ALORS ON L'IGNORE AVEC UNE EXCEPTION
        '''

        print("Identifiant eleve : ",programme["user"])
        #On récupère le nom de la Fonction
        print("Identifiant exercice : ",programme["exercise_name"])
        nom_fonction = cu.grab_funcname_with_exercice_name(liste_code_solutions,programme["exercise_name"])
        print("Nom de la fonction : ",nom_fonction)

        #À AJOUTER À LA FIN DE L'EXEC POUR ATTRAPER LA FONCTION POUR LE RÉEXECUTER
        grab = "\nla_fonction = "+ nom_fonction


        #print(programme["upload"])
        exec(programme["upload"]+grab)
        #TEST POUR EXECUTER SUR CAS DE TEST
        #Attraper les entrées de la fonction et executer
        cas_test = cu.grab_entries_fonction(liste_code_solutions,nom_fonction)

        nb_cas_test=0
        for test in cas_test:
            if cu.is_black_listed(programme,nb_cas_test) :
                print("QUEL HORREUR !!!")
            else:
                traceur = tracer.Tracer()
                #print(test)
                print("numéro du cas de test = ", nb_cas_test)
                #On execute avec le traceur de variables
                les_traces = traceur.get_trace_and_result(la_fonction,*test["items"])
                #print(les_traces[1])
                del traceur

                #RÉCUPÉRER LES TRACES ET L'ÉCRIRE DANS LE FICHIER JSON PRÉVU À CET EFFET
                liste_traces.append(ju.ajouter_metadonnee_old(programme,nb_programme,nb_cas_test,les_traces[1]))

                nb_cas_test += 1


    except SyntaxError :
        print("SyntaxError sur le programme numéro ",nb_programme)
        #l'instruction 'del traceur' mets une erreur comme quoi il n'est pas instancié

    except NameError :
        print("NameError sur le programme numéro ",nb_programme)
        del traceur

    except ValueError :
        print("ValueError sur le programme numéro ",nb_programme)
        del traceur

    except TypeError :
        print("TypeError sur le programme numéro ",nb_programme)
        del traceur

    except tracer.BoucleInfinie :
        print("BoucleInfinie sur le programme numéro ",nb_programme)
        #Pas de suppession du traceur, il n'est pas encore instancié dans ce cas de figure !


    nb_programme +=1

#RÉCUPÉRER LES TRACES ET L'ÉCRIRE DANS LE FICHIER JSON PRÉVU À CET EFFET
ju.traduire_objet_en_json(liste_traces)
print("Taille de metadonne = ",len(liste_traces))

json.dump(liste_traces,metadonnees,cls=ju.PythonObjectEncoder)

"""
etape = 0
avancement = ""
for la_trace in liste_traces:
    avancement = 100*etape/len(liste_traces)
    print("Avancement écriture dans fichier json : ",avancement,"%")
    json.dump(la_trace,metadonnees,cls=ju.PythonObjectEncoder)
    etape+=1
"""

# FERMER LES FICHIERS C'EST IMPORTANT =)
code_eleves_partie_un.close()
code_eleves_partie_deux.close()
code_solutions.close()
metadonnees.close()
