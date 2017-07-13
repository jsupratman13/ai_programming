#!/usr/bin/env python
import numpy as np

class QLearning(object):
    def __init__(self, R, goal, gamma=0.8, episodes=1000):
        self.QTable = None
        self.R = R
        self.goal = goal
        self.gamma = gamma #closer to 1 delay reward, closer to 0 immediate reward
        self.num_episodes = episodes #more episodes means more training

    def testQ(self, s):
        path = [s]
        while s != self.goal:
            s2 = np.argmax(self.QTable[s,:])
            path.append(s2)
            s = s2
        return path

    def trainQ(self):
        #initialize QTable
        self.QTable = np.zeros([self.R.shape[0], self.R.shape[1]])

        for episode in range(self.num_episodes):
            #randomly pick initial state
            s = np.random.randint(len(self.R))
            while True:
                #get all possible actions from current state
                #possible_actions = self.get_possible_action(s)
                A = np.ndarray.flatten(np.argwhere(self.R[s,:]>=0))
                #pick an action
                a = np.random.choice(A)
                s2 = a #consider new state from given action (in this case the action is the state)

                #Compute
                self.QTable[s,a] = self.R[s,a] + self.gamma*np.max(self.QTable[s2,:])

                #set new state as current state
                s = s2

                #if current_state is goal finish session
                if s == self.goal: break
    
    def printQ(self):
        print np.round(self.QTable)

if __name__ == '__main__':
    state = ['A','B','C','D','E','F']
    #Reward Matrix, -1 is wall else reward value
    #Action          A,  B,  C,  D,  E,  F  #State
    R = np.array([[ -1, -1, -1, -1,  0, -1],#A
                  [ -1, -1, -1,  0, -1,100],#B
                  [ -1, -1, -1,  0, -1, -1],#C
                  [ -1,  0,  0, -1,  0, -1],#D
                  [  0, -1, -1,  0, -1,100],#E
                  [ -1,  0, -1, -1,  0,100]]#F
                  )
    goal = state.index('F')
    agent = QLearning(R,goal)
    agent.trainQ()
    agent.printQ()
    path = agent.testQ(state.index('A'))
    print 'path: ',
    for i in path:
        print state[i],
    print ''
    state2 = ['A','B','C','D','E','F','G','H']
    goal2 = state.index('D')
    #Action           A,  B,  C,  D,  E,  F,  G,  H
    R2 = np.array([[ -1, -1, -1, -1,  0, -1, -1, -1],#A
                   [ -1, -1,  0, -1, -1,  0, -1, -1],#B
                   [ -1,  0, -1,  0, -1, -1,  0, -1],#C
                   [ -1, -1,  0,100, -1, -1, -1, -1],#D
                   [  0, -1, -1, -1, -1,  0, -1, -1],#E
                   [ -1,  0, -1, -1,  0, -1,  0, -1],#F
                   [ -1, -1,  0, -1, -1,  0, -1,  0],#G
                   [ -1, -1, -1, -1, -1, -1,  0, -1]]#H
                   )
    agent = QLearning(R2,goal2)
    agent.trainQ()
    agent.printQ()
    path = agent.testQ(state2.index('A'))
    print 'path:',
    for i in path:
        print state2[i],
