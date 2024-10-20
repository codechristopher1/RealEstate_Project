# Project Name:Real Estate Data Collection

### Description
"""
This project is a web scraper that extracts information about neighborhoods from a specified website and appends the data to a Google Sheet. 
The scraper is configured to:

- Send HTTP requests to fetch HTML content from the target website.

-Extract neighborhood data such as city, neighborhood name, ranking, population, median home value, rent, schools, jobs, and more using XPath.

- Clean and format the extracted data.

- Append the data to a Google Sheet, ensuring structured organization of fields such as city, ranking_in_city, median_home_value, etc.

-The scraper iterates through multiple pages of neighborhood listings, gathering the required information for analysis.

This script is designed to automate the process of gathering neighborhood data for market research or data analysis projects.

Main.py:
  This script allows user to perform two main tasks:

-Create a new Google Sheet with pre-defined headers.
-Scrape data from website and update an existing Google Sheet with the scraped information.
-Exit the program.

The user can choose between creating a new sheet or running a scraper that extracts neighborhood information from a specified URL or Exit the program. 
The scraper processes multiple pages and appends the data to a Google Sheet.

Key components include:

GoogleSheetClient: Manages interactions with Google Sheets (creating new sheets, appending data).
NeighborhoodScraper: Handles scraping neighborhood-related data from the provided URL and formats it into a structure that can be added to Google Sheets.
Exit: Exit the program.


"""
### Features
- niche.py: Handles scraping neighborhood-related data from the provided niche URL.
- Redfin.py: Handles scraping market data from the provided niche URL
- GoogleClient.py: Manages interactions with Google Sheets.
- main.py: Responsible 'for' the execution and control of the entire program.  

### Requirements
- **Python 3.10+**
- Libraries/Dependencies:
    - see requirements.txt file


### Installation
Explains how to set up the project/program:
1. **Download** the project files.
2. Open a terminal and **navigate** to the project folder: cd project_folder_name
3. Create a virtual environment with this command: python -m venv venv 
4. Save Googlesheet credentials.json file to Environment varieble: setx GOOGLE_SHEET_CREDENTIALS   "C:/{your_path}/{your_path}/Niche/credentials.json".
5. Install the required libraries/dependencies by running on your terminal: pip install -r requirements.txt
6. **Run the program** with command: python main.py
