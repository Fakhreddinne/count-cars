import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Load the data
file_path = 'cars_traffic_data_extended.xlsx'
df = pd.read_excel(file_path)

# Streamlit app title
st.title("Traffic Data Visualization")

# Create two columns for the first sections
col1, col2 = st.columns(2)

# Display data as a table in the first column
with col1:
    st.subheader("Traffic Data Table")
    st.dataframe(df)

# Display summary statistics in the second column
with col2:
    st.subheader("Traffic Data Statistics")
    total_up = df['NumberOfCarsGoingUpTheRoad'].sum()
    total_down = df['NumberOfCarsGoingDownTheRoad'].sum()
    avg_up = df['NumberOfCarsGoingUpTheRoad'].mean()
    avg_down = df['NumberOfCarsGoingDownTheRoad'].mean()

    st.metric("Total Cars Going Up", total_up)
    st.metric("Total Cars Going Down", total_down)
    st.metric("Average Cars Going Up per Day", f"{avg_up:.2f}")
    st.metric("Average Cars Going Down per Day", f"{avg_down:.2f}")

# Grouped stats by location
stats_by_location = df.groupby('Location').agg(
    Total_Up=('NumberOfCarsGoingUpTheRoad', 'sum'),
    Total_Down=('NumberOfCarsGoingDownTheRoad', 'sum'),
    Avg_Up=('NumberOfCarsGoingUpTheRoad', 'mean'),
    Avg_Down=('NumberOfCarsGoingDownTheRoad', 'mean')
).reset_index()

# Create two columns for the second sections
col3, col4 = st.columns(2)

# Display grouped stats in the first column
with col3:
    st.subheader("Traffic Stats by Location")
    st.dataframe(stats_by_location)

# Create and display the plot in the second column
with col4:
    st.subheader("Average Number of Cars per Location")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=stats_by_location.melt(id_vars='Location', value_vars=['Avg_Up', 'Avg_Down']),
        x='Location', y='value', hue='variable', ax=ax
    )

    ax.set_title("Average Number of Cars per Location")
    ax.set_ylabel("Average Number of Cars")
    ax.set_xlabel("Location")
    ax.legend(title="Direction", labels=["Going Up", "Going Down"])

    st.pyplot(fig)
