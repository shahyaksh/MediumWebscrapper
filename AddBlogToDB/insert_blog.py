# Import necessary libraries
import mysql.connector as SqlConnector
import time
from datetime import datetime

# Infinite loop to keep attempting to connect to the database until successful
while True:
    try:
        # Establish connection to the MySQL database
        mydb = SqlConnector.connect(
            host="HostURL",
            user="EnterYourUsernameHere",
            password="EnterPasswordHere",
            database="blog_recommendation_system"
        )

        # Initialize a cursor object to execute SQL queries, using a buffered cursor
        cursor = mydb.cursor(buffered=True)

        print("Connection to Database Successful")
        break
    except Exception as error:
        # If connection fails, print error and retry after 2 seconds
        print("Connection to Database Failed")
        print("Error:", error)
        time.sleep(2)


def get_author_id(author_name: str, blog_name: str) -> int:
    """
    Fetches the author ID from the 'author' table. If the author does not exist, adds the author to the table.

    Args:
    - author_name (str): The name of the blog's author.
    - blog_name (str): The name of the blog's website (e.g., 'Medium').

    Returns:
    - Author_id (int): The ID of the author from the database.
    """

    # Execute SQL query to check if the author exists
    cursor.execute("SELECT * FROM author WHERE author_name=%s", [author_name])
    auth_details = cursor.fetchone()

    if auth_details is not None:
        # If the author exists, return their ID
        Author_id = auth_details[0]
    else:
        # If the author doesn't exist, add them to the database
        Author_id = add_author(author_name, blog_name)

    return Author_id


def add_author(author_name: str, blog_name: str) -> int:
    """
    Adds a new author to the 'author' table and returns the new author's ID.

    Args:
    - author_name (str): The name of the blog's author.
    - blog_name (str): The name of the blog's website.

    Returns:
    - Author_id (int): The ID of the newly inserted author.
    """

    # Insert new author into the 'author' table
    cursor.execute("""
        INSERT INTO author (author_name, blog_web_name)
        VALUES (%s, %s)
    """, (author_name, blog_name))

    # Commit the transaction
    mydb.commit()

    # Fetch and return the ID of the newly inserted author
    cursor.execute("SELECT author_id FROM author WHERE author_name=%s", [author_name])
    Author_id = cursor.fetchone()[0]

    return Author_id


def insert_blog_in_db(blog: dict) -> str:
    """
    Inserts a new blog into the 'blogs' table if it doesn't already exist.

    Args:
    - blog (dict): A dictionary containing the blog's details such as title, content, link, etc.

    Returns:
    - result (str): 'inserted' if the blog was successfully added, or 'Already Exist' if it was found in the database.
    """

    # If there is a millisecond portion in the timestamp, remove it
    if '.' in blog['timestamp']:
        blog['timestamp'] = blog['timestamp'].split('.')[0]

    # Check if a blog with the same title already exists in the 'blogs' table
    cursor.execute("SELECT * FROM blogs WHERE blog_title=%s", [blog['blog_title']])
    blog_det = cursor.fetchone()

    if blog_det is not None:
        # If the blog already exists, return a message indicating so
        return 'Already Exist'
    else:
        # Convert the timestamp to a datetime object for SQL insertion
        datetime_obj = datetime.strptime(blog['timestamp'], '%Y-%m-%d %H:%M:%S')

        # Insert the new blog into the 'blogs' table
        cursor.execute("""
            INSERT INTO blogs (author_id, blog_title, blog_content, blog_link, blog_img, topic, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (blog['author_id'], blog['blog_title'], blog['blog_content'], blog['blog_link'],
              blog['blog_img'], blog['blog_topic'], datetime_obj))

        # Commit the transaction
        mydb.commit()

        # Return a success message
        return 'inserted'
