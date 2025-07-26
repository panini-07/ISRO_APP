import streamlit as st
import requests 
import pandas as pd

centres = st.session_state["Centres_Data"]

# Converting API Link Data to a DataFrame
API_Centres_DF = pd.DataFrame(centres["centres"])  # Extract 'centres' key
API_Centres_DF.columns = API_Centres_DF.columns.str.lower().str.strip()

# Coordinates for Centres API
csv_Centres_Coordinates = "Centre_Coordinates.csv"
Coordinates_DF = pd.read_csv(csv_Centres_Coordinates)

# Merge API data with coordinates
Merged_DF = API_Centres_DF.merge(Coordinates_DF, on=["name", "place", "state"], how="inner")

# Page Title
st.title("ISRO Centres Explorer")
st.write("Explore various ISRO centres across India")

Filtered_df = Merged_DF

# Filters to narrow search
st.subheader("Filter Options")
col1, col2 = st.columns(2)
with col1:
    state_filter = st.multiselect("Select State(s)", options=Merged_DF["state"].unique())
with col2:
    city_filter = st.multiselect("Select City(s)", options=Merged_DF["place"].unique())

if state_filter != []:
    Filtered_df = Filtered_df[Filtered_df["state"].isin(state_filter)]
if city_filter != []:
    Filtered_df = Filtered_df[Filtered_df["place"].isin(city_filter)]

st.header("ISRO Centres")
columns_to_show = ["name", "place", "state", "latitude", "longitude"]
st.dataframe(Filtered_df[columns_to_show]) # Displays dataframe 

# Map Visualization
st.subheader("Map of ISRO Centres")
if not Filtered_df.empty and "latitude" in Filtered_df.columns and "longitude" in Filtered_df.columns:
    st.map(Filtered_df)
else:
    st.write("Latitude and Longitude data not available.")

# Summary Statistics - Gives number and Links for selected centres
st.subheader("Summary")
st.write("Total Centres: ", len(Filtered_df))
if state_filter != []:
    st.write("To know more about your selected Centres: ", Filtered_df["link"])

