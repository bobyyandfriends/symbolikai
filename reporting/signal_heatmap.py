#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_signal_distribution(signals: pd.DataFrame):
    """
    Plot a heatmap showing the frequency of signals by day of week and hour of day.
    
    Expects 'signals' DataFrame to have a 'datetime' column (of type datetime)
    and a 'signal' column. The heatmap will use day-of-week (0=Monday,...,6=Sunday)
    on the y-axis and hour of day (0-23) on the x-axis.
    """
    # Ensure datetime column is of type datetime
    signals = signals.copy()
    signals['datetime'] = pd.to_datetime(signals['datetime'])
    
    # Extract day of week and hour
    signals['day_of_week'] = signals['datetime'].dt.dayofweek
    signals['hour'] = signals['datetime'].dt.hour
    
    # Create a pivot table counting signals per day and hour
    pivot = signals.pivot_table(index='day_of_week', columns='hour', values='signal', aggfunc='count', fill_value=0)
    
    # Create the heatmap using imshow
    plt.figure(figsize=(12, 6))
    plt.imshow(pivot, aspect='auto', cmap='viridis', origin='lower')
    plt.colorbar(label='Number of Signals')
    plt.title("Signal Distribution by Day of Week and Hour of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week (0=Mon, 6=Sun)")
    plt.xticks(ticks=np.arange(0, 24, 1), labels=np.arange(0, 24, 1))
    plt.yticks(ticks=np.arange(0, 7, 1), labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    plt.tight_layout()
    plt.show()

def plot_indicator_interaction_matrix(data: pd.DataFrame):
    """
    Plot a heatmap of correlations between numeric indicator columns and a numeric
    representation of the 'signal' column (if present).
    
    The function expects 'data' to include numeric indicator columns.
    If a 'signal' column exists (with categorical values like 'buy' and 'sell'),
    it converts it to a binary numeric column (buy=1, sell=-1, others=0) and includes
    it in the correlation matrix.
    """
    df = data.copy()
    # If 'signal' column exists, convert it to numeric (e.g., buy=1, sell=-1)
    if 'signal' in df.columns:
        def signal_to_numeric(val):
            if isinstance(val, str):
                if 'buy' in val.lower():
                    return 1
                elif 'sell' in val.lower():
                    return -1
            return 0
        df['signal_numeric'] = df['signal'].apply(signal_to_numeric)
    
    # Select only numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(corr, cmap='coolwarm', interpolation='none', aspect='auto')
    plt.colorbar(label='Correlation')
    plt.title("Indicator Interaction Matrix")
    # Set tick labels to column names
    ticks = np.arange(len(numeric_cols))
    plt.xticks(ticks, numeric_cols, rotation=45, ha='right')
    plt.yticks(ticks, numeric_cols)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage for plot_signal_distribution:
    import numpy as np
    from datetime import datetime, timedelta

    # Create dummy signals data:
    base_time = datetime(2022, 1, 1)
    dummy_signals = []
    for i in range(100):
        # Randomly pick a time within a day and a day offset
        dt = base_time + timedelta(days=np.random.randint(0, 7), hours=np.random.randint(0, 24))
        signal = np.random.choice(['buy', 'sell'])
        dummy_signals.append({'datetime': dt, 'signal': signal})
    signals_df = pd.DataFrame(dummy_signals)
    plot_signal_distribution(signals_df)
    
    # Example usage for plot_indicator_interaction_matrix:
    # Create dummy data with indicators and a signal column
    dummy_data = pd.DataFrame({
        'rsi': np.random.uniform(20, 80, size=50),
        'sma': np.random.uniform(90, 110, size=50),
        'momentum': np.random.randn(50),
        'signal': np.random.choice(['buy', 'sell'], size=50)
    })
    plot_indicator_interaction_matrix(dummy_data)
