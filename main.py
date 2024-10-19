import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.GoogleClient import GoogleSheetClient
from src.niche import NeighborhoodScraper



def main():
    google_sheet_url = 'https://docs.google.com/spreadsheets/d/1nCBBF7Fh141aTi4TRiyU7wt32Mmf8gdSF4J5InWvlog/edit?gid=0#gid=0'
    google_sheet_credentials = "GOOGLE_SHEET_CREDENTIALS"

    # Initialize the GoogleSheetClient object
    Gs = GoogleSheetClient(google_sheet_credentials, google_sheet_url)

    while True:
        print("\nWhat would you like to do?")
        print("1. Create a new Google Sheet")
        print("2. Run the scraper and update sheet")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            # User wants to create a new sheet
            sheet_name = input("Enter the name for the new sheet: ").strip()

            headers = [ "#","City", "Neighborhood", "Image","Zipcode","Ranking in City", "Overall Grade", 
                        'Short descreption','Population', 'Median Home Value','Rent','Rent/Value',
                        'Rent / Own','Schools','Housing', 'Good for Families','Jobs','Cost Of Living',
                        'Outdoors activivties', 'Crime & Safety','Nightlife','Diversity','Weather',
                        'Heath & Fitness','Commute', 'Property Tax Rate', '# of MF for sale',
                        'Average price / unit From Redfin', 'YOY Growth', '# of homes sold', 'YOY Growth', 
                        'Median Days on Market', 'YOY Growth', 'Sale to list price', 'Avg home sale to list price', 
                        'Days to pending'
            ]# Define your headers here

            Gs.create_new_sheet(sheet_name, headers=headers)
            print(f"New sheet '{sheet_name}' created with headers.")


        elif choice == '2':
            # User wants to run the scraper
            URL1 = input('Please enter URL for Niche: ').strip()
            URL2= input('Please enter URL for Redfin: ').strip()
            sheetname= input('please enter sheetname to update data: ').strip()

            while not URL1:
                print('Invalid input. Please enter a valid URL.')
                URL1= input('Please enter URL Niche: ').strip()

            while not URL2:
                print('Invalid input. Please enter a valid URL.')
                URL2= input('Please enter URL Redfin: ').strip()

            while not sheetname:
                print('Invalid input. Please enter a valid sheetname.')
                sheetname= input('please enter sheetname to update data: ').strip()

            if not URL1.endswith('/'):
                URL1 = URL1 + '/'


            # Initialize scraper object and run
            scraper = NeighborhoodScraper(
                base_url= URL1 + '?page={}',
                redfin_url= URL2,
                google_sheet_url= google_sheet_url,
                google_sheet_credentials= google_sheet_credentials,  
                sheetname= sheetname,
                pages_to_scrape=6
            )
            scraper.scrape()
            print("Scraping completed.")

        elif choice == '3':
            # Exit the loop
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose again.")


if __name__ == '__main__':
    main()