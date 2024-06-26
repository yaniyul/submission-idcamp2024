import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

all_df = pd.read_csv("dashboard/all_data.csv")

def corr_1(df):
    columns_relevan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']
    df_subset = df[columns_relevan]

    correlation = df_subset.corr()
    return correlation

def regression_1(df):
    X = df[['TEMP', 'PRES', 'DEWP', 'RAIN']]
    y = df['PM2.5']

    X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train_1, y_train_1)

    y_pred_1 = model.predict(X_test_1)

    mse = mean_squared_error(y_test_1, y_pred_1)
    r2 = r2_score(y_test_1, y_pred_1)
    return mse, r2

def dongsi_station(df):
    df_dongsi = all_df[all_df['station'] == 'Dongsi']
    df_dongsi['datetime'] = pd.to_datetime(df_dongsi[['year', 'month', 'day', 'hour']])
    df_dongsi.set_index('datetime', inplace=True)
    df_dongsi = df_dongsi[['PM2.5']]
    df_dongsi = df_dongsi.asfreq('H')
    df_dongsi = df_dongsi.interpolate()
    return df_dongsi

def regression_2(df):
    df_dongsi['target'] = df_dongsi['PM2.5'].shift(-1)
    df_dongsi.dropna(inplace=True)

    X_2 = df_dongsi[['PM2.5']]
    y_2 = df_dongsi['target']

    X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_2, y_2, test_size=0.2, shuffle=False)

    model_2 = LinearRegression()
    model_2.fit(X_train_2, y_train_2)

    y_pred_2 = model_2.predict(X_test_2)

    mse_2 = mean_squared_error(y_test_2, y_pred_2)
    return model_2, X_test_2, y_test_2, y_pred_2, mse_2

def dongsi_predict(df):
    forecast_steps = 24 * 7
    last_value = X_test_2.iloc[-1].values.reshape(1, -1)
    
    predictions = []
    for _ in range(forecast_steps):
        next_predict = model_2.predict(last_value)[0]
        predictions.append(next_predict)
        last_value = np.array([[next_predict]])

    future_dates = pd.date_range(start=y_test_2.index[-1], periods=forecast_steps + 1, inclusive='right')
    forecast_df = pd.DataFrame(predictions, index=future_dates, columns=['PM2.5'])
    return forecast_df

all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day']])
all_df.set_index('datetime', inplace=True)

min_date = all_df.index.min().date()
max_date = all_df.index.max().date()

with st.sidebar:
    stations = all_df['station'].unique()
    selected_stations = st.multiselect(
        'Select Station', 
        options=stations,
    )

    start_date, end_date = st.date_input(
        label='Time Span', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

filtered_df = all_df[(all_df.index >= start_date) & (all_df.index <= end_date) & (all_df['station'].isin(selected_stations))]
filtered_df = filtered_df.drop(columns=['No', 'year', 'month', 'day'])

st.markdown(
    """
    <h1 style='text-align: center;'>
        Air Quality Table &#x1F32C
    </h1>
    """, 
    unsafe_allow_html=True
)

st.dataframe(filtered_df)

st.markdown(
    """
    <h3 style='text-align: center;'>
        Relationship between TEMP, PRES, DEWP and RAIN with Air Quality
    </h3>
    """, 
    unsafe_allow_html=True
)

correlation = corr_1(all_df)
mse, r2 = regression_1(all_df)

st.write("Mean Squared Error : ", mse)
st.write("R-Squared : ", r2)

plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation between Parameters')
st.pyplot(plt)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='TEMP', y='PM2.5', data=all_df)
plt.title('Temperature vs PM2.5')
plt.xlabel('Temperature')
plt.ylabel('PM2.5')
st.pyplot(plt)

st.markdown(
    """
    <h3 style='text-align: center;'>
        Dongsi Station Air Quality for the Next 7 Days
    </h3>
    """, 
    unsafe_allow_html=True
)

df_dongsi = dongsi_station(all_df)
model_2, X_test_2, y_test_2, y_pred_2, mse_2 = regression_2(df_dongsi)
forecast_df = dongsi_predict(all_df)

plt.figure(figsize=(12, 6))
plt.plot(y_test_2.index, y_test_2, label='Actual')
plt.plot(y_test_2.index, y_pred_2, label='Predicted', linestyle='--')
plt.title('Actual vs Predicted')
plt.xlabel('Date')
plt.ylabel('PM2.5')
plt.legend()
st.pyplot(plt)

plt.figure(figsize=(12, 6))
plt.plot(df_dongsi.index, df_dongsi['PM2.5'], label='Historical PM2.5')
plt.plot(forecast_df.index, forecast_df['PM2.5'], label='Forecasted PM2.5', linestyle='--')
plt.xlabel('Date')
plt.ylabel('PM2.5')
plt.title('Historical and Forecasted PM2.5 in Dongsi')
plt.legend()
st.pyplot(plt)