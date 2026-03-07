# Hat Yai Air Quality Prediction Dashboard

## Dataset Source
The PM10 dataset is sourced from the Thailand open data portal operated by the Digital Government Development Agency (https://www.data.go.th/dataset/pm10). The dataset is provided by the Pollution Control Department Thailand and contains air quality measurements including PM10 concentrations.

For this project, synthetic data is used for demonstration purposes. To use real data:
1. Visit https://air4thai.pcd.go.th/webV2/download/
2. Select station 35t (Hat Yai Municipality Office)
3. Choose parameters: PM10 and TEMP (temperature)
4. Download the CSV file and place it in the `data/` folder as `pm10.csv`

## Project Objective
Build an interactive Machine Learning dashboard that:
- Visualizes historical air quality data for Hat Yai, Thailand
- Predicts future PM10 levels and temperature using AutoGluon
- Allows users to input parameters for custom predictions
- Displays air quality risk levels based on PM10 concentrations

## Technologies Used
- Python
- Dash (Plotly Dash) for the web dashboard
- AutoGluon for automated machine learning
- Pandas for data processing
- Plotly for interactive graphs
- CSS for styling

## Project Structure
```
air-quality-dashboard/
│
├── data/
│   pm10.csv                 # Air quality dataset
│   processed_data.csv       # Processed dataset after cleaning
│
├── models/
│   trained_model/
│       pm10_model/          # Trained AutoGluon model for PM10 prediction
│       temp_model/          # Trained AutoGluon model for temperature prediction
│
├── assets/
│   style.css                # CSS styles for the dashboard
│
├── app.py                   # Main Dash application
├── data_processing.py       # Data cleaning and preprocessing script
├── train_model.py           # Model training script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Installation and Setup

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Process the data:
   ```
   python data_processing.py
   ```
4. Train the models:
   ```
   python train_model.py
   ```
5. Run the dashboard:
   ```
   python app.py
   ```

The dashboard will be available at http://127.0.0.1:8050/

## Features

### Historical Data Visualization
- PM10 concentration trends over time
- Monthly average PM10 levels

### Machine Learning Predictions
- AutoGluon regression models for PM10 and temperature prediction
- Feature importance analysis
- Prediction accuracy visualization

### User Prediction Panel
- Input current PM10, previous day PM10, month, and day of week
- Get predictions for next day's PM10 and temperature

### Air Quality Risk Indicator
- Real-time risk assessment based on PM10 levels:
  - Good: 0-50 µg/m³
  - Moderate: 51-100 µg/m³
  - Unhealthy: 101-150 µg/m³
  - Dangerous: >150 µg/m³

## Data Processing
The data processing includes:
- Date conversion and station filtering
- Missing value removal
- Outlier detection and removal using IQR method
- Feature engineering: time features (month, day of week) and lag features
- Target variable creation for next-day predictions

## Model Training
Two separate AutoGluon TabularPredictor models are trained:
1. PM10 prediction model using PM10 values, lags, month, and day of week
2. Temperature prediction model using temperature values, lags, month, and day of week

## Contributing
This project is set up for Git version control. Ensure all changes are committed with clear messages.

## License
This project uses data from the Thailand open data portal. Please refer to their terms of use for data usage.
