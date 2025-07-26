import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests
from collections import Counter

with st.sidebar:
    #Creates sidebar menu page 
    Selection_panel=st.selectbox("What do you want to explore?", ["Spacecrafts", "Launchers"],index=None,
            placeholder="Select an option")

if "Spacecrafts_Data" in st.session_state:
#To create output for Spacecraft option in dropdown menu.
    if Selection_panel == "Spacecrafts":
        Spacecrafts = st.session_state["Spacecrafts_Data"]
        st.header("ISRO has launched the following spacecrafts")
        columns = st.columns(4)
        for Num, Craft_Name in enumerate(Spacecrafts):
            col= columns[Num % 4]
            col.write(Craft_Name["name"])
        Search_Query = st.text_input("Search (Enter name of Spacecraft)").lower()
        def filter_data(Info , key):
            return [item for item in Info if Search_Query in item[key].lower()]
        if Search_Query:
            for item in filter_data(st.session_state["Spacecrafts_Data"],"name"):
                st.subheader(item["name"])  # Display name as header
                st.json(item)  # Show all details in JSON format

#ChatGPT could never do this the way I do ;)

if "Launchers_Data" in st.session_state:
    if Selection_panel == "Launchers":
        Launchers = st.session_state["Launchers_Data"]
        Chart_Type=st.selectbox("Choose a Visualization",["Bar Chart", "Pie Chart", "Timeline Plot", "Scatter plot"],index=None , placeholder= "Select a chart")
        
        with st.sidebar:
             st.subheader("Filter Data")
             selected_types = st.multiselect("Select Launcher Types", list(set(l["LaunchType"] for l in Launchers)), default=[]) #Dropdown Multiselect for Launch Types
             
             Launcher_types = [L_Type["LaunchType"] for L_Type in Launchers]  # Lists all Launchers in Data
             launcher_counts = Counter(Launcher_types)  # Counts Frequency of total Lunchers

             if selected_types:
                 filtered_launchers = [l for l in Launchers if l["LaunchType"] in selected_types] # Lists all Launchers in selected_types var with multiselect 
             else:
                 filtered_launchers = Launchers #Lists all 

        if Chart_Type == "Timeline Plot":
            st.header("Launches By ISRO")
            Years = [launch["LaunchDate"].split("-")[0] for launch in Launchers if "LaunchDate" in launch]  # Extracting year from date
            launch_counts = Counter(Years)
            df = pd.DataFrame(list(launch_counts.items()), columns=["Year", "Launches"])        
            df = df.astype({"Year": int}).sort_values("Year",ascending=True)
            st.dataframe(df,hide_index= True)
            Year_Num = list(df["Year"])  # Unique years
            Year_Frequency = list(df["Launches"])  # Count of launches
            fig, ax = plt.subplots(figsize=(20,10))
            ax.bar(Year_Num, Year_Frequency, color='seashell', edgecolor='saddlebrown')
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Launches")
            ax.set_title("ISRO Launches Per Year")
            st.pyplot(fig)

        elif Chart_Type == "Bar Chart":
            st.subheader("Launcher Count by Type")
            type_counts = Counter(l["LaunchType"] for l in filtered_launchers) # Counts Launchers in filtered Launchers selected from Multiselect
            #Creates a dictionary
            fig, ax = plt.subplots(figsize=(20,10))
            ax.bar(type_counts.keys(), type_counts.values(), color="seashell")
            ax.set_xlabel("Launcher Type")
            ax.set_ylabel("Count")
            ax.set_title("Number of Launchers by Type")
            st.pyplot(fig)

        elif Chart_Type == "Pie Chart":
            st.subheader("Launcher Distribution")
            type_counts = Counter(l["LaunchType"] for l in filtered_launchers) # Counts Launchers in filtered Launchers selected from Multiselect
            fig, ax = plt.subplots(figsize=(20,10))
            ax.pie(type_counts.values(), labels=type_counts.keys(), autopct="%1.1f%%",
            colors=["seashell","antiquewhite","linen","papayawhip","blanchedalmond"])
            ax.set_title("Launcher Distribution")
            st.pyplot(fig)
        
        elif Chart_Type == "Scatter plot":
            min_year, max_year = st.sidebar.slider("Select Year Range", 1970, 2025, (1970, 2025)) #Slider for years
            st.subheader("Launch Type Timeline of ISRO")
            launch_data = [(l["LaunchType"], int(l["LaunchDate"][:4])) for l in filtered_launchers if l["LaunchDate"][:4].isdigit()]
            filtered_data = [(ltype, year) for ltype, year in launch_data if min_year <= year <= max_year]
            launch_types = sorted(set(l[0] for l in filtered_data))  # Unique launch types
            type_map = {lt: i for i, lt in enumerate(launch_types)}  # Map to numeric values for plotting
            x_vals = [l[1] for l in filtered_data]  # Years
            y_vals = [type_map[l[0]] for l in filtered_data]  # Numeric launch type values
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.scatter(x_vals, y_vals, color="red", alpha=0.7, label="Launch Event")  # Scatter points
            ax.set_xlabel("Year")
            ax.set_ylabel("Launch Type")
            ax.set_title("Timeline of ISRO Launch Types")
            ax.set_yticks(range(len(launch_types)))
            ax.set_yticklabels(launch_types)  # Set launch type names as y-tick labels
            ax.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig)

