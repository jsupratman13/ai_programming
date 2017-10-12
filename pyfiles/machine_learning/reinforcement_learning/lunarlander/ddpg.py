import numpy as np
import random
import gym
from keras.models import model_from_json, Model
import tensorflow as tf
import json

from actor import ActorNetwork
from critic import CriticNetwork
from replay import ReplayBuffer
from noise import Ornstein_Uhlenbeck

print 'initialize parameters'
buffer_size = 1000000
batch_size = 64
gamma = 0.99
tau = 0.001
actor_alpha = 0.0001
critic_alpha = 0.001
num_episode = 5000
epsilon = 1
min_epsilon = 0.01

env = gym.make('LunarLander-v2')
num_action = env.action_space.n
num_state = env.observation_space.shape[0]

np.random.seed(123)

sess = tf.Session()
from keras import backend as K
K.set_session(sess)

actor = ActorNetwork(sess, num_state, num_action, batch_size, tau, actor_alpha)
critic = CriticNetwork(sess, num_state, num_action, batch_size, tau, critic_alpha)
buff = ReplayBuffer(buffer_size)

with open('actor_model.json', 'w') as json_file:
    json_file.write(actor.model.to_json())
with open('critic_model.json', 'w') as json_file:
    json_file.write(critic.model.to_json())

print 'start training'
best_r = -10000

actor.update_target_network()
critic.update_target_network()

try:
    for i in range(num_episode):
        total_reward = 0
        s = env.reset()
        s_t = np.hstack((s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]))
        while True:
            if epsilon > min_epsilon:
                epsilon *= 0.995
            loss = 0.0
            if np.random.rand() < epsilon:
                a = env.action_space.sample()
            else:
                a = actor.model.predict(s_t.reshape(1,s_t.shape[0]))
                a = max(num_action-1, min(num_action, int(round(a[0]))))

            s2, r, done, info = env.step(a)
            s2_t = np.hstack((s2[0],s2[1],s2[2], s2[3], s2[4], s2[5], s2[6], s[7]))
            buff.add(s_t, [a], r, s2_t, done)
            batch = buff.get_batch(batch_size)

            if len(batch) >= batch_size:
                states = np.asarray([e[0] for e in batch])
                actions = np.asarray([e[1] for e in batch])
                reward = np.asarray([e[2] for e in batch])
                new_states = np.asarray([e[3] for e in batch])
                dones = np.asarray([e[4] for e in batch])
                y_t = np.zeros(len(batch))
                
                target_q = critic.target_model.predict([new_states, actor.target_model.predict(new_states)])
                
                for k in range(len(batch)):
                    if dones[k]:
                        y_t[k] = reward[k]
                    else:
                        y_t[k] = reward[k] + gamma*target_q[k]
               
                loss += critic.model.train_on_batch([states,actions], y_t)
                
                a_for_grad = actor.model.predict(states)
                grads = critic.gradients(states,a_for_grad)
                actor.update_network(states,grads)

                actor.update_target_network()
                critic.update_target_network()

            total_reward += r
            s_t = s2_t

            if done:
                print 'episode: ' + str(i) + ' reward: ' + str(total_reward) + ' loss: ' + str(loss)
                if total_reward >= best_r:
                    best_r = total_reward
                    actor.model.save_weights('episode'+str(i)+'.hdf5', overwrite=True)
                    #actor.model.save_weights('actor_weight.hdf5', overwrite=True)
                    #critic.model.save_weights('critic_weight.hdf5', overwrite=True)
                break

except (KeyboardInterrupt, SystemExit):
    pass

actor.model.save_weights('episodefinal.hdf5', overwrite=True)
print 'finished, best reward is: ' + str(best_r)
