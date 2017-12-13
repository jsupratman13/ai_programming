#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#filename: pdnddqn.py                             
#brief: prioritized + dueling + DDQN               
#author: Joshua Supratman                    
#last modified: 2017.11.10. 
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
import numpy as np
import gym
import json
import matplotlib.pyplot as plt
import collections,random,sys,math
from keras.models import Sequential, Model
from keras.models import model_from_json
from keras.layers import Dense, Lambda
from keras.optimizers import Adam
from keras import backend as K

class Agent(object):
    def __init__(self,env):
        self.gamma = 0.95
        self.alpha = 0.001
        self.nepisodes = 5000
        self.epsilon = 1.0
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995
        self.updateQ = 100
        self.batch_size = 32
        self.weights_name = 'episodefinal.hdf5'
        self.env = env
        self.nstates = env.observation_space.shape[0]
        self.nactions = env.action_space.n
        self.model = self.create_neural_network()
        self.memory = collections.deque(maxlen=2000)
        self.target_model = self.model
        self.loss_list = []
        self.reward_list = []

    def create_neural_network(self):
        model = Sequential()
        model.add(Dense(100, input_dim=self.nstates, activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(self.nactions,activation='linear'))
        
        #get second last layer of the model, abondon the last layer
        layer = model.layers[-2]
        nb_action = model.output._keras_shape[-1]
       
        #layer y has a shape(nb_action+1)
        #y[:,0] represents V(s;theta)
        #y[:,1] represents A(a;theta)
        y = Dense(nb_action+1, activation='linear')(layer.output)
       
        #calculate the Q(s,a,;theta)
        #dueling type averate -> Q(s,a;theta) = V(s;theta) + (A(s,a;theta)-Average_a(A(s,a;theta)))
        #outputlayer = Lambda(lambda a:K.expand_dims(a[:,0], -1) + a[:,1:] - K.mean(a[:,1:], keepdims=True), output_shape=(nb_action,))(y)
        #dueling type max     -> Q(s,a;theta) = V(s;theta) + (A(s,a;theta)-Max_a(A(s,a;theta)))
        #dueling type naive   -> Q(s,a;theta) = V(s;theta) + A(s,a;theta)
        outputlayer = Lambda(lambda a: K.expand_dims(a[:,0], -1) + a[:,1:], output_shape=(nb_action,))(y)
       
        #connect
        model = Model(input=model.input, output=outputlayer)
       
        model.compile(loss='mse', optimizer=Adam(lr=self.alpha))
        model_json = model.to_json()
        with open('cartpole.json','w') as json_file:
            json_file.write(model_json)
        return model

    def load_model(self,filename):
        json_file = open(filename,'r')
        model = model_from_json(json_file.read())
        json_file.close() 
        return model

    def epsilon_greedy(self,state):
        if np.random.rand() < self.epsilon:
            return self.env.action_space.sample()
        else:
            Q = self.target_model.predict(state)
            return np.argmax(Q[0])

    def train(self):
        max_r = -1000
        for episode in range(self.nepisodes):
            s = self.env.reset()
            s = np.reshape(s,[1,self.nstates]) #change shape from (2,) to (1,2)
            treward = []
            loss = 0
            while True:
                a = self.epsilon_greedy(s)
                s2, r, done, info = self.env.step(a)
                s2 = np.reshape(s2, [1,self.nstates])
                Q = r if done else r + self.gamma * self.target_model.predict(s2)[0][np.argmax(self.model.predict(s2)[0])]
                target = self.target_model.predict(s)
                error = math.fabs(target[0][a]-Q)
                self.memory.append((s,a,r,s2,error,done)) #store <s,a,r,s'> in replay memory
                s = s2
                treward.append(r)
                if done:
                    break
            treward = sum(treward)

            #save checkpoint
            if not episode%1000: max_r = max_r - 100
            if treward > max_r:
                max_r = treward 
                self.model.save_weights('episode'+str(episode)+'.hdf5')

            #replay experience
            if len(self.memory) > self.batch_size:
                loss = self.replay()
            self.loss_list.append(loss)
            self.reward_list.append(treward)
            
            print 'episode: ' + str(episode+1) + ' reward: ' + str(treward) + ' epsilon: ' + str(round(self.epsilon,2)) + ' loss: ' + str(round(loss,4))

            #Target Network
            if not episode % self.updateQ:
                self.target_model = self.model

            #shift from explore to exploit
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
            
        self.model.save_weights(self.weights_name)

    def replay(self):
        minibatch = self.resampling(self.memory)
        loss = 0.0
        for s,a,r,s2,error,done in minibatch:
            Q = r if done else r + self.gamma * self.target_model.predict(s2)[0][np.argmax(self.model.predict(s2)[0])]
            target = self.target_model.predict(s)
            target[0][a] = Q
            #history = self.model.fit(s,target,epochs=1,verbose=0)
            loss += self.model.train_on_batch(s,target)
        #return history.history['loss'][0]
        return loss/len(minibatch)

    def resampling(self, memory):
        minibatch = []
        index = int(random.random()*self.batch_size)
        beta = 0.0
        max_w = max([m[4] for m in memory])
        for j in range(self.batch_size):
            beta += random.random() * 2.0 * max_w
            while beta > memory[index][4]:
                beta -= memory[index][4]
                index = (index + 1) % self.batch_size
            minibatch.append(memory[index])
        return minibatch 

    def test(self,modelname,weightname,ntrials=5):
        self.model = self.load_model(modelname)
        self.model.load_weights(weightname)
        self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha))
        self.epsilon = 0.1
        for trial in range(ntrials):
            s = self.env.reset()
            s = np.reshape(s,[1,self.nstates])
            treward = 0
            while True:
                self.env.render()
                a = self.epsilon_greedy(s)
                s2, r, done, info = self.env.step(a)
                s = np.reshape(s2, [1,self.nstates])
                treward += r
                if done:
                    print 'trial: '+str(trial+1) + ' reward: ' + str(treward) + ' epsilon: ' + str(self.epsilon)
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

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        assert False, 'missing argument'
    env = gym.make('CartPole-v1')
    agent = Agent(env)
    if str(sys.argv[1]) == 'train': 
        if len(sys.argv) > 2: agent.model.load_weights(str(sys.argv[2]))
        agent.train()
        agent.plot()
    if str(sys.argv[1]) == 'test':
        if len(sys.argv) < 4: assert False, 'missing .hdf5 weight or json file'
        agent.test(str(sys.argv[2]),str(sys.argv[3]))
