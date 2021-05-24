import pandas as pd
from LearningMethods.correlation_evaluation import SignificantCorrelation
from LearningMethods.textreeCreate import create_tax_tree
from Plot.taxtreeDraw import draw_tree
import Plot.plot_positive_negative_bars as PP
import Plot.plot_real_and_shuffled_hist as PPR
from matplotlib.pyplot import Axes


class CorrelationFramework:
    def __init__(self, x: pd.DataFrame, y: pd.Series, **kwargs):
        self.x = x.copy()
        self.y = y.copy()

        self.sc = SignificantCorrelation(self.x, self.y, **kwargs)
        self.correlation_tree = create_tax_tree(self.sc.get_real_correlations())
        self.plot = _CorrelationPlotter(self.sc, self.correlation_tree)


class _CorrelationPlotter:
    def __init__(self, significant_correlation, correlation_tree):
        self.significant_correlation = significant_correlation
        self.correlation_tree = correlation_tree

    def plot_graph(self, threshold=0.0):
        draw_tree(self.correlation_tree, threshold=threshold)

    def plot_positive_negative_bars(self, ax: Axes, percentile, last_taxonomic_levels_to_keep=2, **kwargs):
        significant_bacteria = self.significant_correlation.get_most_significant_coefficients(percentile=percentile)
        if last_taxonomic_levels_to_keep is not None:
            significant_bacteria.index = [
                str([h.strip(" gs0_1").capitalize() for h in i.split(";")][-2:]).replace("[", "").replace("]", "").replace("\'","")
                for i in significant_bacteria.index]
        return PP.plot_positive_negative_bars(ax, significant_bacteria, **kwargs)

    def plot_real_and_shuffled_hist(self, ax: Axes, **kwargs):
        return PPR.plot_real_and_shuffled_hist(ax, self.significant_correlation.coeff_df['real'],
                                               self.significant_correlation.coeff_df.drop('real',
                                                                                          axis=1).values.flatten()
                                               , **kwargs)
