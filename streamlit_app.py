import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pypalettes import load_cmap, get_hex
import plotly.graph_objects as go
import altair as alt


plt.style.use('dark_background')
sns.set_style("darkgrid", {
    "axes.facecolor": "#0e1117",   
    "axes.edgecolor": "#0e1117",   
    "grid.color": "#1e2228",       
    "grid.linestyle": "-",         
    "axes.labelcolor": "#8b949e",  
    "xtick.color": "#8b949e",      
    "ytick.color": "#8b949e",      
    "text.color": "#8b949e"        
})

cmap = load_cmap('cacnea').hex
palette = get_hex('cacnea')
palette_2_compare = get_hex('cacnea', keep=[False, True, True, False, False, False, False, 
                                            False, False, False, False, False, False, False])
palette_1 = get_hex('cacnea', keep_first_n=1)[0]

# Load data
data_path = '/home/abhinawap/StudySes/Dicoding/Analyst_project/bike-sharing-dataset-cleaned.csv'
df = pd.read_csv(data_path)

st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

# Select which business question to answer
question = st.sidebar.selectbox("Select Business Question", ["Factors Influencing Total Rentals", 
                                                             "Casual vs Registered User Patterns"])

# Sidebar option for Hour or Day selection
view_option = st.sidebar.selectbox("Select time frame", ["Hourly", "Daily"])

# Define prefixes based on selection
prefix = "Hourly" if view_option == "Hourly" else "Daily"

# Utility function to get column with fallback
def get_column(name):
    return f"{prefix} {name}" if f"{prefix} {name}" in df.columns else name

# Adjust column names with fallback for missing prefixes
total_rentals_col = get_column("Total Rentals")
casual_users_col = get_column("Casual Users")
registered_users_col = get_column("Registered Users")
weather_col = get_column("Weather Situation")
temp_col = get_column("Temperature")
atemp_col = get_column("Feels-like Temperature")
humidity_col = get_column("Humidity")
windspeed_col = get_column("Windspeed")

# Set up Streamlit app
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"""
This dashboard provides insights into the bike-sharing dataset, focusing on factors influencing the {view_option.lower()} count of rentals and the rental patterns of casual vs. registered users.
""")

# Display Key Metrics in Columns
if question == "Factors Influencing Total Rentals":
    st.subheader("All-Time Statistics")
    metrics = [
        (f"Total Rentals ({view_option})", total_rentals_col, '#29b5e8')
    ]

    cols = st.columns(len(metrics))
    for col, (title, column, color) in zip(cols, metrics):
        # Calculate total value as a numeric type
        total_value = int(df[column].sum()) if df[column].dtype in ['int64', 'float64'] else None
        if total_value is not None:
            col.metric(label=title, value=f"{total_value:,}")

    st.subheader("Total Rentals by Category")

    # Create tabs for each category
    col1, col2, col3, col4 = st.columns(4)

    # Weather Tab
    with col1:
        st.markdown("### Weather")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=weather_col, y=total_rentals_col, data=df, palette=palette)
        ax.set_xlabel("Weather")
        ax.set_ylabel(f"Rentals ({view_option})")
        st.pyplot(fig)

    # Working Day Tab
    with col2:
        st.markdown("### Working Day")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Working Day", y=total_rentals_col, data=df, palette=palette)
        ax.set_xlabel("Working Day")
        ax.set_ylabel(f"Rentals ({view_option})")
        st.pyplot(fig)

    # Season Tab
    with col3:
        st.markdown("### Season")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Season", y=total_rentals_col, data=df, palette=palette)
        ax.set_xlabel("Season")
        ax.set_ylabel(f"Rentals ({view_option})")
        st.pyplot(fig)

    # Holiday Tab
    with col4:
        st.markdown("### Holiday")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Holiday", y=total_rentals_col, data=df, palette=palette)
        ax.set_xlabel("Holiday")
        ax.set_ylabel(f"Rentals ({view_option})")
        st.pyplot(fig)
        
    
    # Set columns for the temperature and Feels-like temperature
    col1, col2 = st.columns(2)
    
    with col1:
        # Streamgraph Temperature Container
        with st.container():
            st.subheader(f"Total Rentals vs Temperature ({view_option}) with Season Variation")
            df_stream = df.groupby([temp_col, 'Season'])[total_rentals_col].sum().reset_index()
            chart = alt.Chart(df_stream).mark_area(interpolate='basis').encode(
                x=alt.X(f'{temp_col}:Q', title='Temperature'),
                y=alt.Y(f'{total_rentals_col}:Q', stack='center', title=f'Total Rentals ({view_option})'),
                color=alt.Color('Season:N', scale=alt.Scale(range=palette), legend=alt.Legend(title="Season"))
            ).properties(width=700, height=400)
            st.altair_chart(chart, use_container_width=True)

    with col2:
        # Additional Streamgraph for Feels-like Temperature
        with st.container():
            st.subheader(f"Total Rentals vs Feels-like Temperature ({view_option}) with Season Variation")
            df_stream = df.groupby([atemp_col, 'Season'])[total_rentals_col].sum().reset_index()
            chart = alt.Chart(df_stream).mark_area(interpolate='basis').encode(
                x=alt.X(f'{atemp_col}:Q', title='Feels-like Temperature'),
                y=alt.Y(f'{total_rentals_col}:Q', stack='center', title=f'Total Rentals ({view_option})'),
                color=alt.Color('Season:N', scale=alt.Scale(range=palette), legend=alt.Legend(title="Season"))
            ).properties(width=700, height=400)
            st.altair_chart(chart, use_container_width=True)

    # Hourly-Specific Plots
    if view_option == "Hourly":
        with st.container():
            
            # Create three columns and use the middle one for centering the plot
            left_col, center_col, right_col = st.columns([1, 3, 1])  # Adjust column ratios as needed

            with center_col:
                # Create the plot with a wider aspect ratio
                st.subheader("Total Rentals by Hour")
                fig, ax = plt.subplots(figsize=(12, 4))  # Adjust width and height as needed
                sns.histplot(x="hr", weights="Hourly Total Rentals", data=df, bins=24, kde=True, color=palette_1, ax=ax)
                
                # Set labels
                ax.set_xlabel("Hour of Day")
                ax.set_ylabel("Rentals (Hourly)")
                
                # Display the plot
                st.pyplot(fig)

                
        # Container for tabbed layout
        with st.container():
            weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            st.subheader("Hourly Rentals by Day of the Week")
            
            # Create a tab for each day
            tabs = st.tabs(weekdays)
            
            # Iterate through each weekday and plot data in its respective tab
            for i, day in enumerate(weekdays):
                with tabs[i]:
                    st.markdown(f"#### Rentals on {day}")
                    
                    # Filter data for the selected day
                    df_weekday = df[df['Weekday'] == day]
                    
                    # Create the plot for the selected day
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.lineplot(x='hr', y='Hourly Total Rentals', data=df_weekday, ax=ax, color=palette_1)
                    
                    # Set plot title and labels
                    ax.set_title(f'Rentals on {day}')
                    ax.set_xlabel("Hour")
                    ax.set_ylabel("Rentals")
                    ax.tick_params(colors="#8b949e")
                    
                    # Display the plot
                    st.pyplot(fig)

# Display Casual vs Registered User Patterns
elif question == "Casual vs Registered User Patterns":
    st.subheader("Casual vs Registered User Rental Patterns")
    st.subheader("All-Time Statistics")
    metrics = [
        (f"Total Casual Users ({view_option})", casual_users_col, '#29b5e8'),
        (f"Total Registered Users ({view_option})", registered_users_col, '#f9a825')
    ]

    cols = st.columns(len(metrics))
    for col, (title, column, color) in zip(cols, metrics):
        # Calculate total value as a numeric type
        total_value = int(df[column].sum()) if df[column].dtype in ['int64', 'float64'] else None
        if total_value is not None:
            col.metric(label=title, value=f"{total_value:,}")
            
    cols1, cols2, cols3 = st.columns(3)

    # Visualization 1: Average Rentals on Holidays vs Non-Holidays
    with cols1:
        with st.container():
            st.markdown("#### Holidays vs Non-Holidays")
            holiday_avg = df.groupby('Holiday')[[casual_users_col, registered_users_col]].mean().reset_index()
        

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(holiday_avg['Holiday'], holiday_avg[casual_users_col], label='Casual', color=palette_2_compare[0])
            ax.bar(holiday_avg['Holiday'], holiday_avg[registered_users_col], bottom=holiday_avg[casual_users_col], 
                label='Registered', color=palette_2_compare[1])

            ax.set_title('Average Number of Rentals on Holidays vs Non-Holidays')
            ax.set_ylabel('Average Number of Rentals')
            ax.set_xlabel('Day Type')
            ax.legend(title='User Type')
            plt.grid(True, axis='y')
            st.pyplot(fig)

    # Visualization 2: Average Rentals by Season
    with cols2:
        with st.container():
            st.markdown("#### Average Rentals by Season")
            season_avg = df.groupby('Season')[[casual_users_col, registered_users_col]].mean().reset_index()
            

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(season_avg['Season'], season_avg[casual_users_col], label='Casual', color=palette_2_compare[0])
            ax.bar(season_avg['Season'], season_avg[registered_users_col], bottom=season_avg[casual_users_col], 
                label='Registered', color=palette_2_compare[1])

            ax.set_title('Average Number of Rentals by Season')
            ax.set_ylabel('Average Number of Rentals')
            ax.set_xlabel('Season')
            ax.legend(title='User Type')
            plt.grid(True, axis='y')
            st.pyplot(fig)

    # Visualization 3: Average Rentals by Month
    with cols3:
        with st.container():
            st.markdown("#### Average Rentals by Month")
            month_avg = df.groupby('Month')[[casual_users_col, registered_users_col]].mean().reset_index()

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(month_avg['Month'], month_avg[casual_users_col], label='Casual', color=palette_2_compare[0])
            ax.bar(month_avg['Month'], month_avg[registered_users_col], bottom=month_avg[casual_users_col], 
                label='Registered', color=palette_2_compare[1])

            ax.set_title('Average Number of Rentals by Month')
            ax.set_ylabel('Average Number of Rentals')
            ax.set_xlabel('Month')
            ax.legend(title='User Type')
            plt.grid(True, axis='y')
            st.pyplot(fig)
    
    if view_option == "Hourly":
        # Visualization 4: Hourly Rentals by User Type
        st.markdown("### Average Number of Rentals per Hour for Each Day")
        
        # Define a list of weekday names matching the dataset
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        # Create tabs for each day of the week
        tabs = st.tabs(weekdays)
        
        for i, day in enumerate(weekdays):
            with tabs[i]:
                st.markdown(f"#### Hourly Rentals on {day}")
                
                # Filter data for the selected day
                df_weekday = df[df['Weekday'] == day]
        
                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(x='hr', y=casual_users_col, data=df_weekday, color=palette_2_compare[0], label='Casual')
                sns.lineplot(x='hr', y=registered_users_col, data=df_weekday, color=palette_2_compare[1], label='Registered')
                
                # Set plot title and labels
                ax.set_title(f'Average Number of Rentals per Hour on {day}')
                ax.set_xlabel("Hour")
                ax.set_ylabel("Rentals")
                ax.legend(title="User Type")
                
                # Display the plot
                st.pyplot(fig)
