import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from LearningMethods.utilis import set_default_parameters


def plot_positive_negative_bars(ax: plt.Axes, values: pd.Series, positive_dict: dict = None,
                                negative_dict: dict = None, title='Significant Spearman Correlation',
                                x_label='Spearman Correlation'):
    if positive_dict is None:
        positive_dict = {}
    if negative_dict is None:
        negative_dict = {}

    default_positive_dict = {'color': 'green', 'height': 0.2}
    default_negative_dict = {'color': 'red', 'height': 0.2}
    positive_dict = set_default_parameters(positive_dict, default_positive_dict)
    negative_dict = set_default_parameters(negative_dict, default_negative_dict)

    sorted_values = values.sort_values()

    y_position = np.arange(len(sorted_values))
    positive_values = sorted_values.apply(lambda x: x if x >= 0 else 0)
    ax.barh(y_position, positive_values, **positive_dict)
    negative_values = sorted_values.apply(lambda x: x if x < 0 else 0)
    ax.barh(y_position, negative_values, **negative_dict)

    ax.set_yticks(y_position)
    ax.set_yticklabels(sorted_values.index)
    
    fat_bar_number = 5
    if len(y_position) < fat_bar_number:
        ax.set_ylim([i + np.sign(i)*(fat_bar_number - len(y_position)) for i in ax.get_ylim()])
    # ax.set_xlim((1,10))
    ax.set_title(title)
    ax.set_xlabel(x_label)
    return ax
