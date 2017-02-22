#!/usr/bin/env python
import numpy as np

class QLearning(object):
    def __init__(self, R, goal, gamma=0.8, episodes=1000):
        self.QTable = None
        self.R = R
        self.goal = goal
        self.gamma = gamma #1$B$K6a$$$[$ICY$lJs=7(B
        self.num_episodes = episodes #$B%(%T%=!<%I$,B?$$>l9g71N}$,A}$($k(B

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
            #$B0lHV9b$$(BQValue$B$N(Baction$B$rA*$V(B
            for action in self.get_possible_action(current_state):
                if QValue < self.QTable[current_state][action]:
                    QValue = self.QTable[current_state][action]
                    new_state = action
            #action$B$r$K(Bpath$BDI2C(B
            path.append(new_state)
            #$B?7$7$$>uBV$r8=:_>uBV$K%;%C%H$9$k(B
            current_state = new_state
        return path

    def train_QTable(self):
        #QTable$B$r=i4|2=(B
        self.QTable = [[0 for row in range(len(self.R[0]))]for col in range(len(self.R))]

        for episode in range(self.num_episodes):
            #$B%i%s%@%`$K=i4|>uBV$rA*$V(B
            current_state = np.random.randint(len(self.R))
            while True:
                #$B8=:_$N>uBV$KBP$7$F0\F0$G$-$k>uBV$rC5$9(B
                possible_action = self.get_possible_action(current_state)
                #$B?7$7$$>uBV$r%i%s%@%`$KA*$V(B
                new_state = np.random.choice(possible_action)
                #$B?7$7$$>uBV$KBP$7$F$9$Y$F$N(BQValue$B$rC5$9(B
                Qvalue = []
                for action in self.get_possible_action(new_state):
                    Qvalue.append(self.QTable[new_state][action])
                #$B<0$r7W;;$9$k(B
                self.QTable[current_state][new_state] = self.R[current_state][new_state] + self.gamma*max(Qvalue)
                #$B?7$7$$>uBV$r8=:_>uBV$K%;%C%H$9$k(B
                current_state = new_state
                #$B$b$78=:_>uBV$,%4!<%k$N>l9g!"$3$N%;%C%7%g%s$r=*N;$9$k(B
                if current_state == self.goal: break
        #$BI,MW$J$$$,(BQTable$B$r4]$a$k!#(B
        self.QTable = [[int(round(row)) for row in self.QTable[col]]for col in range(len(self.QTable))]
    
    def print_QTable(self):
        print 'QTable:'
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])for row in self.QTable]))
 
if __name__ == '__main__':
    state = ['A','B','C','D','E','F']
    #Reward Matrix, -1 $B$,JI(B
    #Action  A,  B,  C,  D,  E,  F  #State
    R =  [[ -1, -1, -1, -1,  0, -1],#A
          [ -1, -1, -1,  0, -1,100],#B
          [ -1, -1, -1,  0, -1, -1],#C
          [ -1,  0,  0, -1,  0, -1],#D
          [  0, -1, -1,  0, -1,100],#E
          [ -1,  0, -1, -1,  0,100]]#F
    goal = state.index('F')

    agent = QLearning(R,goal)
    agent.train_QTable()
    agent.print_QTable()
    path = agent.use_QTable(state.index('C'))
    print 'path:',
    for i in path:
        print state[i],

