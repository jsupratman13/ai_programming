#!/usr/bin/env python
import numpy as np

class QLearning(object):
    def __init__(self, R, goal, gamma=0.8, episodes=1000):
        self.QTable = None
        self.R = R
        self.goal = goal
        self.gamma = gamma #1に近いほど遅れ報酬
        self.num_episodes = episodes #エピソードが多い場合訓練が増える

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
            #一番高いQValueのactionを選ぶ
            for action in self.get_possible_action(current_state):
                if QValue < self.QTable[current_state][action]:
                    QValue = self.QTable[current_state][action]
                    new_state = action
            #actionをにpath追加
            path.append(new_state)
            #新しい状態を現在状態にセットする
            current_state = new_state
        return path

    def train_QTable(self):
        #QTableを初期化
        self.QTable = [[0 for row in range(len(self.R[0]))]for col in range(len(self.R))]

        for episode in range(self.num_episodes):
            #ランダムに初期状態を選ぶ
            current_state = np.random.randint(len(self.R))
            while True:
                #現在の状態に対して移動できる状態を探す
                possible_action = self.get_possible_action(current_state)
                #新しい状態をランダムに選ぶ
                new_state = np.random.choice(possible_action)
                #新しい状態に対してすべてのQValueを探す
                Qvalue = []
                for action in self.get_possible_action(new_state):
                    Qvalue.append(self.QTable[new_state][action])
                #式を計算する
                self.QTable[current_state][new_state] = self.R[current_state][new_state] + self.gamma*max(Qvalue)
                #新しい状態を現在状態にセットする
                current_state = new_state
                #もし現在状態がゴールの場合、このセッションを終了する
                if current_state == self.goal: break
        #必要ないがQTableを丸める。
        self.QTable = [[int(round(row)) for row in self.QTable[col]]for col in range(len(self.QTable))]
    
    def print_QTable(self):
        print 'QTable:'
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])for row in self.QTable]))
 
if __name__ == '__main__':
    state = ['A','B','C','D','E','F']
    #Reward Matrix, -1 が壁
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

