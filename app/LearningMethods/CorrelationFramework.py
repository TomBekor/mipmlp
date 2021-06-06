import pandas as pd
from LearningMethods.correlation_evaluation import SignificantCorrelation
import Plot.plot_positive_negative_bars as PP
import Plot.plot_real_and_shuffled_hist as PPR
from matplotlib.pyplot import Axes
import matplotlib.pyplot as plt


class CorrelationFramework:
    def __init__(self, x: pd.DataFrame, y: pd.Series, **kwargs):
        self.x = x.copy()
        self.y = y.copy()

        self.sc = SignificantCorrelation(self.x, self.y, **kwargs)
        self.plot = _CorrelationPlotter(self.sc)


class _CorrelationPlotter:
    def __init__(self, significant_correlation):
        self.significant_correlation = significant_correlation

    def plot_positive_negative_bars(self, ax: Axes, percentile, last_taxonomic_levels_to_keep=2, **kwargs):
        significant_bacteria = self.significant_correlation.get_most_significant_coefficients(percentile=percentile)
        if last_taxonomic_levels_to_keep is not None:
            significant_bacteria.index = [str([h[4:].strip("_").capitalize() for h in i.split(";")][-2:])
                    .replace("[", "").replace("]", "").replace("\'", "") for i in significant_bacteria.index]
        return PP.plot_positive_negative_bars(ax, significant_bacteria, **kwargs)

    def plot_real_and_shuffled_hist(self, ax: Axes, **kwargs):
        return PPR.plot_real_and_shuffled_hist(ax, self.significant_correlation.coeff_df['real'],
                                               self.significant_correlation.coeff_df.drop('real',
                                                            axis=1).values.flatten(), **kwargs)

def use_corr_framwork(X: pd.DataFrame, y, title=None, folder=""):
    cf = CorrelationFramework(X, y)

    fig1 = plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    positive_dict = {'color': 'green', 'height': 0.8}
    negative_dict = {'color': 'red', 'height': 0.8}
    cf.plot.plot_positive_negative_bars(ax1, 1, positive_dict=positive_dict, negative_dict=negative_dict)
    real_hist_dict = {'bins': 30, 'color': 'g', 'label': 'Real values', 'density': True, 'alpha': 0.5}
    shuffled_hist_dict = {'bins': 30, 'color': 'b', 'label': 'Shuffled values', 'density': True, 'alpha': 0.5}
    cf.plot.plot_real_and_shuffled_hist(ax2, real_hist_dict=real_hist_dict, shuffled_hist_dict=shuffled_hist_dict)

    if title is not None:
        fig1.suptitle(title.replace("_", " "), fontsize=16)

    fig1.tight_layout()
    fig1.savefig(f"{folder}/{title}.svg")
