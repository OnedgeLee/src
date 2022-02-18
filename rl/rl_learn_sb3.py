from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import BaseCallback
import os
from rl_env import RlEnv
import argparse
import numpy as np
import wandb
from omegaconf import OmegaConf

class LoggerCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level.
    """

    def __init__(self, run_config, verbose: int=1):
        super(LoggerCallback, self).__init__(verbose)
        self.run_config = run_config
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        print(f"\t|Timestep\t|Rew_100\t|Rew_Best_Prev\t|N_Dones")
        os.makedirs(self.run_config.log_dir, exist_ok=True)
        os.makedirs(self.run_config.ckpt_dir, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls > 1:
            training_arr = np.loadtxt(os.path.join(self.run_config.log_dir, "envlog.csv"), delimiter=",", dtype=np.float32).T
            reward, done = training_arr[:2]
            obs = training_arr[2:5]
            action = training_arr[5:]
            if self.run_config.wandb:
                log_dict = {}
                log_dict["reward"] = reward[-1]
                # log_dict["n_dones"] = n_dones
                for i, obs_ in enumerate(obs):
                    log_dict[f"obs_{i}"] = obs_[-1]
                for i, action_ in enumerate(action):
                    log_dict[f"action_{i}"] = obs_[-1]
                wandb.log(log_dict)
        if self.n_calls % self.run_config.check_freq == 0 and self.n_calls > 0:
            if len(obs) > 0:
                mean_reward = np.mean(reward[-1024:])
                n_dones = np.sum(done)
                if self.verbose > 0:
                    print(f"\t|{self.num_timesteps}\t\t|{mean_reward:.2f}\t\t|{self.best_mean_reward:.2f}\t\t|{n_dones:.0f}")
                if mean_reward > self.best_mean_reward:
                    self.best_mean_reward = mean_reward
                    self.model.save(os.path.join(self.run_config.ckpt_dir, "model.pt"))
        return True


def main(args):
    config = OmegaConf.load(args.config_path)
    run_config = config.run_config
    run_config.log_dir = config.env_config.log_dir
    
    if run_config.wandb:
        wandb.login()
        wandb.init(project="rl_sb3")
    
    callback_ckpt = LoggerCallback(run_config=run_config)
    env = RlEnv(config.env_config)
    
    model = SAC("MlpPolicy", env, verbose=1)
    if run_config.resume:
        try:
            model.load(os.path.join(run_config.ckpt_dir, "model.pt"))
        except:
            print("Couldn't load from checkpoint, learn from scratch")
    model.learn(total_timesteps=run_config.n_train, callback=[callback_ckpt])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="./conf.yaml")
    main(parser.parse_args())
