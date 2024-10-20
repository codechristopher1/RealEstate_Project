import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os


class GoogleSheetClient:
    def __init__(self, credentials_env_var, google_sheet_url, sheet_name=None):
        # Load environment variables
        load_dotenv()

        # Path to your credentials file from the environment variable
        self.credentials_file = os.getenv(credentials_env_var)

        if self.credentials_file is None:
            raise ValueError(f"Environment variable '{credentials_env_var}' not set.")
        elif not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"The credentials file does not exist at: {self.credentials_file}")

        # Authenticate using the service account credentials
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.scope)
        self.client = gspread.authorize(self.creds)

        # Open the Google Sheet by URL
        self.spreadsheet = self.client.open_by_url(google_sheet_url)
        if sheet_name is not None:
            self.sheet = self.spreadsheet.worksheet(sheet_name)



    def get_headers(self, row_number=2):
        try:

            # Fetch all headers from the specified row
            all_headers = self.sheet.row_values(row_number)
        
            # Define the range of headers you're interested in (from '#' to 'Commute')
            start_column = all_headers.index('#')  # Column where '#' is located
            end_column = all_headers.index('Days to pending') + 1  # Column where 'Commute' is located (inclusive)
        
            # Slice the list to get only the required headers
            filtered_headers = all_headers[start_column:end_column]
        
            return filtered_headers
        except Exception as e:
            print('Error getting headers:', e)



    def get_last_index(self):
        """
        Get the last index from the `#` column, which is the first column.
        """
        all_values = self.sheet.col_values(1)  # Get all values in the first column
        if len(all_values) > 1:
            return int(all_values[-1])  # Get the last index as an integer
        else:
            return 0  # If there are no rows, start from 0



    def add_row(self, row_data):
        try:
            # Append a new row to the sheet with the scraped data
            self.sheet.append_row(row_data)
            print(f"Row added: {row_data}")
        except Exception as e:
            print('Error updating row data:',e)



    def delete_rows(self, row_numbers):
        try:
            # Sort the row numbers in reverse order to prevent row shifting issues
            row_numbers = sorted(row_numbers, reverse=True)
            
            for row_number in row_numbers:
                self.sheet.delete_rows(row_number)
                print(f"Row {row_number} deleted.")
        
        except Exception as e:
            print(f"Error deleting rows: {e}")



    def get_column_letter(self, n):
        """Convert a 1-based column index to an Excel-style column letter (A, B, C, ..., Z, AA, AB, ..., etc.)."""
        letter = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter



    def create_new_sheet(self, sheet_name, headers, rows=1000, cols=37):
        """
        Create a new worksheet (sheet) within the spreadsheet and set column headers.
        Parameters:
        - sheet_name: Name of the new sheet to be created.
        - headers: List of column headers to be set in the first row.
        - rows: Number of rows for the new sheet (default is 100).
        - cols: Number of columns for the new sheet (default is 26).
        """
        try:
            # Add a new worksheet to the spreadsheet
            new_sheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=rows, cols=cols)
            print(f"New sheet '{sheet_name}' created with {rows} rows and {cols} columns.")
            
            # Ensure the number of headers does not exceed the column limit
            if len(headers) > cols:
                raise ValueError(f"Number of headers ({len(headers)}) exceeds the number of columns ({cols}).")
            
            # Add headers to the first row
            cell_list = new_sheet.range(1, 1, 1, len(headers))  # First row, from column 1 to len(headers)
            for i, header in enumerate(headers):
                cell_list[i].value = header
            new_sheet.update_cells(cell_list)

            # new_sheet.update('A2', [[1]])

            header_range = f"A1:{self.get_column_letter(len(headers))}1"  # From A1 to the last header column (e.g., D1)
            new_sheet.format(header_range, {
                "textFormat": {"bold": True}
            })
    
            print(f"Headers added to '{sheet_name}': {headers}")
            return new_sheet
        except Exception as e:
            print(f"Error creating new sheet '{sheet_name}':", e)
            return None
    



    
