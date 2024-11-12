# Bike-Share-Analysis

This dataset contains the hourly and daily count of rental bikes between years 2011 and 2012 in Capital bikeshare system with the corresponding weather and seasonal information.
## **Overview**
### **Day table**
- `Unnamed: 0` - Index column
- `Date` - Date in `YYYY-MM-DD` format
- `Season` - Season of the year (`Winter`, `Spring`, `Summer`, `Fall`)
- `Year` - Year of the record (e.g., `2011`, `2012`)
- `Month` - Month (1 to 12)
- `Holiday` - Indicator if the day is a holiday (`Holiday`, `Non-Holiday`)
- `Weekday` - Day of the week by name (e.g., `Sunday`, `Monday`)
- `Working Day` - Indicator if the day is a working day (`Workingday`, `Non-Workingday`)
- `Daily Weather Situation` - General weather condition (e.g., `Clear`, `Mist`, `Light Snow`)
- `Daily Temperature` - Normalized daily average temperature
- `Daily Feels-like Temperature` - Normalized daily average "feels-like" temperature
- `Daily Humidity` - Normalized daily average humidity
- `Daily Windspeed` - Normalized daily average wind speed
- `Daily Casual Users` - Daily count of casual users
- `Daily Registered Users` - Daily count of registered users
- `Daily Total Rentals` - Daily total rental count including casual and registered users

### **Hour table**
- `hr` - Hour of the day (0 to 23)
- `Hourly Weather Situation` - Specific hourly weather condition (e.g., `Clear`, `Mist`, `Light Snow`, `Heavy Rain`)
- `Hourly Temperature` - Normalized hourly temperature
- `Hourly Feels-like Temperature` - Normalized hourly "feels-like" temperature
- `Hourly Humidity` - Normalized hourly humidity
- `Hourly Windspeed` - Normalized hourly wind speed
- `Hourly Casual Users` - Hourly count of casual users
- `Hourly Registered Users` - Hourly count of registered users
- `Hourly Total Rentals` - Hourly total rental count including casual and registered users

View the dashboard on Streamlit directly at this link: [Bike Share Analysis Dashboard](https://bike-share-analysis-abhinawap.streamlit.app/)
