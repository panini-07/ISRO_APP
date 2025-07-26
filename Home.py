
import pandas as pd
import streamlit as st
import requests

def Extract(URL):
#Function to Extract data from the API URL
    URL_Response= requests.get(URL)
    if URL_Response.status_code== 200:
        # HTTP status code 200 checks if request was successful.
        Data= URL_Response.json()
        return Data 
    return None

def ImgExtract(URLIMG):
    URL_Response= requests.get(URLIMG)
    if URL_Response.status_code== 200:
        # HTTP status code 200 checks if request was successful.
        Data= URL_Response.json()
        if "hdurl" in Data:
            Img= Data["hdurl"]
            return Img, Data
        return None, Data
    return None, None 

PicOfTheDay_Img, PicOfTheDay_Data = ImgExtract("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY") #NASA_PicOfTheDay_API (Using DEMO_KEY - can make 30 requests per hour)
Spacecrafts_Data = Extract("https://services.isrostats.in/api/spacecraft") #ISRO_Spacecrafts_API
Launchers_Data = Extract("https://services.isrostats.in/api/launches") #ISRO_Launchers_API
Centres_Data = Extract("https://isro.vercel.app/api/centres") #ISRO_Centres_API

#This will allow us to make sure the data is not lost.
#Streamlit reruns when we switch pages.
if "Spacecrafts_Data" not in st.session_state:
    st.session_state["Spacecrafts_Data"] = Spacecrafts_Data
if "Launchers_Data" not in st.session_state:
    st.session_state["Launchers_Data"] = Launchers_Data
if "Centres_Data" not in st.session_state:
    st.session_state["Centres_Data"] = Centres_Data
if "PicOfTheDay_Data" not in st.session_state:
    st.session_state["PicOfTheDay_Data"] = PicOfTheDay_Data
if "PicOfTheDay_Img" not in st.session_state:
    st.session_state["PicOfTheDay_Img"] = PicOfTheDay_Img

def AppBackground():
     #Funtion to create Background using NASAs Picture of the day Data.
     Image= PicOfTheDay_Img
     if Image:
         background_style = f"""
        <style>
        .stApp {{ 
            background-image: url("{Image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        #.stApp is where the app renders
        # Uses CSS and HtML for stylization
         st.markdown(background_style, unsafe_allow_html=True)
         # Disabling streamlit restrictions on CSS and HTML use

AppBackground() # New picture every 24 hours. Time in Seconds.

def Title_Page():
    st.title("Space Explorer")
    st.divider()
    st.subheader("Astronomy Picture of the Day")

    Title = PicOfTheDay_Data.get("title", "NASA Picture of the Day")
    Date = PicOfTheDay_Data.get("date", "Date Unavailable")
    Explanation = PicOfTheDay_Data.get("explanation", "No description available.")
    Media_Type = PicOfTheDay_Data.get("media_type", "Type Unavailable")
    Url = PicOfTheDay_Data.get("url", "URL Unavailable")
    with st.expander("More Information"): # Expander on Home page  
        st.subheader(Title)
        st.caption(Date)
        st.write(Explanation)
        if Media_Type == "video": # If video this code will run and give the URL for the video
            st.divider()
            st.write("Video")
            st.write("URL:",Url)

    st.write("Come back tomorrow for a new picture.")


Title_Page()
