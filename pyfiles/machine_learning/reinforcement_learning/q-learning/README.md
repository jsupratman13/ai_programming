#Q-Learning
* type of reinforcement learning algorithm
* given the Qtable Q, reward matrixR, learning paramteter y
```
Q(state,action) = R(state,action) + y*Max(Q(next state, all actions))
```
* The goal is to learn optimal Qmatrix and use the table in real situation
* Basically the Qmatrix or Qtable is the brain of the agent
* Q and R are matrix
* y or gamma has range from 0 to 1. if y is closer to zero, agent will tend to consider only immediate reward. if y is closer to one the agent will consider future reward with greater weight, willing to delay the reward

##Q Learning Algorithm
* Given: state diagram with goal state (represented by reward matrix R)
* Find: Minimum path from any initial state to the goal state (represented by matrix Q)
```
set paramter y and reward matrix R
Initialize matrix Q as zero matrix
for each episode:
    select random initial state
    while not reach goal state:
        select one among all possible actions for the current state
        using this possible action, consider to go to the next state
        get maximum Q value of this next state based on all possible actions
        compute(update) Q(s,a)=r+y*max(Q(s',a'))
        set next state as current state
    end while
end for
```
* algorithm above is used by agent to learn from experience or training
* each episode is equivalent to one training session, the more training the better Q matrix can be used by the agent to move in optimal way
* the purpose of training is to enhance the brain of the agent that represented by Q matrix
* in training, the agent explores the environment, get the reward until it reach goal state

##Utilizing Qtable
* The agent traces the sequence of state from the initial state until goal state
* algorithm is as simple as finding the action that makes maximum Q for current state
```
Input: Qmatrix, initial state
current state = initial state
while not reach goal state:
    find action that produce max Q value from current state
    current state = next state
```


```
