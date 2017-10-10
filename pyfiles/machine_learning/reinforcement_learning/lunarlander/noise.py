import random
import numpy as np

class Ornstein_Uhlenbeck(object):
    def __init__(self, mu, sigma=0.3, theta=0.15, dt=1e-2, x0=None, size=1):
        self.theta = theta
        self.mu = mu
        self.dt = dt
        self.x0 = x0
        self.sigma = sigma
        self.size = 1
        self.reset()

    def reset(self):
        self.x_prev = self.x0 if self.x0 is not None else np.zeros(self.size)

    def __call__(self):
        x = self.x_prev + self.theta * (self.mu - self.x_prev) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.normal(size=self.size) 
        self.x_prev = x
        return x

    def function(self, x, mu, theta, sigma):
        return theta * (mu - x) + sigma * np.random.randn(1)


class Epsilon_Greedy(object):
    def __init__(self, env, epsilon=1, min_epsilon=0.01, epsilon_decay=0.995):
        self.env = env
        self.epsilon = epsilon
        self.min_epsilon = 0.01
        self.epsilon_decay=0.995
        self.reset()

    def reset(self):
        self.current_epsilon = self.epsilon

    def __call__(self, action):
        if np.random.rand() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = np.argmax(action)
    
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
        
        return action
