'''
Created on June 05 2021

@author: Mathieu REDOR
'''

import tracer,programme_1,programme_2,programme_3,programme_4,programme_5,trace_into_entree
import numpy as np
import tensorflow as tf

les_traces = np.array([])



print("PROGRAMME UN")

traceur = tracer.Tracer()
res = traceur.get_trace_and_result(programme_1.minimum,[9,2,-1,8,0])
print(res[1])

#les_traces.append(trace_into_entree.trace_into_entree(res[1]))
les_traces = np.append(les_traces,trace_into_entree.trace_into_entree(res[1]))

dataset = tf.data.Dataset.from_tensor_slices(trace_into_entree.trace_into_entree(res[1]))


print("PROGRAMME DEUX")

traceur = tracer.Tracer()
res = traceur.get_trace_and_result(programme_2.max,20,12)
print(res[1])

#les_traces.append(trace_into_entree.trace_into_entree(res[1]))
les_traces = np.append(les_traces,trace_into_entree.trace_into_entree(res[1]))


print("PROGRAMME TROIS")

traceur = tracer.Tracer()
res = traceur.get_trace_and_result(programme_3.multiplier,12,42)
print(res[1])

#les_traces.append(trace_into_entree.trace_into_entree(res[1]))
les_traces = np.append(les_traces,trace_into_entree.trace_into_entree(res[1]))

print("PROGRAMME QUATRE")

traceur = tracer.Tracer()
res = traceur.get_trace_and_result(programme_4.est_paire,78)
print(res[1])

#les_traces.append(trace_into_entree.trace_into_entree(res[1]))
les_traces = np.append(les_traces,trace_into_entree.trace_into_entree(res[1]))

print("PROGRAMME CINQ")

traceur = tracer.Tracer()
res = traceur.get_trace_and_result(programme_5.liste_contient_ce_truc,[1,2,3,4,5,6,7,8,9],8)
print(res[1])

#les_traces.append(trace_into_entree.trace_into_entree(res[1]))
les_traces = np.append(les_traces,trace_into_entree.trace_into_entree(res[1]))

print("TEST JSON INTO ENTREE")

print(les_traces)

print("TEST ONE HOT ENCODING DES TRACES")


#ragged_tensors = tf.ragged.constant(les_traces)

#dataset = tf.data.Dataset.from_tensor_slices(ragged_tensors)

#mon_test = tf.one_hot(dataset,50)

#print(mon_test)
