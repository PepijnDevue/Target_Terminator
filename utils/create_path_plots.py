import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.collections import LineCollection


def create_path_plots(
    folder_path: str, 
    observation_history: dict,
    env_data: dict,
    figs_stride: int=1
)-> None:
    """
    Create plots that display the path of the agent.

    It tries to draw background of the environment on the 
    figure. Above which it plots the x,y flight history of the agent.
    It colours this graph in accordance with the normalized reward 
    provided. It saves the figure in the provided folder. It does this
    for each of the runs in the observation history.

    @params:
        - folder_path (str): Path to output folder.
        If this folder does not exist, no new one will be made.
        - observation_history (dict): Dictionary containing list of 
        observations per iteration/run.
        - env_data (dict): Environment configuration.
            See config/default_env.yaml for more info.
            In theory, it only needs to contain the window dimensions
            and preferably the background data.
        - figs_stride (int): Stride for saving the figures.
    """
    obs_hist_iter = iter(observation_history.items())
    for iteration, observations in itertools.islice(
        obs_hist_iter, 0, None, figs_stride
    ):
        try:
            vertices = [(x, y, r) for (x, y, _, _), r, _, _, _ in observations]
            
            xs, ys, rewards = zip(*vertices)
            normalize_rewards = plt.Normalize(min(rewards), max(rewards))

            colour_map = plt.get_cmap('RdYlGn')

            points = np.array([xs, ys]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            # Create a LineCollection from the segments
            lc = LineCollection(
                segments, 
                cmap=colour_map, 
                norm=normalize_rewards
            )
            lc.set_array(np.array(rewards))
            
            fig, ax = plt.subplots()
            ax.add_collection(lc)
            ax.set_xlim(0, env_data["window_dimensions"][0])
            ax.set_ylim(0, env_data["window_dimensions"][1])
            ax.invert_yaxis()
            cbar = plt.colorbar(lc, ax=ax)
            cbar.set_label('Reward')
            ax.set_title(f"Flight path for iteration {iteration}.")

            # try to plot the backgrounds, if available
            # if any of these settings are missing, 
            # nothing will be plotted
            try:
                background_image = plt.imread(env_data["background"]["sprite"])
                ax.imshow(background_image)

            except KeyError:
                pass

            plt.savefig(f"{folder_path}/flight_path_it-{iteration}")
            plt.close(fig)
        
        # if any of the runs are empty, dont plot them
        except ValueError:
            continue