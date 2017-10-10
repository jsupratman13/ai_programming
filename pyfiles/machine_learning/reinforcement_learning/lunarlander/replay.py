import collections
import random

class ReplayBuffer(object):
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.num_experiences = 0
        self.memory = collections.deque(maxlen=memory_size)

    def get_batch(self, batch_size):
        if self.num_experiences < batch_size:
            return random.sample(self.memory, self.num_experiences)
        else:
            return random.sample(self.memory, batch_size)

    def size(self):
        return self.memory_size

    def add(self, state, action, reward, new_state, done):
        experience = (state, action, reward, new_state, done)
        if self.num_experiences < self.memory_size:
            self.memory.append(experience)
            self.num_experiences += 1
        else:
            self.memory.popleft()
            self.memory.append(experience)

    def count(self):
        return self.num_experiences

    def erase(self):
        self.memory = collections.deque(maxlen=self.memory_size)
        self.num_experiences = 0
