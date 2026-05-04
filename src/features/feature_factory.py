import pandas as pd

class FeatureFactory:
    """
    Centralized factory for all ML features. 
    Now includes Momentum and Trend features for V3 compatibility.
    """
    
    @staticmethod
    def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
        """Computes Z-Score and Rolling correlations."""
        # Volume Shock (30d)
        df['zscore_30d'] = df.groupby('id', group_keys=False).apply(
            lambda x: (x['total_volume'] - x['total_volume'].rolling(30).mean()) / x['total_volume'].rolling(30).std()
        )
        # Price-Volume Correlation
        df['price_vol_corr'] = df.groupby('id', group_keys=False).apply(
            lambda x: x['price'].rolling(30).corr(x['total_volume'])
        )
        return df

    @staticmethod
    def add_market_features(df: pd.DataFrame) -> pd.DataFrame:
        """Computes volatility, trend and calendar features."""
        # Volatility
        df['volatility_30d'] = df.groupby('id')['daily_variation'].rolling(30).std().reset_index(0, drop=True)
        
        # Trend (MA30)
        df['ma30'] = df.groupby('id')['price'].transform(lambda x: x.rolling(30).mean())
        df['price_vs_ma30'] = df['price'] / df['ma30']
        
        # Momentum (7d Change)
        df['price_change_7d'] = df.groupby('id')['price'].pct_change(7)
        
        # Calendar
        df['day_of_week'] = df['ds'].dt.dayofweek
        df['is_month_end'] = df['ds'].dt.is_month_end
        return df

    @staticmethod
    def create_features(df: pd.DataFrame) -> pd.DataFrame:
        """Full pipeline for feature generation."""
        df = FeatureFactory.add_volume_features(df)
        df = FeatureFactory.add_market_features(df)
        return df
