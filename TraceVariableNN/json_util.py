from json import dumps, loads, JSONEncoder
import pickle

json_types = (list, dict, str, int, float, bool)

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, json_types):
            return super().default(self, obj)
        else :
            return {'_python_object': pickle.dumps(obj).decode('latin-1')}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(dct['_python_object'].encode('latin-1'))
    return dct

"""
Ajout de traces de variable brutes dans la variable metadonnees
"""
def ajouter_metadonnee_old(programme,nb_code,number_cas_test,traces_brutes) :
    res = {}
    res["user"]= programme["user"]
    res["exo_name"]= programme["exercise_name"]
    res["nb_code"]= nb_code
    res["number_cas_test"]= number_cas_test
    res["eval_set"]= programme["eval_set"]
    res["date"]= programme["date"]
    res["traces_brutes"] = traces_brutes
    return res

"""
Ajout de traces de variable plus son traitement dans la variable metadonnees
"""
def ajouter_metadonnee(programme,nb_code,number_cas_test,traces_brutes,mon_vocabulaire) :
    res = {}
    res["user"]= programme["user"]
    res["exo_name"]= programme["exercise_name"]
    res["nb_code"]= nb_code
    res["number_cas_test"]= number_cas_test
    res["eval_set"]= programme["eval_set"]
    res["date"]= programme["date"]
    res["label"]=mon_vocabulaire.verif_label(programme["exercise_name"])
    res["traces_ohe"],res["longueur_traces"] = mon_vocabulaire.traitement_traces_brutes(traces_brutes)
    return res

"""
POUR LA DEUXIÈME EXPÉRIENCE
Ajout de traces de variable plus son traitement dans la variable metadonnees
"""
def ajouter_metadonnee_exp2(programme,nb_code,number_cas_test,traces_brutes,mon_vocabulaire,is_exp1) :
    res = {}
    res["user"]= programme["user"]
    res["exo_name"]= programme["exercise_name"]
    res["nb_code"]= nb_code
    res["number_cas_test"]= number_cas_test
    if is_exp1 :
        res["eval_set"]= programme["eval_set"]
    else:
        res["eval_set"]= "test_exp2"
    res["date"]= programme["date"]
    res["label"]=mon_vocabulaire.verif_label(programme["exercise_name"])
    res["traces_ohe"],res["longueur_traces"] = mon_vocabulaire.traitement_traces_brutes(traces_brutes)
    return res

def traduire_objet_en_json(metadonnees):
    for liste_traces in metadonnees:
        #print("trace numéro : ",liste_traces["nb_code"])
        for traces_programme in liste_traces["traces_brutes"]:
            for cle,traces_du_pas in traces_programme.items():
                #print(traces_du_pas)
                if(not isinstance(traces_du_pas, json_types)):
                    traces_programme[cle] = repr(traces_du_pas)



    return liste_traces
