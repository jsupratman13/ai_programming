import numpy as np
import math
from keras.models import Sequential, Model, model_from_json
from keras.layers import Dense, Flatten, Input, merge, Lambda, Activation
from keras.optimizers import Adam
import tensorflow as tf
import keras.backend as K

class CriticNetwork(object):
    def __init__(self, sess, num_state, num_action, batch_size, tau, learning_rate):
        self.sess = sess
        self.batch_size = batch_size
        self.tau = tau
        self.learning_rate = learning_rate

        K.set_session(sess)

        self.model, self.action, self.state = self.create_network(num_state, num_action)
        self.target_model, self.target_action, self.target_state = self.create_network(num_state, num_action)
        self.action_gradient = tf.gradients(self.model.output, self.action)
        #self.sess.run(tf.initialize_all_variables())
        self.sess.run(tf.global_variables_initializer())

    def gradients(self, states, actions):
        return self.sess.run(self.action_gradient, feed_dict={self.state: states, self.action: actions})[0]

    def update_target_network(self):
        critic_weights = self.model.get_weights()
        critic_target_weights = self.target_model.get_weights()
        for i in xrange(len(actor_weights)):
            critic_target_weights[i] = self.tau*critic_weights[i] + (1-self.tau)*critic_target_weights[i]
        self.target_model.set_weights(critic_target_weights)

    def create_network(self, num_state, num_action):
        #action_input = Input(shape=(num_action,))
        #state_input = Input(shape(1,)+num_state)
        #flattened_state = Flatten()(state_input)
        #x = concatenate([action_input, flattened_state])
        action_input = Input(shape=[num_action])
        state_input = Input(shape=[num_state])
        s = Dense(400, activation='relu')(state_input)
        a = Dense(300, activation='relu')(action_input)
        s2 = Dense(300, activation='relu')(s)
        x = merge([s2,a],mode='sum')
        x = Dense(num_action, activation='relu')(x)
        model = Model(inputs=[state_input, action_input], outputs=x)
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model, action_input, state_input

        
