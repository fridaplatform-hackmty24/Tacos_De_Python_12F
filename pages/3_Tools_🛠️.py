import streamlit as st
from PIL import Image
import requests
import pandas as pd
import matplotlib.pyplot as plt


# Set page configuration
st.set_page_config(
    page_title="ClientHero",
    page_icon="🚀",
)

st.image('./images/Logo 1.png', width=300)

# Function to resize images
def resize_image(image_path, size=(500, 350)):
    image = Image.open(image_path)
    return image.resize(size)

# Function to navigate to another page
def navigate_to(page):
    st.query_params.update(page=page)
     # Rerun the app to apply the query params

# Check the query parameters to determine which page to display
query_params = st.query_params
page = query_params.get("page", "home")

if page == "home":
    st.subheader(":violet[Our main tools]")
    st.divider()

    # Container for images and descriptions
    col1, col2, col3 = st.columns(3)

    with col1:
        resized_image = resize_image('./images/Video.png')
        st.image(resized_image, use_column_width=True)
        st.write("Choose from several metrics from tagged video or important heatmap zones to view user behavior using OpenVino")
        if st.button("View", key="1"):
            navigate_to("page1")

    with col2:
        resized_image = resize_image('./images/Foto1.jpeg')
        st.image(resized_image, use_column_width=True)
        st.write("Use of GenAI tools to generate insights on calls between customers and vendors using FRIDA, OpenAI and Whisper")
        if st.button("View", key="2"):
            navigate_to("page2")

    with col3:
        resized_image = resize_image('./images/Foto2.png')
        st.image(resized_image, use_column_width=True)
        st.write("Compare video and audio to analyze interaction between both parties using live comparison in between")
        if st.button("View", key="3"):
            navigate_to("page3")

elif page == "page1":
    st.subheader("Upload videos to start analyzing.")
    st.divider()
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    
    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)
        
        # Send the file to the FastAPI backend
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        upload_response = requests.post("http://10.22.238.73:8000/v1/datastore/upload", files=files)
        
        if upload_response.status_code == 200:
            st.success("File uploaded successfully!")
            
            if st.button("Download Heatmap"):

                download_url = f"http://10.22.238.73:8000/v1/datastore/download?file_name={uploaded_file.name}&file_type=video&media_type=video%2Fmp4"
                st.markdown(f"[Download Video]({download_url})")
                download = requests.get(download_url)
                if download.status_code == 200:
                    st.success("Video visualization in progress")
                    with open(uploaded_file.name, "wb") as f:
                        f.write(download.content)
                    st.video(uploaded_file.name)
                else:
                    st.error("Failed to analyze the file.")
        else:
            st.error("Failed to upload file.")
    
    if st.button("Back to Home"):
        navigate_to("home")

elif page == "page2":
    st.subheader("Upload audio file to start analyzing.")
    st.divider()
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "flac", "m4a"])
    
    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)
        
        # Send the file to the FastAPI backend
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        upload_response = requests.post("http://10.22.238.73:8000/v1/datastore/upload", files=files)
        
        if upload_response.status_code == 200:
            st.success("File uploaded successfully!")
            
            if st.button("Analyze File"):
                # Call the analysis endpoint
                analyze_url = f"http://10.22.238.73:8000/v1/audio/analyze?file_name={uploaded_file.name}"
                analyze_response = requests.get(analyze_url)
                
                if analyze_response.status_code == 200:
                    st.success("File analyzed successfully!")
                    analysis_result = analyze_response.json()
                    st.write("Analysis Result:")
                    
                    transcription = analysis_result.transcription
                    st.write(transcription)
                    
                else:
                    st.error("Failed to analyze the file.")
        else:
            st.error("Failed to upload file.")
    
    if st.button("Back to Home"):
        navigate_to("home")


elif page == "page3":
    st.subheader("Upload auduio file to start analyzing.")
    st.divider()
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    
    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)
    
    if st.button("Back to Home"):
        navigate_to("home")