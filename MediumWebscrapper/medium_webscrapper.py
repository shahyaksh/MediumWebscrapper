# Import necessary libraries and modules
import selenium as sc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import requests as re
from def_image import getImage  # Custom module to get default image
import os
import time
from pytz import timezone

# from AddBlogToDB.insert_blog import get_author_id, insert_blog_in_db

# Configure environment path for Selenium WebDriver
os.environ['PATH'] += r"C:/SeleniumDrivers"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Add a short delay to allow the browser to launch
time.sleep(2)


def web_scrape(tag: str):
    """
    Scrapes Medium for blogs related to a specific tag.

    Args:
    - tag (str): The tag/category to search for blogs (e.g., 'ai', 'technology').

    Returns:
    - blogs (list): A list of dictionaries, each containing information about a blog post.
    """

    # URLs to scrape for trending and latest articles based on the provided tag
    trending_url = f'https://medium.com/tag/{tag}/recommended'

    # Open the trending URL in the browser
    driver.get(trending_url)

    # Set parameters for scrolling down the webpage
    last_height = driver.execute_script("return document.body.scrollHeight")
    SCROLL_PAUSE_TIME = 2  # Pause time between scrolls

    # Continuously scroll down to load more articles until no more new content is found
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the page source after scrolling
    source_page = driver.page_source

    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(source_page, 'html.parser')

    # Initialize a list to hold all the blog data
    blogs = []

    # Get the current time to timestamp the blog entries
    curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

    # Find all article elements in the parsed HTML
    All_Articles = soup.find_all('article')

    # Iterate over all found articles
    for article in All_Articles:
        blog = {}

        # Extract blog author and link information
        source = article.find('div', recursive=False).find_all('a')

        if len(source) < 4:
            continue

        # Collect blog data and store it in the blog dictionary
        blog['blog_website_name'] = 'medium'

        # Extract author information
        blog['author'] = source[0].find('img')['alt']

        # Extract blog link
        blog['blog_link'] = 'https://medium.com' + source[3]['href']

        # Ensure the article contains a title and content, otherwise skip
        if source[3].find_all('h2') == [] or source[3].find_all('div') == []:
            continue

        # Extract the blog title
        blog['blog_title'] = source[3].find_all('h2')[0].text

        # Extract the blog content
        blog['blog_content'] = source[3].find_all('div')[0].text

        # Extract the blog image, or provide a default image using getImage module
        if source[len(source) - 4].find('img') is None:
            blog['blog_img'] = getImage.get_image(tag)  # Get default image
        else:
            blog['blog_img'] = source[len(source) - 4].find('img')['src']

        # Add additional blog metadata
        blog['blog_topic'] = tag
        blog['timestamp'] = curr_time

        # Append the blog dictionary to the blogs list
        blogs.append(blog)

    # Return the list of scraped blogs
    return blogs


# Main function to execute the scraping process
if __name__ == "__main__":
    try:
        # Scrape blogs related to 'ai' tag
        blogs = web_scrape('ai')

        # Print the scraped blogs
        print(blogs)
        print(f"Total blogs scraped: {len(blogs)}")
    except Exception as e:
        # Handle exceptions and print error message
        print(f'Web scraping attempt failed. Please try again. Error: {e}')
