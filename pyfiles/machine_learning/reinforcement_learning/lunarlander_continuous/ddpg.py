#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#filename: ddpg.py                             
#brief: deep deterministic policy gradient                  
#author: Joshua Supratman                    
#last modified: 2017.10.22. 
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
import numpy as np
import gym
import json
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import collections,random,sys
from keras.models import Sequential, Model, model_from_json
from keras.layers import Dense, Input
from keras.layers.merge import concatenate
from keras.optimizers import Adam
import keras.backend as K
import tensorflow as tf
import ConfigParser

class Agent(object):
    def __init__(self,env):
        config = ConfigParser.RawConfigParser()
        config.read('parameters.cfg')
        self.env = env
        sess = tf.Session()
        K.set_session(sess)
        np.random.seed(123)

        self.gamma = config.getfloat('training','gamma')
        alpha_actor = config.getfloat('training','alpha_actor')
        alpha_critic = config.getfloat('training','alpha_critic')
        tau = config.getfloat('network','tau')
        self.nepisodes = config.getint('training','episodes')
        self.weights_name = 'episodefinal.hdf5'
        
        self.nstates = env.observation_space.shape[0]
        self.nactions = env.action_space.shape[0]
        
        self.batch_size = config.getint('network','batch_size')
        self.memory = collections.deque(maxlen=config.getint('network','memory_size'))

        self.actor = ActorNetwork(sess, self.nstates, self.nactions, tau, alpha_actor)
        self.critic = CriticNetwork(sess, self.nstates, self.nactions, tau, alpha_critic)
        self.noise = Ornstein_Uhlenbeck(np.zeros(self.nactions))
        
        self.loss_list = []
        self.reward_list = []

    def load_model(self,filename):
        json_file = open(filename,'r')
        model = model_from_json(json_file.read())
        model.summary()
        json_file.close() 
        return model

    def train(self):
        max_r = -10000
        self.actor.update_target_network()
        self.critic.update_target_network()
        for episode in range(self.nepisodes):
            s = self.env.reset()
            #s = np.reshape(s,[1,self.nstates])
            s = np.hstack((s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]))
            treward = []
            while True:
                loss = 0.0
                #a = self.actor.model.predict(s)
                a = self.actor.model.predict(s.reshape(1,s.shape[0])) + self.noise()
                a[0][0] = max(env.action_space.low[0], min(env.action_space.high[0], a[0][0]))
                a[0][1] = max(env.action_space.low[1], min(env.action_space.high[1], a[0][1]))

                s2, r, done, info = self.env.step(np.array(a[0]))
                #s2 = np.reshape(s2, [1,self.nstates])
                s2 = np.hstack((s2[0], s2[1], s2[2], s2[3], s2[4], s2[5], s2[6], s2[7]))

                self.memory.append((s,a[0],r,s2,done))

                if len(self.memory) >= self.batch_size:
                    minibatch = random.sample(self.memory,self.batch_size)
                    states = np.asarray([e[0] for e in minibatch])
                    actions = np.asarray([e[1] for e in minibatch])
                    rewards = np.asarray([e[2] for e in minibatch])
                    next_states = np.asarray([e[3] for e in minibatch])
                    dones = np.asarray([e[4] for e in minibatch])
                    target = np.zeros(len(minibatch))

                    target_estimate = self.critic.target_model.predict([next_states, self.actor.target_model.predict(next_states)])

                    for i in range(len(minibatch)):
                        if dones[i]:
                            target[i] = rewards[i]
                        else:
                            target[i] = rewards[i] + self.gamma * target_estimate[i]

                    loss += self.critic.model.train_on_batch([states, actions], target)

                    a_for_grad = self.actor.model.predict(states)
                    grads = self.critic.gradients(states, a_for_grad)
                    self.actor.update_network(states, grads)

                    self.actor.update_target_network()
                    self.critic.update_target_network()

                s = s2
                treward.append(r)


                if done:
                    treward = sum(treward)
                    
                    #save checkpoint
                    if treward >= max_r:
                        max_r = treward
                        self.actor.model.save_weights('episode'+str(episode)+'.hdf5', overwrite=True)

                    print 'episode: ' + str(episode+1) + ' reward: ' + str(treward) + ' loss: ' + str(round(loss,4))
                    break
            
            self.reward_list.append(treward)
            self.loss_list.append(loss)
            
        self.actor.model.save_weights(self.weights_name)

    def test(self,modelname,weightname,ntrials=5):
        model = self.load_model(modelname)
        model.load_weights(weightname)
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        for trial in range(ntrials):
            s = self.env.reset()
            #s = np.reshape(s,[1,self.nstates])
            s = np.hstack((s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]))
            treward = 0
            while True:
                self.env.render()
                a = model.predict(s.reshape(1,s.shape[0]))
                s2, r, done, info = self.env.step(np.array(a[0]))
                #s = np.reshape(s2, [1,self.nstates])
                s = np.hstack((s2[0], s2[1], s2[2], s2[3], s2[4], s2[5], s2[6], s2[7]))
                treward += r
                if done:
                    print 'trial: '+str(trial+1) + ' reward: ' + str(treward)
                    break

    def plot(self):
        ep = np.arange(0, self.nepisodes, 1)
        plt.figure(1)
        plt.plot(ep, self.reward_list)
        plt.xlabel('episodes')
        plt.ylabel('reward')
        plt.savefig('reward.png')
        plt.figure(2)
        plt.plot(ep, self.loss_list)
        plt.xlabel('episodes')
        plt.ylabel('loss')
        plt.yscale('log')
        plt.savefig('loss.png')
        plt.show()

class Ornstein_Uhlenbeck(object):
    def __init__(self, mu, sigma=0.3, theta=0.15, dt=1e-2, x0=None):
        self.mu = mu
        self.sigma = sigma
        self.theta = theta
        self.dt = dt
        self.x0 = x0
        self.reset()

    def reset(self):
        self.prev_x = self.x0 if self.x0 is not None else np.zeros(self.mu.size)

    def __call__(self):
        x = self.prev_x + self.theta * (self.mu - self.prev_x) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.normal(size=self.mu.size)
        self.prev_x = x
        return x

class ActorNetwork(object):
    def __init__(self, sess, num_state, num_action, tau, learning_rate):
        self.tau = tau
        self.sess = sess

        self.model, self.weights, self.state = self.create_network(num_state, num_action)
        self.target_model, self.target_weights, self.target_state = self.create_network(num_state, num_action)
        self.action_gradient = tf.placeholder(tf.float32, [None, num_action])
        self.params_grad = tf.gradients(self.model.output, self.weights, -self.action_gradient)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(learning_rate).apply_gradients(grads)
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
        x = Dense(num_action, activation='tanh')(x)
        model = Model(inputs=state_input, outputs=x)
        model_json = model.to_json()
        with open('actor_model.json','w') as json_file:
            json_file.write(model_json)
        return model, model.trainable_weights, state_input

class CriticNetwork(object):
    def __init__(self, sess, num_state, num_action, tau, learning_rate):
        self.sess = sess
        self.tau = tau
        self.learning_rate = learning_rate

        self.model, self.action, self.state = self.create_network(num_state, num_action)
        self.target_model, self.target_action, self.target_state = self.create_network(num_state, num_action)
        self.action_gradient = tf.gradients(self.model.output, self.action)
        self.sess.run(tf.global_variables_initializer())

    def gradients(self, states, actions):
        return self.sess.run(self.action_gradient, feed_dict={self.state: states, self.action: actions})[0]

    def update_target_network(self):
        critic_weights = self.model.get_weights()
        critic_target_weights = self.target_model.get_weights()
        for i in xrange(len(critic_weights)):
            critic_target_weights[i] = self.tau*critic_weights[i] + (1-self.tau)*critic_target_weights[i]
        self.target_model.set_weights(critic_target_weights)

    def create_network(self, num_state, num_action):
        #action_input = Input(shape=(num_action,))
        #state_input = Input(shape(1,)+num_state)
        #, Inputflattened_state = Flatten()(state_input)
        #x = concatenate([action_input, flattened_state])
        action_input = Input(shape=[num_action])
        state_input = Input(shape=[num_state])
        x = concatenate([state_input, action_input])
        x = Dense(400, activation='relu')(x)
        x = Dense(300, activation='relu')(x)
        x = Dense(300, activation='relu')(x)
        x = Dense(1, activation='linear')(x)
        model = Model(inputs=[state_input, action_input], outputs=x)
        model_json = model.to_json()
        with open('critic_model.json','w') as json_file:
            json_file.write(model_json)
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model, action_input, state_input

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        assert False, 'missing argument'
    env = gym.make('LunarLanderContinuous-v2')
    agent = Agent(env)
    if str(sys.argv[1]) == 'train': 
        #if len(sys.argv) > 2: agent.model.load_weights(str(sys.argv[2]))
        agent.train()
        agent.plot()
    if str(sys.argv[1]) == 'test':
        if len(sys.argv) < 4: assert False, 'missing .hdf5 weight or json file'
        agent.test(str(sys.argv[2]),str(sys.argv[3]))
