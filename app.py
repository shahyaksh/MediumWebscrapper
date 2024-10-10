# Import necessary modules
from MediumWebscrapper.medium_webscrapper import web_scrape, driver  # Import custom web scraper
import streamlit as st
import pandas as pd
from datetime import datetime
from pytz import timezone
import json

# List of topics to choose from for scraping Medium blogs
All_topics = ['Select Topics', 'cybersecurity', 'information-security', 'blockchain', 'Cryptocurrency', 'web3',
              'security', 'ai', 'machine-learning', 'deep-learning', 'nlp', 'data-science', 'data-analysis',
              'image-processing', 'cloud-computing', 'cloud-services', 'dev-ops', 'android', 'app-development',
              'flutter', 'web-development', 'Software-Development', 'backend-development', 'backend']

# Streamlit component for user to select a topic
tag = st.selectbox('Choose the topic', All_topics)

# Streamlit button to trigger CSV generation
generate_csv = st.button('Generate CSV')

if tag != 'Select Topics':  # Check if the user has selected a valid topic
    try:
        # Call the web scraping function to retrieve blogs for the selected topic
        blogs = web_scrape(tag)

        # Display the number of blogs scraped
        st.write(f'Number of Blogs Scrapped are {len(blogs)}')

        # Display the scraped blog data as formatted JSON
        st.code(json.dumps(blogs))

        # Save the scraped blog data to a JSON file
        with open('blogs.json', 'w') as f:
            f.write(json.dumps(blogs))

        # If the user clicks the 'Generate CSV' button, save the data as a CSV file
        if generate_csv:
            try:
                # Load the JSON data into a pandas DataFrame
                df = pd.read_json('blogs.json')

                # Get the current date to include in the CSV filename
                time = datetime.now(timezone("Asia/Kolkata")).date()

                # Save the DataFrame to a CSV file with a specific naming format based on the topic and date
                df.to_csv(
                    f'Datapath/{tag}_mediumblog{time}.csv',
                    index=False)

                # Notify the user that the CSV has been generated
                st.write('CSV Generated Successfully')
            except Exception as e:
                # Handle exceptions during CSV generation
                st.write(f'Error during CSV generation: {e}')
    except Exception as e:
        # Handle exceptions during the web scraping process
        st.write('Browser Closed. Please restart the app.')
        st.write(f'Error: {e}')
