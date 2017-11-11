import numpy as np

class RBF(object):
    def __init__(self, env, sigma, num_base_func):
        self.sigma = sigma
        self.num_base_func = num_base_func
        self.centers = self.MakeCenters(env)

    def RadialBasisFunction(self, state, center, sigma):
        diff = state - center
        diff = np.dot(diff,diff) #dot product of self = (euclidean dist)^2 since norm = root(dot product) = euclidean dist
        return np.exp(-0.5*diff/sigma**2)

    def MakeCenters(self,env):
        s_max = env.observation_space.high
        s_min = env.observation_space.low
        x_pos = np.linspace(s_min[0],s_max[0],7)
        y_pos = np.linspace(s_min[1],s_max[1],7)
        th_vel = np.linspace(s_min[1],s_max[1],12)
        
        return self.cartesian([x_pos, y_pos, th_vel])

    def cartesian(self, arrays, out=None):
        arrays = [np.asarray(x) for x in arrays]
        dtype = arrays[0].dtype
        n = np.prod([x.size for x in arrays])
        if out is None:
            out = np.zeros([n,len(arrays)], dtype=dtype)
        m = n / arrays[0].size
        out[:,0] = np.repeat(arrays[0], m)
        if arrays[1:]:
            self.cartesian(arrays[1:], out=out[0:m,1:])
            for j in xrange(1,arrays[0].size):
                out[j*m:(j+1)*m, 1:] = out[0:m,1:]
        return out

    def get_features(self, state):
        phi_list = []
        for i in range(self.num_base_func-1):
            phi = np.array([self.RadialBasisFunction(state, self.centers[i],self.sigma)])
            phi_list.append(phi)
        phi_list.append(np.array([1]))
        return np.matrix(np.array(phi_list))
