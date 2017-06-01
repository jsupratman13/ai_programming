#!/usr/bin/env python
import numpy as np

class QLearning(object):
    def __init__(self, R, goal, gamma=0.8, episodes=1000):
        self.QTable = None
        self.R = R
        self.goal = goal
        self.gamma = gamma #closer to 1 delay reward, closer to 0 immediate reward
        self.num_episodes = episodes #more episodes means more training

    def get_possible_action(self,current_state):
        actions = []
        for index in range(len(self.R[current_state])):
            if self.R[current_state][index] >= 0:
                actions.append(index)
        return actions

    def use_QTable(self,current_state):
        path = [current_state]
        while current_state != self.goal:
            QValue = 0
            #pick action with the highest QValue
            for action in self.get_possible_action(current_state):
                if QValue < self.QTable[current_state][action]:
                    QValue = self.QTable[current_state][action]
                    new_state = action
            #append action to the path
            path.append(new_state)
            #set next state as current state
            current_state = new_state
        return path

    def train_QTable(self):
        #initialize QTable
        self.QTable = [[0 for row in range(len(self.R[0]))]for col in range(len(self.R))]

        for episode in range(self.num_episodes):
            #randomly pick initial state
            current_state = np.random.randint(len(self.R))
            while True:
                #randomly pick possible action from current state
                possible_action = self.get_possible_action(current_state)
                #consider new state
                new_state = np.random.choice(possible_action)
                #find all Qvalue for new state with all possible action
                Qvalue = []
                for action in self.get_possible_action(new_state):
                    Qvalue.append(self.QTable[new_state][action])
                #Compute
                self.QTable[current_state][new_state] = self.R[current_state][new_state] + self.gamma*max(Qvalue)
                #set new state as current state
                current_state = new_state
                #if current_state is goal finish session
                if current_state == self.goal: break
        #Round to the nearest integer
        self.QTable = [[int(round(row)) for row in self.QTable[col]]for col in range(len(self.QTable))]
    
    def print_QTable(self):
        print 'QTable:'
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])for row in self.QTable]))
 
if __name__ == '__main__':
    state = ['A','B','C','D','E','F']
    #Reward Matrix, -1 is wall else reward value
    #Action  A,  B,  C,  D,  E,  F  #State
    R =  [[ -1, -1, -1, -1,  0, -1],#A
          [ -1, -1, -1,  0, -1,100],#B
          [ -1, -1, -1,  0, -1, -1],#C
          [ -1,  0,  0, -1,  0, -1],#D
          [  0, -1, -1,  0, -1,100],#E
          [ -1,  0, -1, -1,  0,100]]#F
    goal = state.index('F')

    state2 = ['A','B','C','D','E','F','G','H']
    goal2 = state.index('D')
    #Action  A,  B,  C,  D,  E,  F,  G,  H
    R2 = [[ -1, -1, -1, -1,  0, -1, -1, -1],#A
          [ -1, -1,  0, -1, -1,  0, -1, -1],#B
          [ -1,  0, -1,  0, -1, -1,  0, -1],#C
          [ -1, -1,  0,100, -1, -1, -1, -1],#D
          [  0, -1, -1, -1, -1,  0, -1, -1],#E
          [ -1,  0, -1, -1,  0, -1,  0, -1],#F
          [ -1, -1,  0, -1, -1,  0, -1,  0],#G
          [ -1, -1, -1, -1, -1, -1,  0, -1]]#H

    agent = QLearning(R,goal)
    agent.train_QTable()
    agent.print_QTable()
#    path = agent.use_QTable(state2.index('A'))
#    print 'path:',
#    for i in path:
#        print state2[i],

