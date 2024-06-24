import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_df = pd.read_csv("dashboard/all_data.csv")

def mean_air_quality(df):
    mean_air = all_df.groupby('station')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()
    return mean_air

def best_air_quality(df):
    mean_air = mean_air_quality(df)
    best_air = mean_air.sort_values(by='PM2.5').head(5)
    return best_air

def worst_air_quality(df):
    mean_air = mean_air_quality(df)
    worst_air = mean_air.sort_values(by='PM2.5', ascending=False).head(5)
    return worst_air

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
        Air Quality &#x1F32C
    </h1>
    """, 
    unsafe_allow_html=True
)

st.dataframe(filtered_df)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

best_air_df = best_air_quality(filtered_df)
sns.barplot(x=best_air_df.index, y=best_air_df['PM2.5'], palette=colors, ax=ax[0])
ax[0].set_ylabel('PM2.5')
ax[0].set_xlabel("Station")
ax[0].set_title("Best Air Quality")
ax[0].tick_params(axis='x', rotation=45)

worst_air_df = worst_air_quality(filtered_df)
sns.barplot(x=worst_air_df.index, y=worst_air_df['PM2.5'], palette=colors, ax=ax[1])
ax[1].set_ylabel('PM2.5')
ax[1].set_xlabel("Station")
ax[1].set_title("Worst Air Quality")
ax[1].tick_params(axis='x', rotation=45)

st.pyplot(fig)