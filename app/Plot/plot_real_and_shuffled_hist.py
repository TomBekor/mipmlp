import matplotlib.pyplot as plt
from LearningMethods.utilis import set_default_parameters
import numpy as np


def plot_real_and_shuffled_hist(ax: plt.Axes, real_values, shuffled_values, real_hist_dict=None,
                                shuffled_hist_dict=None, title='Histogram of real and shuffled spearman correlation',
                                x_label='Spearman Correlation', bin_num=30):
    if real_hist_dict is None:
        real_hist_dict = {}
    if shuffled_hist_dict is None:
        shuffled_hist_dict = {}

    default_real_dict = {'color': ['g', 'b'], 'label': ['Real values', 'Shuffled values'],
                         'density': [True, True]}

    # real_hist_dict = set_default_parameters(real_hist_dict, default_real_dict)
    # shuffled_hist_dict = set_default_parameters(shuffled_hist_dict, default_shuffled_dict)

    bins = np.linspace(min(real_values.min(), shuffled_values.min()), max(real_values.max(), shuffled_values.max()), bin_num)

    ax.hist([real_values, shuffled_values], bins, **default_real_dict)
    # ax.hist(shuffled_values, **shuffled_hist_dict)
    ax.set_title(title)
    ax.set_xlabel(x_label)

    ax.legend()
    return ax
