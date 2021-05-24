from LearningMethods.CorrelationFramework import CorrelationFramework
import matplotlib.pyplot as plt
import pandas as pd

def use_corr_framwork(X: pd.DataFrame, y, title=None, folder=""):
    cf = CorrelationFramework(X, y)

    fig1 = plt.figure(figsize=(12, 12))
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    # ax3 = plt.subplot(2, 3, 3)
    ax4 = plt.subplot(2, 1, 2)

    positive_dict = {'color': 'green', 'height': 0.8}
    negative_dict = {'color': 'red', 'height': 0.8}
    cf.plot.plot_positive_negative_bars(ax1, 1, positive_dict=positive_dict, negative_dict=negative_dict)
    real_hist_dict = {'bins': 30, 'color': 'g', 'label': 'Real values', 'density': True, 'alpha': 0.5}
    shuffled_hist_dict = {'bins': 30, 'color': 'b', 'label': 'Shuffled values', 'density': True, 'alpha': 0.5
                          }
    cf.plot.plot_real_and_shuffled_hist(ax2, real_hist_dict=real_hist_dict, shuffled_hist_dict=shuffled_hist_dict)
    cf.plot.plot_graph(0.5)
    # ax4)

    if title is not None:
        fig1.suptitle(title, fontsize=16)

    fig1.tight_layout()
    fig1.show()
    fig1.savefig(f"{folder}/{title}.svg")