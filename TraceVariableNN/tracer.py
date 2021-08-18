import sys,json

class BoucleInfinie(Exception):
    pass

class Tracer(object):

  def __init__(self):
    """
        lines_trace =   liste contenant les lignes executees lors de l'appel d'une fonction
        nb_max_entree = taille maximale de la liste de lines_trace avant de detecter une condition de boucle infini
        dico_event =    dictionnaire a 5 entrees, chaque entrees defini un evenement pouvant etre releve par la fonction tracer.
                        Mettre a True si l'ont veut que cet evenement soit pris en compte'
    """
    super(Tracer, self).__init__()
    self.lines_trace = []
    self.var_traces= []
    self.nb_max_entree = 400
    # call, line, return, exception, opcode
    self.dico_event = {"call":True, "line":True, "return":False, "exception":False, "opcode":False}

  def __del__(self):
      print("tracer deleted")

  def tracer(self, frame, event, arg = None):
    """
        Definit la methode de trace
    """
    line_no = frame.f_lineno
    # Utiliser la synchronisation basee sur SIGALRM s'est averee peu fiable sur diverses installations python et est inutilisable sur Windows,
    # Une autre solution enviseagable serait d'appeler la fonction dans un thread avec un timeout defini.
    if(len(self.lines_trace)>self.nb_max_entree):
        raise BoucleInfinie()
    #print(f"A {event} at line number {line_no} ")
    #print(frame.f_locals)

    if self.dico_event[event] == True:
        self.lines_trace.append(line_no)
        self.var_traces.append(frame.f_locals.copy())
    return self.tracer

  def get_trace_and_result(self,fonction,*args,**kwargs):
    """
        Execute une fonction pour en extraire la trace d'execution.

        @param fonction: le nom de la fonction
        @param args: les arguments de la fonction ( mis un par un )

        @return un tuple trace, contenant la liste des lignes executees ainsi que , et res, le resultat de la fonction
    """
    # mise en place de la fonction trace
    sys.settrace(self.tracer)

    # appel de la fonction a tester
    try:
        res = fonction(*args)

    except BoucleInfinie as e:
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "Boucle infinie")

    except IndexError as e :
        print("IndexError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "IndexError")

    except UnboundLocalError as e :
        print("UnboundLocalError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "UnboundLocalError")

    except AttributeError as e :
        print("AttributeError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "AttributeError")
    except ZeroDivisionError as e :
        print("ZeroDivisionError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "ZeroDivisionError")
    except AssertionError as e :
        print("AssertionError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "AssertionError")
    except TypeError as e :
        print("TypeError sur le programme numéro ",nb_programme)
        trace = self.lines_trace
        vartrace = self.var_traces
        self.lines_trace = []
        self.var_traces = []
        sys.settrace(None)
        return(trace, vartrace, "TypeError")    




    # on recupere la liste des lignes executees pendant la trace
    trace = self.lines_trace
    vartrace = self.var_traces
    self.lines_trace = []
    self.var_traces = []
    sys.settrace(None)

    return (trace,vartrace,res)
