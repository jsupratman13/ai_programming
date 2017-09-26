import gym
import numpy as np
import math,sys
from features import RBF

def test(w, episode=100, rendering=False):
    reward = []
    for e in range(episode):
        s = env.reset()
        rt = 0
        while True:
            if rendering: env.render()
            a = policy(s,w)
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

def guassian_policy(s,a,w):
    sigma = 0.5
    phi = rbf.get_features(s)
    a = a.item(0) + 2.0
    mu = (phi.T*w).item(0)
    return ((a-mu)*phi)/(sigma**2)

def sampling(w):
    sample = []
    s = env.reset()
    while True:
        a = policy(s,w)
        #a = env.action_space.sample()
        s2, r, done, info = env.step(a)
        sample.append([s,a,r])
        s = s2
        if done:
            break
    return sample 

def policy(s,w):
    sigma = 0.5
    phi = rbf.get_features(s)
    mu = (phi.T*w).item(0)
    s = s.item(0)
    action = np.exp(((s-mu)**2)/(2*sigma**2))
    return np.array([action - 2.0])

def REINFORCE(w, num_episodes=1):
    alpha = 0.001
    for e in range(num_episodes):
        steps = sampling(w)
        vt = 0
        for s,a,r in steps:
            vt += r 
            w = w + alpha*guassian_policy(s,a,w)*vt
    return w    


if not len(sys.argv) > 1:
    assert False, 'missing argument'
        
num_base_func = 7*7*12*1+1
num_iterations = 100
env = gym.make('Pendulum-v0')
rbf = RBF(env, 2, num_base_func)
np.seterr(over='ignore')

if str(sys.argv[1]) == 'train':
    w = np.matrix(np.random.rand(num_base_func,1))
    for l in range(num_iterations):
        print str(l+1) + '/'+ str(num_iterations)
        w = REINFORCE(w)
        record(l,w)
    print 'finish training'
    np.save('saved_weight.npy',w)

elif str(sys.argv[1]) == 'test':
    if not len(sys.argv) > 2: assert False, 'missing .npy file'
    w = np.load(str(sys.argv[2]))
    test(w, episode=10, rendering=True)

else:
    assert False, 'unknown argument'
