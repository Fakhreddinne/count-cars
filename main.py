import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Streamlit app layout to wide for a better presentation
st.set_page_config(layout="wide")

# Load the data from the Excel file
file_path = 'cars_traffic_data_extended.xlsx'
df = pd.read_excel(file_path)

# Ensure 'Date' column is in datetime format for easy filtering and plotting
df['Date'] = pd.to_datetime(df['Date'])

# Set the app title
st.title("INTERVIEWW 123 ")

# Create two columns for the first section of the app
col1, col2 = st.columns(2)

# Display the traffic data table in the first column
with col1:
    st.subheader("Traffic Data Table")
    st.dataframe(df)  # Show the raw data

# Display summary statistics and video in the second column
with col2:
    st.subheader("Traffic Data Statistics")
    
    # Calculate total and average number of cars going up and down the road
    total_up = df['NumberOfCarsGoingUpTheRoad'].sum()
    total_down = df['NumberOfCarsGoingDownTheRoad'].sum()
    avg_up = df['NumberOfCarsGoingUpTheRoad'].mean()
    avg_down = df['NumberOfCarsGoingDownTheRoad'].mean()

    # Create two sub-columns to separate statistics and video
    col21, col22 = st.columns(2)
    
    with col21:
        # Display the calculated metrics
        st.metric("Total Cars Going Up", total_up)
        st.metric("Total Cars Going Down", total_down)
        st.metric("Average Cars Going Up per Day", f"{avg_up:.2f}")
        st.metric("Average Cars Going Down per Day", f"{avg_down:.2f}")
    
    with col22:
        # Add a video (local file or URL)
        st.subheader("Traffic Flow Video")
        try:
            gif_path = 'output.gif'  # Replace with your GIF file path
            st.image(gif_path, caption="Traffic Flow - Car-Detection-OpenCV - jitendrasb24 ", use_container_width=True)
        except FileNotFoundError:
            st.error("Video file not found. Please ensure 'o    utput.mp4' exists in the app directory.")
    

# Add a dropdown menu to select sorting by Date or Location
sort_by = st.selectbox("Sort by", options=["Date", "Location"])

# Show statistics based on Date selection
if sort_by == "Date":
    # Allow the user to select a specific date
    selected_date = st.date_input("Select Date", df['Date'].min())
    
    # Filter data for the selected date
    df_filtered_by_date = df[df['Date'] == pd.to_datetime(selected_date)]
    
    # If there is data for the selected date
    if not df_filtered_by_date.empty:
        # Create two columns to display the stats and plot side by side
        col3, col4 = st.columns(2)

        with col3:
            # Display the traffic stats for the selected date by location
            st.subheader(f"Traffic Stats for {selected_date}")
            
            # Group the data by location and aggregate the statistics
            stats_by_location_on_date = df_filtered_by_date.groupby('Location').agg(
                Total_Up=('NumberOfCarsGoingUpTheRoad', 'sum'),
                Total_Down=('NumberOfCarsGoingDownTheRoad', 'sum'),
                Avg_Up=('NumberOfCarsGoingUpTheRoad', 'mean'),
                Avg_Down=('NumberOfCarsGoingDownTheRoad', 'mean')
            ).reset_index()

            # Display the aggregated statistics as a table
            st.dataframe(stats_by_location_on_date)

        with col4:
            # Create and display a bar plot for the average number of cars per location
            fig, ax = plt.subplots(figsize=(8, 4))  # Set smaller figure size

            # Create a bar plot showing average cars going up and down by location
            sns.barplot(
                data=stats_by_location_on_date.melt(id_vars='Location', value_vars=['Avg_Up', 'Avg_Down']),
                x='Location', y='value', hue='variable', ax=ax
            )

            # Customize the plot with titles and labels
            ax.set_title(f"Average Number of Cars per Location on {selected_date}")
            ax.set_ylabel("Average Number of Cars")
            ax.set_xlabel("Location")
            ax.legend(title="Direction", labels=["Going Up", "Going Down"])

            # Display the plot
            st.pyplot(fig)

# Show statistics based on Location selection
else:
    # Allow the user to select a specific location
    selected_location = st.selectbox("Select Location", df['Location'].unique())
    
    # Filter data for the selected location
    df_filtered_by_location = df[df['Location'] == selected_location]
    
    # If there is data for the selected location
    if not df_filtered_by_location.empty:
        # Create two columns to display the stats and plot side by side
        col3, col4 = st.columns(2)

        with col3:
            # Display the traffic stats for the selected location by date
            st.subheader(f"Traffic Stats for {selected_location}")
            
            # Group the data by date and aggregate the statistics
            stats_by_date_on_location = df_filtered_by_location.groupby('Date').agg(
                Total_Up=('NumberOfCarsGoingUpTheRoad', 'sum'),
                Total_Down=('NumberOfCarsGoingDownTheRoad', 'sum'),
                Avg_Up=('NumberOfCarsGoingUpTheRoad', 'mean'),
                Avg_Down=('NumberOfCarsGoingDownTheRoad', 'mean')
            ).reset_index()

            # Display the aggregated statistics as a table
            st.dataframe(stats_by_date_on_location)

        with col4:
            # Create and display a line plot for the average number of cars per date
            fig, ax = plt.subplots(figsize=(8, 4))  # Set smaller figure size

            # Create a line plot showing average cars going up and down by date
            sns.lineplot(data=stats_by_date_on_location.melt(id_vars='Date', value_vars=['Avg_Up', 'Avg_Down']),
                         x='Date', y='value', hue='variable', ax=ax)

            # Customize the plot with titles and labels
            ax.set_title(f"Average Number of Cars per Date at {selected_location}")
            ax.set_ylabel("Average Number of Cars")
            ax.set_xlabel("Date")
            ax.legend(title="Direction", labels=["Going Up", "Going Down"])

            # Display the plot
            st.pyplot(fig)
            
# Add header with your name, your colleague's name, and LinkedIn profile link at the top
st.markdown("""
    <div style="text-align: center; font-size: 14px; padding-bottom: 10px;">
        <h5>Developed by Eng. Fakhreddine Annabi & Eng. Houssem Ouerghie</h5>
        <p>
            <a href="https://www.linkedin.com/in/fakhreddine-annabi/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" width="20" height="20" alt="LinkedIn Profile">
            </a>
        </p>
        <p>© 2024 All Rights Reserved</p>
    </div>
    <hr>
""", unsafe_allow_html=True)
