import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'cars_traffic_data_extended.xlsx'
df = pd.read_excel(file_path)

# Streamlit app title
st.title("Traffic Data Visualization")

# Display data as a table
st.subheader("Traffic Data Table")
st.dataframe(df)

# Display summary statistics
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
st.subheader("Traffic Stats by Location")
stats_by_location = df.groupby('Location').agg(
    Total_Up=('NumberOfCarsGoingUpTheRoad', 'sum'),
    Total_Down=('NumberOfCarsGoingDownTheRoad', 'sum'),
    Avg_Up=('NumberOfCarsGoingUpTheRoad', 'mean'),
    Avg_Down=('NumberOfCarsGoingDownTheRoad', 'mean')
).reset_index()

st.dataframe(stats_by_location)

# Visualization Section
st.subheader("Traffic Data Visualizations")

# 1. Total Cars per Location
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(data=stats_by_location, x='Location', y='Total_Up', color='skyblue', label='Up')
sns.barplot(data=stats_by_location, x='Location', y='Total_Down', color='orange', label='Down')
ax1.set_title("Total Cars by Location")
ax1.set_ylabel("Number of Cars")
ax1.legend()
st.pyplot(fig1)

# 2. Daily Trends of Cars Going Up and Down
fig2, ax2 = plt.subplots(figsize=(10, 6))
for location in df['Location'].unique():
    df_location = df[df['Location'] == location]
    ax2.plot(df_location['Date'], df_location['NumberOfCarsGoingUpTheRoad'], label=f'{location} Up', marker='o')
    ax2.plot(df_location['Date'], df_location['NumberOfCarsGoingDownTheRoad'], label=f'{location} Down', marker='x')

ax2.set_title("Daily Traffic Trends by Location")
ax2.set_xlabel("Date")
ax2.set_ylabel("Number of Cars")
ax2.legend()
st.pyplot(fig2)

# 3. Distribution of Cars
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.histplot(df['NumberOfCarsGoingUpTheRoad'], kde=True, color='skyblue', label='Cars Going Up', ax=ax3)
sns.histplot(df['NumberOfCarsGoingDownTheRoad'], kde=True, color='orange', label='Cars Going Down', ax=ax3)
ax3.set_title("Distribution of Cars")
ax3.set_xlabel("Number of Cars")
ax3.legend()
st.pyplot(fig3)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'cars_traffic_data_extended.xlsx'
df = pd.read_excel(file_path)

# Streamlit app title
st.title("Traffic Data Visualization")

# Display data as a table
st.subheader("Traffic Data Table")
st.dataframe(df)

# Display summary statistics
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
st.subheader("Traffic Stats by Location")
stats_by_location = df.groupby('Location').agg(
    Total_Up=('NumberOfCarsGoingUpTheRoad', 'sum'),
    Total_Down=('NumberOfCarsGoingDownTheRoad', 'sum'),
    Avg_Up=('NumberOfCarsGoingUpTheRoad', 'mean'),
    Avg_Down=('NumberOfCarsGoingDownTheRoad', 'mean')
).reset_index()

st.dataframe(stats_by_location)

# Visualization Section
st.subheader("Traffic Data Visualizations")

# 1. Total Cars per Location
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(data=stats_by_location, x='Location', y='Total_Up', color='skyblue', label='Up')
sns.barplot(data=stats_by_location, x='Location', y='Total_Down', color='orange', label='Down')
ax1.set_title("Total Cars by Location")
ax1.set_ylabel("Number of Cars")
ax1.legend()
st.pyplot(fig1)

# 2. Daily Trends of Cars Going Up and Down
fig2, ax2 = plt.subplots(figsize=(10, 6))
for location in df['Location'].unique():
    df_location = df[df['Location'] == location]
    ax2.plot(df_location['Date'], df_location['NumberOfCarsGoingUpTheRoad'], label=f'{location} Up', marker='o')
    ax2.plot(df_location['Date'], df_location['NumberOfCarsGoingDownTheRoad'], label=f'{location} Down', marker='x')

ax2.set_title("Daily Traffic Trends by Location")
ax2.set_xlabel("Date")
ax2.set_ylabel("Number of Cars")
ax2.legend()
st.pyplot(fig2)

# 3. Distribution of Cars
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.histplot(df['NumberOfCarsGoingUpTheRoad'], kde=True, color='skyblue', label='Cars Going Up', ax=ax3)
sns.histplot(df['NumberOfCarsGoingDownTheRoad'], kde=True, color='orange', label='Cars Going Down', ax=ax3)
ax3.set_title("Distribution of Cars")
ax3.set_xlabel("Number of Cars")
ax3.legend()
st.pyplot(fig3)
