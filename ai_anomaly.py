import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame):
    """
    Takes a DataFrame of expenses and returns the DataFrame with an 'is_anomaly' column.
    Expected columns: 'amount'
    """
    if df.empty or len(df) < 5:
        # Not enough data to reliably detect anomalies
        df['is_anomaly'] = False
        return df

    # We use Isolation Forest on the 'amount' to find unusually high or low spending
    # contamination=0.05 means we expect ~5% of transactions to be anomalies
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Fit the model
    df['anomaly_score'] = model.fit_predict(df[['amount']])
    
    # -1 means anomaly, 1 means normal
    df['is_anomaly'] = df['anomaly_score'] == -1
    
    return df
