import numpy as np
import gym, os
from gym import spaces
import csv

class RlEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, env_conf):
        self.log_dir = env_conf["log_dir"]
        self.done_step = env_conf["done_step"]
        
        log_path = os.path.join(self.log_dir, "envlog.csv")
        if os.path.exists(log_path):
            os.remove(log_path)
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.ob_lx = -60
        self.ob_hx = 60
        self.ob_lz = -170
        self.ob_hz = 170
        self.ob_ly = -60
        self.ob_hy = 60
        self.pos_thr = 0.01

        obs_lstate = np.array([-1.0, -1.0, -1.0], dtype=np.float32)
        obs_hstate = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        actlx = (-1 - self.ob_lx) / (self.ob_hx - self.ob_lx) * 2 - 1
        acthx = (1 - self.ob_lx) / (self.ob_hx - self.ob_lx) * 2 - 1
        actlz = (-1 - self.ob_lz) / (self.ob_hz - self.ob_lz) * 2 - 1
        acthz = (1 - self.ob_lz) / (self.ob_hz - self.ob_lz) * 2 - 1
        actly = (-1 - self.ob_ly) / (self.ob_hy - self.ob_ly) * 2 - 1
        acthy = (1 - self.ob_ly) / (self.ob_hy - self.ob_ly) * 2 - 1


        print(actlx, acthx, actlz, acthz, actly, acthy)
        act_lstate = np.array([actlx, actly, actlz], dtype=np.float32)
        act_hstate = np.array([acthx, acthy, acthz], dtype=np.float32)


        self.timesteps = 0
        self.observation_space = spaces.Box(low=obs_lstate, high=obs_hstate, shape=(3,), dtype=np.float32)
        self.action_space = spaces.Box(low=act_lstate, high=act_hstate, shape=(3,), dtype=np.float32)

        self.reward_range = (-float('inf'), float('inf'))
        self.metadata = {'render.modes': ['human']}
        self.spec = None
        self.prev = 0

        gpx = 40.0
        gpy = 30.0
        gpz = 160.0

        _gpx = (gpx - self.ob_lx)/(self.ob_hx - self.ob_lx) * 2 - 1
        _gpy = (gpy - self.ob_ly)/(self.ob_hy - self.ob_ly) * 2 - 1
        _gpz = (gpz - self.ob_lz)/(self.ob_hz - self.ob_lz) * 2 - 1
        self.gp = np.array([_gpx, _gpy, _gpz])
        self.max_rew = -float('inf')
        self.corresponding_data = list()


    def reset(self):
        ipx = 0.0
        ipy = 0.0
        ipz = 141.5
        _ipx = (ipx - self.ob_lx)/(self.ob_hx - self.ob_lx) * 2 - 1
        _ipy = (ipy - self.ob_ly)/(self.ob_hy - self.ob_ly) * 2 - 1
        _ipz = (ipz - self.ob_lz)/(self.ob_hz - self.ob_lz) * 2 - 1

        self.obs = np.array([_ipx, _ipy, _ipz], dtype=np.float32)
        self.timesteps = 0

        return self.obs

    def render(self):
        pass

    def step(self, action):
        self.timesteps += 1

        if self.timesteps == self.done_step or abs(self.obs[0] - self.gp[0]) < self.pos_thr and abs(self.obs[1] - self.gp[1]) < self.pos_thr and abs(self.obs[2] - self.gp[2]) < self.pos_thr:
            done = np.array([True], dtype=bool)
            # print("\n\n\n\n DONE \n\n\n\n")
        else:
            done = np.array([False], dtype=bool)
        actx = action[0]
        acty = action[1]
        actz = action[2]

        vec = self.obs + action - self.gp
        self.obs = self.obs + action

        rew_distance_penalty = -np.linalg.norm(vec)
        delta_dist_penalty = -abs(-rew_distance_penalty - self.prev)
        self.prev = -rew_distance_penalty
        rew_action_penalty  = -np.square(action).sum()

        # reward = 3*rew_distance_penalty + 2*delta_dist_penalty + 2*delta_x_penalty + 2*delta_z_penalty # + rew_action_penalty
        reward = 8 * rew_distance_penalty + 5 * delta_dist_penalty + 8 * rew_action_penalty  #+ 2 * delta_x_penalty + 2 * delta_z_penalty
        self.obs[0] = np.clip(self.obs[0], self.observation_space.low[0], self.observation_space.high[0])
        self.obs[1] = np.clip(self.obs[1], self.observation_space.low[1], self.observation_space.high[1])
        self.obs[2] = np.clip(self.obs[2], self.observation_space.low[2], self.observation_space.high[2])

        if reward > self.max_rew :
            self.max_rew = reward
            self.corresponding_data = [rew_distance_penalty, delta_dist_penalty, rew_action_penalty,
                                       self.gp[0], self.obs[0], self.gp[1], self.obs[1],
                                       self.gp[2], self.obs[2]]

        info = {}
        if done[0] :
            reward = 100
            
        # reward /= 100
        
        with open(os.path.join(self.log_dir, "envlog.csv"), "a") as f:
            writer = csv.writer(f)
            writer.writerow([reward, int(done[0]), *self.obs, *action])
        return self.obs, reward, done, info

