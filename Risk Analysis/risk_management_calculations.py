import numpy as np
import pandas as pd
from scipy.stats import norm, t
import math

class RiskManagementSoftware:
    def __init__(self, data_source=None):
        if data_source:
            try:
                self.data = pd.read_csv(data_source)
                self.preprocess_data()
            except FileNotFoundError:
                raise FileNotFoundError(f"Error: Data file not found at {data_source}")
            except pd.errors.ParserError:
                raise ValueError(f"Error: Could not parse the CSV file. Please check the format.")
            except Exception as e:
                raise Exception(f"An unexpected error occurred while loading the data: {e}")
        else:
            self.data = None

    def preprocess_data(self):
        if self.data is not None:
            for col in self.data.select_dtypes(include=np.number):
                self.data[col].fillna(self.data[col].mean(), inplace=True)

    def calculate_market_risk_parametric(self, asset_prices, confidence_level=0.95, method='normal'):
        if isinstance(asset_prices, list):
            asset_prices = pd.Series(asset_prices)

        if not isinstance(asset_prices, (pd.Series, np.ndarray)):
            raise TypeError("Asset prices must be a Pandas Series, NumPy array, or list.")

        if len(asset_prices) < 2:
            raise ValueError("Not enough data to calculate market risk.")

        returns = asset_prices.pct_change().dropna()

        if len(returns) == 0:
            raise ValueError("Not enough valid data points after calculating returns.")

        if method.lower() == 'normal':
            mean_return = returns.mean()
            std_dev = returns.std()
            z_score = norm.ppf(1 - confidence_level)
            var = mean_return + z_score * std_dev
        elif method.lower() == 't':
            df = len(returns) - 1
            mean_return = returns.mean()
            std_dev = returns.std()
            t_score = t.ppf(1 - confidence_level, df)
            var = mean_return + t_score * std_dev
        else:
            raise ValueError("Invalid method. Choose 'normal' or 't'.")

        return var


    def calculate_market_risk_historical(self, asset_prices, confidence_level=0.95):
        if isinstance(asset_prices, list):
            asset_prices = pd.Series(asset_prices)

        if not isinstance(asset_prices, (pd.Series, np.ndarray)):
            raise TypeError("Asset prices must be a Pandas Series, NumPy array, or list.")

        if len(asset_prices) < 2:
            raise ValueError("Not enough data to calculate market risk.")

        returns = asset_prices.pct_change().dropna()

        if len(returns) == 0:
            raise ValueError("Not enough valid data points after calculating returns.")

        var = returns.quantile(1 - confidence_level)
        return var

    def calculate_credit_risk(self, pd, lgd, ead):
        el = pd * lgd * ead
        return el

    def calculate_operational_risk(self, losses, percentile=0.95):
        if not isinstance(losses, (pd.Series, list, np.ndarray)):
            raise TypeError("Losses must be a pandas Series, list, or NumPy array.")

        if isinstance(losses, list):
            losses = np.array(losses)

        losses = losses[~np.isnan(losses) & np.isfinite(losses)]

        if len(losses) == 0:
            return np.nan

        op_risk_percentile = np.quantile(losses, percentile)
        return op_risk_percentile