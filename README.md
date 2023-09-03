# README for Redfin Scraper Web App

## Introduction
This GitHub repository contains a web scraping application built using Python, Flask, and SQLAlchemy that allows users to scrape housing leads for sale from the Redfin website based on a specified location. The scraped leads are stored in a database and can be viewed on a web page. Additionally, the scraped data is also exported to a Google Sheets spreadsheet for easy access and analysis. The web app includes functionality for updating the scraped data daily to ensure that you always have the latest leads.

## Features
- **Web Scraping:** The application scrapes housing leads for sale from the Redfin website based on a user-specified location.

- **Database Storage:** The scraped data is stored in a SQLite database (`scraped_data.db`) using SQLAlchemy. The database includes two tables: `Location` and `ScrapedData`.

- **Web Interface:** Users can interact with the web app through a user-friendly web interface. They can input a location and initiate the scraping process.

- **Data Updates:** The web app includes a scheduled task that updates the scraped data daily. This ensures that the leads are always up-to-date.

- **Data Visualization:** The scraped data can be viewed on a web page, making it easy to browse and filter the leads.

- **Google Sheets Integration:** The scraped data is exported to a Google Sheets spreadsheet for further analysis and sharing.

## Installation
To run this application locally, you will need to follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/redfin-scraper-web-app.git
   ```

2. Navigate to the project directory:
   ```bash
   cd redfin-scraper-web-app
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

7. **Google Sheets Configuration**:

   - Open the `refer.py` file in your code editor.

   - Locate the `refresh()` function:

     ```python
     def refresh():
         # ...
         driver.get("Your link or the sheet here ")
         # ...
     ```

   - Replace `"Your link or the sheet here "` with the actual URL or link to your Google Sheets document. This document should contain data from the Redfin scraper.

   - Ensure that your Google Sheets document is set up with the Coefficient extension to connect it to your database.
## Database Configuration and Migrations

This web application uses Flask SQLAlchemy for database operations and Flask-Migrate for managing database migrations. Here's how to configure the database and perform migrations:

### Database Configuration

The database configuration can be found in the `app.py` file in the project. By default, the application uses SQLite as the database. You can modify the database URI to use a different database system. The default SQLite configuration is as follows:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
```

#### SQLite (Default)

SQLite is a lightweight and serverless database engine suitable for development and small-scale applications. You don't need to install a separate database server to use SQLite.

To use SQLite, keep the configuration in `app.py` as shown above.

#### Other Database Systems

If you prefer to use a different database system (e.g., PostgreSQL, MySQL), you can modify the database URI in `app.py`. For example, for PostgreSQL:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
```

Replace `username`, `password`, `localhost`, and `database_name` with your specific database credentials and configuration.

### Database Migrations

Flask-Migrate is used to manage database migrations, allowing you to make changes to the database schema over time.

1. After making changes to your models or database schema, you'll need to create a migration:

   ```bash
   flask db init
   ```

2. Generate a migration script based on your changes:

   ```bash
   flask db migrate -m "Description of the migration"
   ```

3. Apply the migration to update the database:

   ```bash
   flask db upgrade
   ```

   This will apply the changes to the database schema.

Remember to create a new migration and upgrade the database each time you make changes to your models.
7. Run the Flask application:
   ```bash
   python app.py
   ```

8. Access the web app in your web browser at `http://localhost:80`.

## Usage
1. Open your web browser and go to `http://localhost:80`.

2. Enter the location for which you want to scrape housing leads on the web interface.

3. Click the "Scrape Leads" button to initiate the scraping process.

4. The scraped data will be stored in the SQLite database and also exported to the Google Sheets spreadsheet.

5. You can view the scraped data on the web page, and it will be automatically updated daily by a scheduled task.

6. To delete a location's data, click the "Delete" button next to the location on the web page.

7. To delete a specific scraped data entry, click the "Delete" button next to the data entry on the web page.

## Contributing
Contributions to this project are welcome. If you have any suggestions, bug fixes, or improvements, please open an issue or submit a pull request.


## Acknowledgments
- This project uses Flask, SQLAlchemy, and other open-source libraries.
- Data scraping from Redfin is performed using a custom scraper.
- Data updates are scheduled using the `apscheduler` library.

## Disclaimer
This application is intended for educational and personal use. Scraping websites may violate their terms of service, so use it responsibly and in accordance with Redfin's policies. Be aware of legal and ethical considerations when scraping data from websites.
