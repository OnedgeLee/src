from rl_env import RlEnv
import argparse
import numpy as np
import wandb
from ray.rllib.agents import sac
import ray
from omegaconf import OmegaConf

def main(args):
    config = OmegaConf.load(args.config_path)
    run_config = config.run_config
    agent_config = config.agent_config
    agent_config.env_config = config.env_config
    
    ray.init()
    
    if run_config.wandb:
        wandb.login()
        wandb.init(project="rl_rllib")
        
    
    trainer = sac.SACTrainer(env=RlEnv, config=agent_config)
    
    for _ in range(int(run_config.n_train)):
        info = trainer.train()
        log_info = {}
        log_info["timesteps_total"] = info["timesteps_total"]
        log_info["episode_reward_max"] = info["episode_reward_max"]
        log_info["episode_reward_min"] = info["episode_reward_min"]
        log_info["episode_reward_mean"] = info["episode_reward_mean"]
        log_info["episode_len_mean"] = info["episode_len_mean"]
        for k, v in info["info"]["learner"]["default_policy"]["learner_stats"].items():
            if not k == "model":
                log_info[k] = v
                
        cleaned_log_info = {k:v for k, v in log_info.items() if not np.isnan(v)}
        if run_config.wandb:
            wandb.log(cleaned_log_info)
            
        trainer.save(run_config.ckpt_dir)
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="./conf.yaml")
    main(parser.parse_args())
