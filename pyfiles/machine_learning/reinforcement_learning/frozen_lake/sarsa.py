import gym
import numpy as np
import sys

class Agent(object):
    def __init__(self, env):
        self.env = env
        self.gamma = 0.99
        self.alpha = 0.01
        self.num_episodes = 20000
        self.num_trials = 100
        self.epsilon = 0.3
        self.Q = np.zeros([env.observation_space.n, env.action_space.n])

    def save_table(self, filename='check.npy'):
        np.save(filename, self.Q)
    
    def load_table(self, filename):
        self.Q = np.load(filename)

    def epsilon_greedy(self, Q, state):
        e = np.random.uniform()
        if e < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = np.argmax(Q[state,:])
        return action

    def train(self):
        for episode in range(self.num_episodes):
            s = self.env.reset()
            a = self.epsilon_greedy(self.Q,s) 
            while True:
                s2 , r, done, info = self.env.step(a)
                a2 = self.epsilon_greedy(self.Q,s2)
                self.Q[s,a] = self.Q[s,a] + self.alpha * (r + self.gamma * self.Q[s2,a2] -  self.Q[s,a])
                s = s2
                a = a2
                if done: break
        self.save_table()

    def test(self,render=False):
        total_reward = 0
        if render: self.num_trials = 1
        for i in range(self.num_trials):
            s = self.env.reset()
            reward = 0
            while True:
                if render: self.env.render()
                a = np.argmax(self.Q[s,:])
                s2, r, done, info = self.env.step(a)
                s = s2
                reward += r
                if done:
                    break
            total_reward += reward
        print 'success rate: ' + str(total_reward/self.num_trials)

if __name__=='__main__':
    if len(sys.argv) < 2:
        assert False, 'missing argument'
    env = gym.make('FrozenLake-v0')
    agent = Agent(env)
    if str(sys.argv[1]) == 'train':
        if len(sys.argv) > 2: agent.load_table(str(sys.argv[2]))
        agent.train()
    if str(sys.argv[1]) == 'test':
        if len(sys.argv) < 3: assert False, 'missng .npy table'
        agent.load_table(str(sys.argv[2]))
        if len(sys.argv) > 3 and str(sys.argv[3]) == 'render':
               agent.test(render=True)
        else:
            agent.test()

