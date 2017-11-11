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

