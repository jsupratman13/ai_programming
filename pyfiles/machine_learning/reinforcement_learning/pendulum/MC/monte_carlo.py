import gym
import numpy as np
import math,sys
from features import RBF

def test(w, episode=1, rendering=False):
    reward = []
    for e in range(episode):
        s = env.reset()
        rt = 0
        while True:
            a = policy(s,w)
            if rendering: 
                env.render()
     #           print a
            s2, r, done, info = env.step(a)
            s = s2
            rt += r
            if done:
                reward.append(rt)
                break
    return sum(reward)/len(reward)

def record(l,w):
    f = open('result.csv','a')
    reward = test(w)
    f.write(str(l)+','+str(reward)+'\n')
    f.close()
    return reward

def likelihood_function(s,a,w):
    sigma = 0.5
    phi = rbf.get_features(s)
    a = a.item(0)
    mu = (phi.T*w).item(0)
    return ((a-mu)*phi)/(sigma**2)

def sampling(w):
    sample = []
    s = env.reset()
    for i in range(100):
        a = policy(s,w)
        s2, r, done, info = env.step(a)
        sample.append([s,a,r])
        s = s2
        #if done:
        #    break
    return discount_reward(sample)
    
def discount_reward(sample):
    discount_r = 0
    gamma = 1
    for i in reversed(range(len(sample))):
        discount_r = sample[i][2] + gamma * discount_r
        sample[i][2] = discount_r
    return sample 

def policy(s,w):
    phi = rbf.get_features(s)
    mu = (phi.T*w).item(0)
    return np.array([mu])

def REINFORCE(fixed_w, num_episodes=1):
    alpha = 0.001
    w = fixed_w
    for e in range(num_episodes):
        steps = sampling(fixed_w)
        for s,a,vt in steps:
            w = w + alpha*likelihood_function(s,a,w)*vt
    return w    


if not len(sys.argv) > 1:
    assert False, 'missing argument'
        
num_base_func = 5*5*12*1+1
num_iterations = 500
env = gym.make('Pendulum-v0')
rbf = RBF(env, 0.5, num_base_func)
np.seterr(over='ignore')

if str(sys.argv[1]) == 'train':
    best_r = -10000
    w = np.matrix(np.random.rand(num_base_func,1))
    for l in range(num_iterations):
        print str(l+1) + '/'+ str(num_iterations)
        w = REINFORCE(w)
        r = record(l,w)
        if r >= best_r:
            best_r = r
            np.save('iteration'+str(l)+'.npy',w)
    print 'finish training'
    np.save('saved_weight.npy',w)

elif str(sys.argv[1]) == 'test':
    if not len(sys.argv) > 2: assert False, 'missing .npy file'
    w = np.load(str(sys.argv[2]))
    test(w, episode=10, rendering=True)

else:
    assert False, 'unknown argument'
