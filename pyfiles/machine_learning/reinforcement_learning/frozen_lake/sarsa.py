import gym
import numpy as np

class Agent(object):
    def __init__(self, env):
        self.env = env
        self.gamma = 0.99
        self.alpha = 0.1
        self.num_episodes = 100
        self.epsilon = 0.5
        self.Q = np.zeros([env.observation_space.n, env.action_space.n])

    def set_RL(self, gamma, alpha, num_episodes):
        self.gamma = gamma
        self.alpha = alpha
        self.num_episodes = num_episodes

    def set_epsilon(self, eps):
        self.epsilon = eps

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
    
    def test(self):
        total_reward = 0
        for i in range(100):
            s = self.env.reset()
            reward = 0
            while True:
                #self.env.render()
                a = np.argmax(self.Q[s,:])
                s2, r, done, info = self.env.step(a)
                s = s2
                reward += r
                if done:
                    break
            total_reward += reward
        print 'success rate: ' + str(total_reward/100)

if __name__=='__main__':
    env = gym.make('FrozenLake-v0')
    agent = Agent(env)
    agent.set_RL(0.99, 0.01, 20000)
    agent.set_epsilon(0.3)
    agent.test()
    agent.train()
    agent.test()
