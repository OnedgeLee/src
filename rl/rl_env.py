import numpy as np
import gym, os
from gym import spaces
from stable_baselines3 import SAC

from stable_baselines3 import TD3
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold



class rlEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, env_name, done_step):
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
        self.done_step = done_step
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
            print("\n\n\n\n DONE \n\n\n\n")
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

        if self.timesteps % 50 == 0 :
            print("reward", reward)
            print("max reward", self.max_rew)
            print("corresponding observation", self.corresponding_data)
        info = {}
        if done[0] :
            reward = 100
        return self.obs, reward, done, info


class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level.
    """
    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'rlEnv')
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

          # Retrieve training reward
          x, y = ts2xy(load_results(self.log_dir), 'timesteps')
          if len(x) > 0:
              # Mean training reward over the last 100 episodes
              mean_reward = np.mean(y[-100:])
              if self.verbose > 0:
                print(f"Num timesteps: {self.num_timesteps}")
                print(f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}")

              # New best model, you could save the agent here
              if mean_reward > self.best_mean_reward:
                  self.best_mean_reward = mean_reward
                  # Example for saving best model
                  if self.verbose > 0:
                    print(f"Saving new best model to {self.save_path}")
                  self.model.save(self.save_path)

        return True



log_dir = "/Users/shetshield/Desktop/res/220217/SAC_MDL/"
os.makedirs(log_dir, exist_ok=True)

eval_env = rlEnv('rlSAC', 1e4)
# env = Monitor(env, log_dir)

callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=-0.02, verbose=1)
eval_callback = EvalCallback(eval_env, callback_on_new_best=callback_on_best, verbose=1)


# n_actions = env.action_space.shape[-1]

# action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.0 * np.ones(n_actions))
model = SAC("MlpPolicy", eval_env, verbose=1)
# model = SAC("MlpPolicy", env).learn(2e4)

# callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)

timesteps = 3e4
model.learn(total_timesteps=int(timesteps), callback=eval_callback)

obsv = model.env.reset()
res = list()
a = eval_env.action_space
print(a)
print(a.is_bounded())
# img = model.env.render(mode='rgb_array')
max_rew = -float('inf')
for i in range(1000):
    action, _ = model.predict(obsv)
    obsv, rew, done ,_ = model.env.step(action)
    res.append([obsv[0][0], obsv[0][1]])
    print(rew[0], obsv[0])
    if done[0] :
        # res = obsv[0]
        break
    # img = model.env.render(mode='rgb_array')
'''
f = open("/Users/shetshield/Desktop/res/220217/SAC_t_160.txt", 'w')
_res = str()
for el in res :
    _res = _res + str(el) + "," + "\n"
f.write(_res)
f.close()
'''
print(res[-2])