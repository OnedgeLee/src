import numpy as np
import gym, os
from gym import spaces
import csv
from utils import transform

class RlEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, env_conf):
        self.env_conf = env_conf
        self.done_step = env_conf["done_step"]
        self.log_dir = env_conf["log_dir"]
        self.log_path = os.path.join(self.log_dir, f"envlog_{os.getpid()}.csv")
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.goal_pos = np.array(env_conf["goal_pos"], dtype=np.float32)
        self.init_pos = np.array(env_conf["init_pos"], dtype=np.float32)
        self.goal_threshold = env_conf["goal_threshold"]
        
        self.obs_bound_real = np.stack([env_conf["obs_bound_real_x"], env_conf["obs_bound_real_y"], env_conf["obs_bound_real_z"]], axis=-1).astype(np.float32)
        self.obs_bound_norm = np.stack([env_conf["obs_bound_agent_x"], env_conf["obs_bound_agent_y"], env_conf["obs_bound_agent_z"]], axis=-1).astype(np.float32)
        self.act_bound_real = np.stack([env_conf["act_bound_real_x"], env_conf["act_bound_real_y"], env_conf["act_bound_real_z"]], axis=-1).astype(np.float32)
        self.act_bound_norm = np.stack([env_conf["act_bound_agent_x"], env_conf["act_bound_agent_y"], env_conf["act_bound_agent_z"]], axis=-1).astype(np.float32)

        self.observation_space = spaces.Box(low=self.obs_bound_norm[0], high=self.obs_bound_norm[1], shape=(3,), dtype=np.float32)
        self.action_space = spaces.Box(low=self.obs_bound_norm[0], high=self.obs_bound_norm[1], shape=(3,), dtype=np.float32)

        self.goal_pos_norm = transform(self.goal_pos, self.obs_bound_real, self.obs_bound_norm)
        
        self.reward_range = (-float('inf'), float('inf'))
        self.metadata = {'render.modes': ['human']}
        self.spec = None
        
        self.timesteps = 0
        self.prev = 0
        self.max_rew = -float('inf')

    def reset(self):
        self.obs = self.init_pos
        self.obs_norm = transform(self.obs, self.obs_bound_real, self.obs_bound_norm)
        self.timesteps = 0
        return self.obs_norm

    def render(self):
        pass

    def step(self, action_norm):
        self.timesteps += 1
        done = np.array([False], dtype=bool)
        if self.timesteps >= self.done_step:
            done = np.array([True], dtype=bool)
        
        
        action = transform(action_norm, self.act_bound_norm, self.act_bound_real)
        self.next_obs = self.obs + action
        self.next_obs_norm = transform(self.obs, self.obs_bound_real, self.obs_bound_norm)
            
        distance = np.linalg.norm(self.obs - self.goal_pos)
        next_distance = np.linalg.norm(self.next_obs - self.goal_pos)
        
        rew_distance = distance - next_distance
        reward = rew_distance
        
        if np.linalg.norm(np.array(self.obs - self.goal_pos)) < self.goal_threshold:
            reward = 1
            done = np.array([True], dtype=bool)
        
        if not self.observation_space.contains(self.next_obs_norm):
            self.next_obs_norm = np.clip(self.next_obs_norm, 0, 1)
            self.next_obs = transform(self.next_obs_norm, self.obs_bound_norm, self.obs_bound_real)
            reward = -1
            done = np.array([True], dtype=bool)
        
        if reward > self.max_rew :
            self.max_rew = reward
            
        info = {}
        
        self.obs = self.next_obs
        self.obs_norm = self.next_obs_norm
        
        with open(self.log_path, "a") as f:
            writer = csv.writer(f)
            writer.writerow([reward, int(done[0]), *self.obs, *action])
        
        return self.obs_norm, reward, done, info

