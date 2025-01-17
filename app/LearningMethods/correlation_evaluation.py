import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats

class SignificantCorrelation:
    def __init__(self, x_df: pd.DataFrame, y: pd.Series, shuffle_times: int = 10,random_seed = None, **kwargs):
        if random_seed is not None:
            np.random.seed(random_seed)
        # Remove nan from y and the corresponding rows from x_df ,please notice that the object requires x_df and y
        # to have the same index.
        y = y.dropna()
        x_df = x_df.loc[y.index]

        self.x_df = x_df
        self.y = y
        self.shuffle_times = shuffle_times
        self.args_for_correlation = kwargs
        self.real_col_name = 'real'

        self.shuffled_y = self._create_shuffled_df()
        self.coeff_df = self.compute_correlation()

    def _create_shuffled_df(self):
        permutation_df = self.y.to_frame(self.real_col_name)
        for shuffle_number in range(self.shuffle_times):
            # assign new columns to the dataframe, each one is a different permutation of the target
            permutation_df[str(shuffle_number)] = np.random.permutation(permutation_df[self.real_col_name].values,)
        return permutation_df

    def get_most_significant_coefficients(self, percentile):

        fake_coeff = self.coeff_df.drop(self.real_col_name,axis = 1).values.flatten()
        real_coeff = self.coeff_df[self.real_col_name]

        upper_bound = np.percentile(fake_coeff, 100 - percentile)
        lower_bound = np.percentile(fake_coeff, percentile)
        real_upper_significant_coefficients = real_coeff[real_coeff >= upper_bound]
        real_lower_significant_coefficients = real_coeff[real_coeff <= lower_bound]

        all_real_significant_coefficients = pd.concat(
            [real_upper_significant_coefficients, real_lower_significant_coefficients])
        return all_real_significant_coefficients

    def compute_correlation(self):
        all_variables_df = self.x_df.join(self.shuffled_y)
        all_variables_corr_df = all_variables_df.corr(method='spearman')

        return all_variables_corr_df.iloc[0:self.x_df.shape[1],-self.shuffled_y.shape[1]:]

    def get_real_correlations(self):
        return self.coeff_df[self.real_col_name]
