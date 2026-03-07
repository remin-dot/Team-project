from autogluon.tabular import TabularPredictor
import pandas as pd

def train_pm10_model(data_path, save_path):
    df = pd.read_csv(data_path)
    
    # Features for PM10 prediction
    features = ['pm10', 'pm10_lag1', 'pm10_lag2', 'month', 'day_of_week']
    target = 'pm10_next_day'
    
    # Split data (simple split, for demo)
    train_data = df[features + [target]]
    
    # Train model
    predictor = TabularPredictor(label=target, path=save_path).fit(train_data)
    
    return predictor

def train_temp_model(data_path, save_path):
    df = pd.read_csv(data_path)
    
    # Features for temperature prediction (using similar features)
    features = ['temperature', 'temp_lag1', 'temp_lag2', 'month', 'day_of_week']
    target = 'temp_next_day'
    
    train_data = df[features + [target]]
    
    predictor = TabularPredictor(label=target, path=save_path).fit(train_data)
    
    return predictor

if __name__ == "__main__":
    data_path = 'data/processed_data.csv'
    
    # Train PM10 model
    pm10_model = train_pm10_model(data_path, 'models/trained_model/pm10_model')
    
    # Train temperature model
    temp_model = train_temp_model(data_path, 'models/trained_model/temp_model')
    
    print("Models trained and saved.")