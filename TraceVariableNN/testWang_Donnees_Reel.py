# -- coding: utf-8 --
'''
Created on 15 August, 2021

@author: Mathieu Redor
'''
import tensorflow as tf
# import du code de wang
import Training as network
import json
'''
TEST AVEC DONNES REEL
'''
print("TEST AVEC DONNES REEL")

print("Ouverture du fichier json")
fichier_donnees = open('TracesVariable.json',"r")
print("Chargement du fichier json")
donnees = json.load(fichier_donnees)
fichier_donnees.close()
print("Chargement du fichier json terminé")

training_pst = [] #Donnees des variables
training_tl = [] #tl pour Trace Length
training_label = [] #Une étiquette par programme

test_pst = [] #Donnees des variables
test_tl = [] #tl pour Trace Length
test_label = [] #Une étiquette par programme



print("Triage entre donnée d'entrainement et donnée de test")
for donnee in donnees :

    #print(donnee["traces_ohe"])

    nb_variable = len(donnee["traces_ohe"])
    if donnee["eval_set"] == "training":
        training_pst.append(donnee["traces_ohe"])
        training_tl.append([donnee["longueur_traces"]]*nb_variable)
        training_label.append([donnee["label"]])
    elif donnee["eval_set"] == "test":
        test_pst.append(donnee["traces_ohe"])
        test_tl.append([donnee["longueur_traces"]]*nb_variable)
        test_label.append([donnee["label"]])
print("Triage terminé")
print("Nombre d'exemple d'entrainement : ",len(training_pst))
print("Nombre d'exemple de test : ",len(test_pst))


print("Lancement du réseau de neurone :")
net = network.Training(training_pst,training_tl,training_label,test_pst,test_tl,test_label)
res = net.train_evaluate()
