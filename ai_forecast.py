import pandas as pd
from prophet import Prophet
import warnings

# Suppress Prophet warnings
warnings.filterwarnings("ignore")

def forecast_expenses(df: pd.DataFrame, periods=30):
    """
    Takes a DataFrame with 'date' and 'amount' columns.
    Returns a DataFrame with forecasted spending for the next `periods` days.
    """
    if df.empty or len(df) < 10:
        return None # Not enough data

    # Group by date to get daily totals
    daily_df = df.groupby('date')['amount'].sum().reset_index()
    
    # Prophet requires columns to be named 'ds' (date) and 'y' (value)
    prophet_df = daily_df.rename(columns={'date': 'ds', 'amount': 'y'})
    
    model = Prophet(daily_seasonality=True, yearly_seasonality=False, weekly_seasonality=True)
    model.fit(prophet_df)
    
    # Create future dataframe
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Return just the relevant columns: date and predicted amount (yhat)
    result_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
        columns={'ds': 'date', 'yhat': 'predicted_amount'}
    )
    
    # Keep only the future predictions (where date is greater than max date in original data)
    max_date = daily_df['date'].max()
    # Ensure types match for comparison
    result_df['date'] = pd.to_datetime(result_df['date']).dt.date
    max_date = pd.to_datetime(max_date).date()
    
    future_predictions = result_df[result_df['date'] > max_date]
    
    return future_predictions
