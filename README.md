Here's a README file based on the information about your Medium Web Scraper project:

---

# Medium Web Scraper

This is a web scraping application that scrapes blogs from Medium.com based on a specified topic and stores the data in a MySQL database. The project is built using Streamlit for the user interface and Selenium for scraping. It allows users to choose from a list of predefined topics, fetch the latest blogs, and save them in a structured format (JSON or CSV).

## Features
- Scrapes Medium blogs based on user-specified topics.
- Saves the scraped blogs' metadata (author, title, content, link, and images) to a MySQL database.
- Provides an option to download the blog data as a JSON or CSV file.
- User-friendly interface built using Streamlit.

## Technologies Used
- **Streamlit**: For the interactive user interface.
- **Selenium**: For web scraping.
- **MySQL**: For storing blog data.
- **BeautifulSoup**: For parsing the HTML content of Medium pages.
- **Pandas**: For managing data and exporting it to CSV.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/shahyaksh/MediumWebscrapper.git
cd MediumWebscrapper
```

### 2. Install dependencies
You can install all the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. MySQL Database Setup
Set up a MySQL database and update the connection details in the script where required (host, user, password, database). Ensure that you have the necessary tables:
- `author`: For storing author details.
- `blogs`: For storing blog metadata (author ID, title, content, link, image, topic, timestamp).

### Sample Tables
#### `author` Table:
```sql
CREATE TABLE author (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(255),
    blog_web_name VARCHAR(255)
);
```

#### `blogs` Table:
```sql
CREATE TABLE blogs (
    blog_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    blog_title VARCHAR(255),
    blog_content TEXT,
    blog_link VARCHAR(255),
    blog_img VARCHAR(255),
    topic VARCHAR(100),
    timestamp DATETIME,
    FOREIGN KEY (author_id) REFERENCES author(author_id)
);
```

### 4. Run the application
To start the scraper, use the following command:
```bash
streamlit run app.py
```

## How to Use

1. **Select Topic**: Choose a topic from the dropdown menu on the Streamlit app.
2. **Scrape Blogs**: The app will scrape the latest blogs based on the selected topic.
3. **View Blogs**: The scraped blogs will be displayed on the screen and saved to the database.
4. **Download Data**: You can download the scraped data as a JSON or CSV file.

## Example
After running the application, select a topic such as "ai" or "machine-learning," and it will fetch and display the latest blogs from Medium. These blogs will be stored in the MySQL database, and you can also save them as CSV or JSON.

## Demo

Watch a demo of the Medium Web Scraper in action [here](https://drive.google.com/file/d/1Ecotjtb7j1wJQaX_wI-dEmJ5Q1hyicWY/view?usp=drive_link).

## Future Enhancements
- Adding more flexible search options for users.
- Improving scraping speed and handling more topics.
- Enhanced error handling for network issues or website changes.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify any part of the README if necessary!
