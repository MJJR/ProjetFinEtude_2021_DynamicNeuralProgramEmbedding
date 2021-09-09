'''
Created on Aug 11, 2017
@author: wangke
'''
from datetime import datetime

# from tensorflow import rnn
# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from tensorflow.compat.v1.nn import rnn_cell as rnn

num_epochs = 10
learning_rate = 0.0001
n_hidden = 200


vocabulary_size = 11553 # To be changed: input vocabulary
CLASSES = 65 # To be changed: prediction classes
batch_size = 32 # To be changed
program_number = 1 # To be changed: number of programs

class Training:
    '''
    classdocs
    '''

    def __init__(self, all_program_symbol_traces, trace_lengths, labels, test_all_program_symbol_traces, test_trace_lengths, test_labels,    test2_all_program_symbol_traces=None, test2_trace_lengths=None, test2_labels=None):
        '''
        Constructor
        '''
        self.all_program_symbol_traces = all_program_symbol_traces
        self.trace_lengths = trace_lengths
        self.labels = labels

        self.test_all_program_symbol_traces = test_all_program_symbol_traces
        self.test_trace_lengths = test_trace_lengths
        self.test_labels = test_labels

        self.test2_all_program_symbol_traces = test2_all_program_symbol_traces
        self.test2_trace_lengths = test2_trace_lengths
        self.test2_labels = test2_labels


    def train_evaluate(self):

        # trace inputs for training: each variable trace forms one data input, meaning one program may consist of multiple traces
        x = tf.placeholder(tf.int32, [batch_size, None])
        # length of each variable trace before padding
        seq_lengths = tf.placeholder(tf.int32, [batch_size])
        # labels for training
        '''
        MODIF : batch_size par program_number
        UN LABEL PAR PROGRAMME
        '''
        y = tf.placeholder(tf.int32, [program_number])

#         keep_prob = tf.constant(1.0)

        W = tf.Variable(tf.random_normal([n_hidden, CLASSES]))
        b = tf.Variable(tf.random_normal([CLASSES]))

        # Embedding layer
        embeddings = tf.get_variable('embedding_matrix', [vocabulary_size, n_hidden])
        rnn_inputs = tf.nn.embedding_lookup(embeddings, x)

        # RNN
        cell = rnn.GRUCell(n_hidden)
        cell = tf.nn.rnn_cell.MultiRNNCell([cell] * 2)

        init_state = cell.zero_state(batch_size, tf.float32)
        rnn_outputs, _ = tf.nn.dynamic_rnn(cell, rnn_inputs, sequence_length=seq_lengths, initial_state=init_state)


#         rnn_inputs = tf.nn.dropout(rnn_inputs, keep_prob)
#         rnn_outputs = tf.nn.dropout(rnn_outputs, keep_prob)

        # remove padding effects
        last_rnn_output = tf.gather_nd(rnn_outputs, tf.stack([tf.range(batch_size), seq_lengths-1], axis = 1))

        # again one program may have multiple variable traces so split with the number of programs instead of batches/variables
        list_of_program_tensors = tf.split(last_rnn_output, program_number, 0)

        all_programs_tensors = []
        for program_tensor in list_of_program_tensors:

            summed_reduced_program_tensor = tf.reduce_max(program_tensor, 0)
#             states_embedding_each_training_program = tf.reduce_mean(states_embedding_each_training_program, 0)
#             states_embedding_each_training_program = tf.reduce_sum(states_embedding_each_training_program, 0)
#             states_embedding_each_training_program = tf.reduce_logsumexp(states_embedding_each_training_program, 0)

            all_programs_tensors.append(summed_reduced_program_tensor)

        all_programs_tensors = tf.stack(all_programs_tensors, 0)

        prediction = tf.matmul(all_programs_tensors, W) + b

        print(y)
        print(tf.cast(tf.argmax(prediction,1), tf.int32))

        correct_pred = tf.equal(tf.cast(tf.argmax(prediction,1), tf.int32), y)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=prediction, labels=y))
        train_step = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=0.9, beta2=0.999).minimize(loss)

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)


            list_loss_iteration = []
            list_learn_error = []
            generalization_error_test1 = []
            generalization_error_test2 = []
            for i in range(num_epochs):

                print(datetime.now()," : Start iteration number ",i)

                # Demo purpose only for one batch add a for loop to read multiple batches
                '''
                AJOUT D'UNE BOUCLE FOR POUR TRAITER PLUSIEURS LOTS
                '''
                total_loss = 0
                nb_lot = len(self.all_program_symbol_traces)
                for lot in range( nb_lot ) :

                    _,_loss = sess.run(

                        [train_step, loss],

                        feed_dict={
                            x : self.all_program_symbol_traces[lot],
                            y : self.labels[lot],
                            seq_lengths : self.trace_lengths[lot],
                        })
                    print(datetime.now(),":iteration n°",i,"training with lot n°",lot,"loss = ",_loss,"(Process",lot*100/nb_lot,"% )")
                    total_loss += _loss

                print(datetime.now(),":training iteration n°",i,"and total_loss:",total_loss/nb_lot)
                list_loss_iteration.append(total_loss/nb_lot)

                """
                =============
                PHASE DE TEST
                =============
                """

                """
                LEARN ERROR
                """
                total_accuracy = 0
                nb_test = 0
                nb_lot = len(self.all_program_symbol_traces)
                for lot in range( nb_lot ) :
                    _accuracy = sess.run(

                        accuracy,

                        feed_dict={
                                x : self.all_program_symbol_traces[lot],
                                y : self.labels[lot],
                                seq_lengths : self.trace_lengths[lot],
                            })
                    print(datetime.now(),":Accuracy for training n°",nb_test,"is",_accuracy,"(Test process:",lot*100/nb_lot,"%)")
                    total_accuracy += _accuracy
                    nb_test += 1

                list_learn_error.append((1-(total_accuracy/nb_test))*100)
                print("Total accuracy (training):",total_accuracy*100/nb_test,"%")


                """
                TEST1
                """
                total_accuracy = 0
                nb_test = 0
                nb_lot = len(self.test_all_program_symbol_traces)
                for lot in range( nb_lot ) :
                    _accuracy = sess.run(

                        accuracy,

                        feed_dict={
                                x : self.test_all_program_symbol_traces[lot],
                                y : self.test_labels[lot],
                                seq_lengths : self.test_trace_lengths[lot],
                            })
                    print(datetime.now(),":Accuracy for test n°",nb_test,"is",_accuracy,"(Test process:",lot*100/nb_lot,"%)")
                    total_accuracy += _accuracy
                    nb_test += 1

                generalization_error_test1.append((1-(total_accuracy/nb_test))*100)
                print("Total accuracy (test):",total_accuracy*100/nb_test,"%")

                """
                TEST 2
                """
                if self.test2_all_program_symbol_traces != None:
                    total_accuracy = 0
                    nb_test = 0
                    nb_lot = len(self.test2_all_program_symbol_traces)
                    for lot in range( nb_lot ) :
                        _accuracy = sess.run(

                            accuracy,

                            feed_dict={
                                    x : self.test2_all_program_symbol_traces[lot],
                                    y : self.test2_labels[lot],
                                    seq_lengths : self.test2_trace_lengths[lot],
                                })
                        print(datetime.now(),"Accuracy for test n°",nb_test,":",_accuracy,"(Test process:",lot*100/nb_lot,"%)")
                        total_accuracy += _accuracy
                        nb_test += 1

                    generalization_error_test2.append((1-(total_accuracy/nb_test))*100)
                    print("Total accuracy (test2):",total_accuracy*100/nb_test,"%")


            print(datetime.now(), " : All iteration over !")

            print("Mean Loss per iteration :")
            for lost in range(len(list_loss_iteration)):
                print("Mean loss in iteration number ",lost," is ",list_loss_iteration[lost])

            print("Learn Error per iteration :")
            for mistake in range(len(list_learn_error)):
                print("Learn Error in iteration number ",mistake," is ",list_learn_error[mistake]," %")

            print("Generalization Error per iteration :")
            for acc in range(len(generalization_error_test1)):
                print("Generalization Error in iteration number ",acc," is ",generalization_error_test1[acc]," %")

            if self.test2_all_program_symbol_traces != None:
                print("Generalization Error per iteration for test 2 :")
                for acc in range(len(generalization_error_test2)):
                    print("Generalization Error in iteration number ",acc," is ",generalization_error_test2[acc]," %")
