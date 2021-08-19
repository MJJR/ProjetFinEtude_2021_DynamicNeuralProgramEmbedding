'''
Created on August 14 2021

@author: Mathieu REDOR
'''
import json_util as ju

class TraceVocabulary():

    def __init__(self):
        """
        vocabulary :
        taille_max_nb_variable : La taille maximale de nombre de variables dans les traces traités
        taille_max_pas_exe : La taille maximal de pas dans les traces pour faire un padding plus tard
        """
        super(TraceVocabulary, self).__init__()
        self.vocabulary = {0 : "_Nothing_"}
        self.label = {}
        self.taille_max_nb_variable = 0
        self.taille_max_pas_exe = 0

    """
    verif_valeur(la_valeur)

    On vérifie si la valeur en entrée est déjà dans le dictionnaire
    Si c'est le cas, on retourne la clef (valeur one hot encoding)
    Sinon on ajoute cette nouvelle valeur dans le dictionnaire et
    on retourne la nouvelle entrée (en one hot encoding)
    """
    def verif_valeur(self,la_valeur):
        for cle,valeur_vocabulary in self.vocabulary.items():
            if la_valeur == valeur_vocabulary:
                return cle
        new_entree = len(self.vocabulary)
        self.vocabulary[new_entree] = la_valeur
        return new_entree

    """
    verif_label(etiquette)

    On vérifie si la valeur en entrée est déjà dans le dictionnaire des labels
    Si c'est le cas, on retourne la clef (avec un identifiant)
    Sinon on ajoute cette nouvelle valeur dans le dictionnaire des labels et
    on retourne la nouvelle entrée (avec un identifiant)
    """
    def verif_label(self,etiquette):
        for cle,valeur_label in self.label.items():
            if etiquette == valeur_label:
                return cle
        new_entree = len(self.label)
        self.label[new_entree] = etiquette
        return new_entree

    """
    traiter trace variable
    """
    def traitement_traces_brutes(self,traces_brutes):

        #print("Traces Brutes : \n",traces_brutes)
        nb_pas = len(traces_brutes)

        dico_variables = self.recup_variable_dans_traces(traces_brutes)
        nb_variable = len(dico_variables)

        #On n'Oublie pas de mettre jour les variables max de notre classe
        self.maj_nb_max(nb_variable,nb_pas)

        traces = [[]]*nb_variable
        traces_ohe = []

        #print(dico_variables)

        for index,variable in dico_variables.items():
            traces[index] = []
            for trace in traces_brutes :
                if variable in trace.keys():
                    traces[index].append(trace[variable])
                else :
                    traces[index].append("_Nothing_")
        #print("Traces Traitées : \n",traces)
        #On fait du one hot encoding sur les valeurs de toutes nos listes crées
        for traces_variable in traces :
            traces_ohe.append(self.utiliser_vocabulary_dict(traces_variable))

        #print("TRACES OHE : \n",traces_ohe)
        return traces_ohe,nb_pas

    """
    recup_variable_dans_traces

    return { 0:v1, 1:v2,..., n:v(n-1) }
    """
    def recup_variable_dans_traces(self,traces_brutes):
        liste_variables_traces = {}
        index = 0

        for trace in traces_brutes:
            for variable in trace.keys():
                if variable not in liste_variables_traces.values():
                    liste_variables_traces[index] = variable
                    index +=1

        return liste_variables_traces


    """
    maj taille_max_nb_variable
    """
    def maj_nb_max(self,nb_variable,nb_exe):
        if nb_variable > self.taille_max_nb_variable:
            self.taille_max_nb_variable = nb_variable
        if nb_exe > self.taille_max_pas_exe:
            self.taille_max_pas_exe = nb_exe
        return

    """
    PostTraitement : Padding [taille_max_pas_exe]*[taille_max_nb_variable]
    """
    def post_traitement_traces(self,toutes_les_traces_ohe):
        print("======= POST TRAITEMENT =======")
        avancement = 0
        taille_a_traiter = len(toutes_les_traces_ohe)
        for traces_une_execution in toutes_les_traces_ohe:
            #print(traces_une_execution["traces_ohe"])
            mes_traces = traces_une_execution["traces_ohe"].copy()
            nb_variable_restant = self.taille_max_nb_variable - len(traces_une_execution["traces_ohe"])
            while nb_variable_restant > 0:
                mes_traces.append([0]*traces_une_execution["longueur_traces"])
                nb_variable_restant -= 1
            avancement += 1
            print("Traitement en cours : ", (avancement/taille_a_traiter)*100,"% (",avancement,"/",taille_a_traiter,")")

            traces_une_execution["traces_ohe"] = mes_traces

            print(traces_une_execution["traces_ohe"])
            print("longueur traces = ",len(traces_une_execution["traces_ohe"]))
            print("les traces ont longueur 32 taille_max ? -> ", self.taille_max_nb_variable == len(traces_une_execution["traces_ohe"]))

        return toutes_les_traces_ohe



    """
    utiliser_vocabulary_dict

    @liste_traces_variable_traite : Une liste des traces d'UNE variable
    que l'on va remplacer par du One Hot Encoding grâce au dictionnaire
    de notre classe
    """
    def utiliser_vocabulary_dict(self,liste_traces_variable_traite):
        liste_one_hot_encoding = []
        for trace in liste_traces_variable_traite:
            liste_one_hot_encoding.append(self.verif_valeur(trace))
        return liste_one_hot_encoding


    """
    affiche_etat_vocabulary
    """
    def affiche_etat_vocabulary(self):
        print("NOMBRE MAX DE VARIABLE : ",self.taille_max_nb_variable)
        print("LONGUEUR MAX DES TRACES : ",self.taille_max_pas_exe)
        print("TAILLE VOCABULARY : ", len(self.vocabulary) )
        print("NOMBRE DE LABELS : ", len(self.label) )
