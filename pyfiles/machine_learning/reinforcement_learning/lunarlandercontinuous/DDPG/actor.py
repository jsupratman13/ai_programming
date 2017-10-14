import numpy as np
import math
from keras.models import Sequential, Model, model_from_json
from keras.layers import Dense, Flatten, Input, merge, Lambda
from keras.optimizers import Adam
import tensorflow as tf
import keras.backend as K

class ActorNetwork(object):
    def __init__(self, sess, num_state, num_action, batch_size, tau, learning_rate):
        self.sess = sess
        self.batch_size = batch_size
        self.tau = tau
        self.learning_rate = learning_rate

        K.set_session(sess)

        self.model, self.weights, self.state = self.create_network(num_state, num_action)
        self.target_model, self.target_weights, self.target_state = self.create_network(num_state, num_action)
        self.action_gradient = tf.placeholder(tf.float32, [None, num_action])
        self.params_grad = tf.gradients(self.model.output, self.weights, -self.action_gradient)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).apply_gradients(grads)
        #self.sess.run(tf.initialize_all_variables())
        self.sess.run(tf.global_variables_initializer())

    def update_network(self, states, action_gradients):
        self.sess.run(self.optimize, feed_dict={self.state: states, self.action_gradient: action_gradients})

    def update_target_network(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in xrange(len(actor_weights)):
            actor_target_weights[i] = self.tau*actor_weights[i] + (1-self.tau)*actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def create_network(self, num_state, num_action):
        #action_input = Input(shape=(1,)+num_state)
        state_input = Input(shape=[num_state])
        x = Dense(400, activation='relu')(state_input)
        x = Dense(400, activation='relu')(x)
        x = Dense(400, activation='relu')(x)
        #x = Dense(num_action, activation='linear')(x)
        x = Dense(num_action,activation='tanh')(x)
        model = Model(inputs=state_input, outputs=x)
        return model, model.trainable_weights, state_input

        
