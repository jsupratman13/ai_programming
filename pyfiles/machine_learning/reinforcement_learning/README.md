# Reinforcement Learning
## Resource
people.revoledu.com/kardi/tutorial/ReinforcementLearning/Q-Learning.htm

## Installation
```
pip install keras-rl
pip install h5py
pip install gym
pip install tensorflow
```
## Content
Environment problems are classified as below. Depending on the type of problem, different RL algorithms are given
* discrete state and action: frozen lake
* continuous state and discrete action: mountain car, cartpole
* continuous state and action: pendulum

## What is reinforcement learning problem
* reinforcement learning or RL is learning what to do and how to map siutations to action. The resul is to maximize the numerical reqward. Learner are not told which action to take but instead must discover which action will yield the maximum reward.
* a branch of machine learning that is concerned with making sequence of decisions. assume that an agent that is situated in an environment
* at each step the agent takes action and receives an observation and reeward from environment. 
* RL seeks to maximize total reward given previously unknown enviornment through learning process which invovles trial and error.
* ex. child learn how to walk
  * agent = child
  * envoronment = surface to walk
  * take action = walking
  * state = standup, stay still take step etc
  * reward = chocoloate
* for each state, agent performs action and receive feedback (reward, new state) and repeats until it finds actions to perform in the current state to obtain the maximum reward
```
        action------------->
agent <                     > Environment
        <-observation,reward
```

## Comparing to other topics in machine learning
* supervised learning vs reinforcement learning
  * sl is when agent learns something with a supervisor watching over them. The supervisor have the correct answer and for each action the agent take, the supervisor reward for accuracy (deep learning is here).
  * however there are some problem that have multiple alternative to achieve the objective making it difficult to create a correct answer sheet aka supervisor.
  * both rl and sl have mapping between input and output
  * rl learns to react to an enviornment by reward function
  * sl task driven through teaching
* unsupervised learning vs reinforcment learning
  * ul have no mapping between input and output.
  * no supervisor, task is to find some sort of pattern
  * ex task suggest new article to user
    * ul will look at similar articles which user have previously read and suggest anyone from them
    * rl will get constant feedback from user by suggesting few news articles and then build a knowledge graph of which articles the user like
* RL focus on making good decision, sl and ul mostly focused on making predictions. 
* sl is simply get the algorithm to pair cetain stimuli but rl must pair itself using observation reward and action. No true correct action for agent to take so it gets tricky

## exploitation vs exploration
* ex maximum bonus from slotmachine
* pure exploitation: select one machine and continue using it to get maximum bonus
* pure exploration: pull every machine to find maximum bonus

## Markov Decision Process
* mathematical framework of rl
* s : state
* a : action
* r : reward function
* pi : policy (set of action) takes in observation and output actions
* v : value(rewards we receive) goodness of states and action
* Q(s,a): how much reward i get if i am in state s and choose action a

## Algorithm
* policy based: focus on optimal policy (learn which reward for each possible action and find optimal solutions)
* value based : focus on optimal value (predict how good a given state or action will be for agent to be in)
* action based: focus on optimal action to take

### Deep Q Learning
* policy based learning algorithm
* used by Google to beat humans in atari games
```
initialize values Q(s,a)
observe current state
choose action a from Q based on action selection policies
perform action and observe reward r and new state s
update the value for the state using the observed reward and the maximum reward possible for the next state
set state to new state and repeat process until terminate state is reached
```

## Example
In reality RL have the following characteristic
1. different action yield different result. In maze, one path lead to treasure while the other path lead to traps
2. reward are delayed over time. In maze, we may not know the result of the path until later on
3. reward for an action is conditional. In maze, turning to the left may be ideal until a certain point
### 2 Armed Bandit
* simplest form of reinforcement learning
* for two slot machine, find the machine with the biggest payout
* no need to consider 2 and 3
* only focus on which rewards we get for each possible action and ensure to pick optimal one
* policy gradient: method where simple neural network learns policy for picking actions by adjusting its weight through gradient descent using feedback from environment.
#### Policy Gradient
```
Loss = Log(pi)*A
Where A is advantage
pi is policy
```
* Loss function allows agent to increase the weight for actions that yield positive reward and decrease for negative reward

## Markvo Decision Process
* Environment which pose the full problem to an agent are referrred to as MDP
* environment not only provide rewards and state transitions given action but those rewards are also condition on the state of the environment and the action the agent takes within the state.
* dynamics are temporar and can be delayed over time
* set of all possible state S which the agent at any time experience s.
* set of all possible action A from which our agent at anytime will take action a.
* given a state action pair (s,a):
  * the transition probabilty to a new state s' is defined by T(s,a)
  * the reward r is given by R(s,a)
* anytime in MDP, an agen is given a state s, takes action a, receives new state s' and reward r
### example
* open a door
* state: vision of the door, position of body and door in the world coordinate
* action: movement our body could make
* reward: successfully opening door
* actions such as walking toward the door are essential to solving problem but are not themselves reward giving since only door open provide reward.
* agent need to learn to assign value to actions to eventually lead to the reward hence introducing temoporal dynamics

## Cart-Pole Task
Goal is to balance the pole as long as possible
* Observation: agent need to know where the pole is and the angle it is balancing
* delayed reward: keeping pole in air as long as possible means moving in ways that will be advantageous for both the present and the future. to accomplish this reward value for each observation-action pair must be adjusted using a function that weighs actions over time
* From armed bandit, agent need update with more than one experence at a time -> collect experiences in a buffer and then occasionally use them to update the agent all at once
* the sequence of experience are referred to as rollouts or experience traces
* reward must be properly adjusted by a discount factor before applying the rollouts
* allow each action to be a littble bit responsible for not only the immediate reqard but all the rewards that follow

## Q-Learning
* RL algorithm
* different from policy based algorithm 
* insted of learning functions which directly map a observation to an action -> attemps to learn the value of being in a given state and take specific action there
* both method lead to intelligent action but the approach is different
### Example Frozen Lake
* 4x4 where s is start, h is hole, f is frozen surface and g is goal
* go to goal without falling to hole
* agent can go up down left right but the catch is that there is a wind that may push the agent to an unplanned grid
* perfect performance is impossible but learning to avoid holes is duable
* every step reward is 0 except for goal state which is 1 -> long term expected reward
* create Qtable 16x4 matrix 16 is grid number and 4 is action(up down left right) all initialize with 0
* update table accordingly using bellman equation
```
Q(s,a) = r+gamma(max(Q(s',a')))
r is current reward
Q is Qtable matrix
s is state
a is action
gamma is maximum discounted future reward (decide how important the possible future rewards are compared to the present reward)
```
* In this way, Qtable is resued when estimating how to update the table for future action
* this is simple example using table but in real world enviornment have larger variable to consider -> use neural network



