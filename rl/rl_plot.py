import argparse
import numpy as np
from omegaconf import OmegaConf
from matplotlib import pyplot as plt
import os
from celluloid import Camera
from utils import transform


def main(args):
    config = OmegaConf.load(args.config_path)
    log_list = []
    with os.scandir(config.env_config.log_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name[:6] == "envlog":
                log_list.append(entry.path)
                
    log = log_list[0]
    training_arr = np.loadtxt(log, delimiter=",", dtype=np.float32).T
    reward, done = training_arr[:2]
    position = training_arr[2:5].T
    
    done_indices = [-1] + np.nonzero(done)[0].tolist()
    
    if len(done_indices) < 2:
        print("There are no episode that done")
        return

    for i in range(len(done_indices) - 1):
        start_idx = done_indices[i]+1
        done_idx = done_indices[i+1]+1
        
        fig = plt.figure(figsize=(5,5))
        camera = Camera(fig)
        ax = plt.axes(projection="3d")
        for j in range(start_idx, done_idx, (done_idx - start_idx) // args.n_frames):
            ax.scatter(*config.env_config.goal_pos, color="red", label="goal")
            ax.text(*config.env_config.goal_pos, "goal")
             
            # position_real = list(map(
            #     transform, position[j], (
            #         config.env_config.obs_bound_agent_x, 
            #         config.env_config.obs_bound_agent_y, 
            #         config.env_config.obs_bound_agent_z    
            #     ), (
            #         config.env_config.obs_bound_real_x, 
            #         config.env_config.obs_bound_real_y, 
            #         config.env_config.obs_bound_real_z
            #     )
            # ))
            
            ax.scatter(*position[j], color="blue", label="agent")
            ax.text(*position[j], "agent")
            camera.snap()
        animation = camera.animate(interval=100, blit=True)
        animation.save(f"rl_{i}.gif")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="./conf.yaml")
    parser.add_argument("--n_frames", type=int, default=100)
    main(parser.parse_args())