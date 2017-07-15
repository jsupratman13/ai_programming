#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#filename: dqn.py                             
#brief: deep q-learning on neural network                  
#author: Joshua Supratman                    
#last modified: 2017.06.14. 
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
import numpy as np
import gym
import json
import matplotlib.pyplot as plt
import collections,random,sys
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.optimizers import Adam

class Agent(object):
    def __init__(self,env):
        self.gamma = 0.99
        self.alpha = 0.01
        self.nepisodes = 10000
        self.epsilon = 0.3
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.updateQ = 100
        self.weights_name = 'check.hdf5'
        self.env = env
        self.nstates = env.observation_space.shape[0]
        self.nactions = env.action_space.n
        self.model = self.create_neural_network()
        self.memory = collections.deque(maxlen=500)
        self.target_model = self.model
        self.loss_list = []
        self.reward_list = []

    def create_neural_network(self):
        model = Sequential()
        model.add(Dense(100,input_dim=self.nstates, activation='linear'))
        model.add(Dense(100,activation='relu'))
        model.add(Dense(self.nactions,activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.alpha))
        model_json = model.to_json()
        with open('mountaincar.json','w') as json_file:
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
            Q = self.model.predict(state)
            return np.argmax(Q[0])

    def train(self):
        max_r = -1000
        for episode in range(self.nepisodes):
            s = self.env.reset()
            s = np.reshape(s,[1,self.nstates]) #change shape from (2,) to (1,2)
            treward = []
            while True:
                a = self.epsilon_greedy(s)
                s2, r, done, info = self.env.step(a)
                s2 = np.reshape(s2, [1,self.nstates])
                #r = 1/(1+(0.5-s2[0][0])**2)
                r = 100 if done and sum(treward) > -199 else r
                self.memory.append((s,a,r,s2,done)) #store <s,a,r,s'> in replay memory
                s = s2
                treward.append(r)
                if done:
                    break
            #treward = max(treward)
            treward = sum(treward)

            #save checkpoint
            if treward > max_r:
            #if not episode%200:
                max_r = treward
                self.model.save_weights('check'+str(episode)+'.hdf5')

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
        minibatch = random.sample(self.memory,self.batch_size)
        loss = 0.0
        for s,a,r,s2,done in minibatch:
            Q = r if done else r + self.gamma * np.max(self.target_model.predict(s2)[0])
            target = self.target_model.predict(s)
            target[0][a] = Q
            #history = self.model.fit(s,target,epochs=1,verbose=0)
            loss += self.model.train_on_batch(s,target)
        #return history.history['loss'][0]
        return loss/len(minibatch)

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
    env = gym.make('MountainCar-v0')
    agent = Agent(env)
    if str(sys.argv[1]) == 'train': 
        if len(sys.argv) > 2: agent.model.load_weights(str(sys.argv[2]))
        agent.train()
        agent.plot()
    if str(sys.argv[1]) == 'test':
        if len(sys.argv) < 4: assert False, 'missing .hdf5 weight or json file'
        agent.test(str(sys.argv[2]),str(sys.argv[3]))
