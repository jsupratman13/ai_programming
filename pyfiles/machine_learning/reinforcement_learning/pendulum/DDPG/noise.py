import random
import numpy as np

class Ornstein_Uhlenbeck(object):
    def function(self, x, mu, theta, sigma):
        return theta * (mu - x) + sigma * np.random.randn(1)

