from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('tkagg')
from windrose import WindroseAxes
import numpy as np
import pandas as pd


def plot(path, dir_field_name, speed_field_name, use_percent=True, bins=None, radii=None, use_box=False,
         title=''):
    """
    @bins: number of bins, or a list of numbers. If not set, bins=6
    @radii: list if numbers
    """
    df = pd.read_csv(path, dtype={dir_field_name: np.float64, speed_field_name: np.float64})
    df.dropna()
    ax = WindroseAxes.from_ax(use_percentage_spoke=use_percent)
    plt.title(title)
    other_params = {}
    if bins is not None:
        other_params['bins'] = bins

    if radii is not None:
        if radii[0] != 0:  # we need one at the center
            radii.insert(0, 0)
        other_params['radii'] = radii

    if use_box:
        ax.box(df[dir_field_name], df[speed_field_name], **other_params)
    else:
        ax.bar(df[dir_field_name], df[speed_field_name], **other_params)

    ax.set_legend()
    plt.show()
