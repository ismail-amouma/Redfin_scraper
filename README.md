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

6. Set up the Google Sheets integration (follow the instructions in the `googlesheets_integration.md` file).

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
- Google Sheets integration is achieved using the Google Sheets API.
- Data scraping from Redfin is performed using a custom scraper.
- Data updates are scheduled using the `apscheduler` library.

## Disclaimer
This application is intended for educational and personal use. Scraping websites may violate their terms of service, so use it responsibly and in accordance with Redfin's policies. Be aware of legal and ethical considerations when scraping data from websites.
