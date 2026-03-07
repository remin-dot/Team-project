import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter for Hat Yai station
    df = df[df['station'] == 'Hat Yai']
    
    # Remove missing PM10 values
    df = df.dropna(subset=['pm10'])
    
    # Remove extreme outliers for PM10 using IQR
    Q1 = df['pm10'].quantile(0.25)
    Q3 = df['pm10'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['pm10'] >= lower_bound) & (df['pm10'] <= upper_bound)]
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create time features
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
    
    # Create lag features for PM10
    df['pm10_lag1'] = df['pm10'].shift(1)
    df['pm10_lag2'] = df['pm10'].shift(2)
    
    # Create lag features for temperature
    df['temp_lag1'] = df['temperature'].shift(1)
    df['temp_lag2'] = df['temperature'].shift(2)
    
    # Create target columns
    df['pm10_next_day'] = df['pm10'].shift(-1)
    df['temp_next_day'] = df['temperature'].shift(-1)
    
    # Drop rows with NaN from lags or targets
    df = df.dropna()
    
    return df

if __name__ == "__main__":
    df = load_and_preprocess_data('data/pm10.csv')
    print(df.head())
    df.to_csv('data/processed_data.csv', index=False)