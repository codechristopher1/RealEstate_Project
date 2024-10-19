import time
from lxml import etree
from rich import print
from dataclasses import asdict, dataclass
from curl_cffi import requests as cureq
from headers import HEADER_TO_FIELD_MAP, MergedItem
from GoogleClient import GoogleSheetClient
from Redfin import RedFinScraper


@dataclass
class Item:
    city: str | None
    neighborhood: str | None
    image: str | None
    zipcode: str | None
    ranking_in_city: str | None
    overall_grade: str | None
    short_description: str | None
    population: str | None
    median_home_value: str | None
    rent: str | None
    rent_value: str | None
    rent_own: str | None
    schools: str | None
    housing: str | None
    good_for_families: str | None
    jobs: str | None
    cost_of_living: str | None
    outdoor_activities: str | None
    crime_safety: str | None
    nightLife: str | None
    diversity: str | None
    weather: str | None
    health_fitness: str | None
    commute: str | None

class NeighborhoodScraper:
    
    def __init__(self, base_url, google_sheet_url, redfin_url, google_sheet_credentials, sheetname, pages_to_scrape=1):
        self.base_url = base_url
        self.gs = GoogleSheetClient(google_sheet_credentials, google_sheet_url, sheetname)
        if sheetname == 'Data':
            self.headers = self.gs.get_headers()
        else:
            self.headers = self.gs.get_headers(row_number=1)

        self.pages_to_scrape = pages_to_scrape
        self.scraper2= RedFinScraper(base_url= redfin_url) 
        


    def get_html(self, url):
        """Send request and get the HTML body as response."""
        try:
            resp = cureq.get(url, impersonate='chrome')
            resp.raise_for_status()
            html = etree.HTML(resp.content)
            return html

        except cureq.exceptions.RequestException as e:
            print(f"HTTP Request failed: {str(e)}")
            return None
        except Exception as e:
            print(f"Error sending request: {str(e)}")
            return None



    def parse_links(self, html):
        """Parse the HTML body and extract content using XPath."""
        try:
            listings = html.xpath('//div[@class="card search-result"]')
            for li in listings:
                yield li.xpath('./a/@href')[0]
        except AttributeError as e:
            print('Error parsing link:', e)


    
    def extract_text(self, html, sel):
        """Extract the text from the given XPath selector."""
        try:
            result = html.xpath(sel)
            text = result[0] if result else None
            return self.clean_data(text)
        except AttributeError:
            return None


    
    def clean_data(self,value):
        """Clean the extracted text data."""
        try:
            if value:
                return value.strip().replace('minus', '-').replace(' -', '-')
            return None
        except Exception as e:
            print('Error cleaning data:', e)


   
    def parse_page(self, html, link):
        """Parse product page and get product details."""
        new_item = Item(
            city=self.extract_text(html, '//a[@class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover postcard__parent nss-n3qyvd"]/text()'),
            neighborhood=self.extract_text(html, '//h1/text()'),
            image=link,
            zipcode= '',
            ranking_in_city=self.extract_text(html, "//div[@class='postcard__badge']/a/em/text()[2]"),
            overall_grade=self.extract_text(html, "//ul[@class='postcard__attrs']/li/span/div/text()"),
            short_description=self.extract_text(html, "//div[@class='blank__bucket']/span/text()"),
            population=self.extract_text(html, "//div[@class='scalar']/div/span[contains(text(), 'Population')]/following::div[1]/span/text()"),
            median_home_value=self.extract_text(html, "//div[@class='scalar']/div/span[contains(text(), 'Median Home Value')]/following::div[1]/span/text()"),
            rent=self.extract_text(html, "//div[@class='scalar']/div/span[contains(text(), 'Median Rent')]/following::div[1]/span/text()"),
            rent_value= '',
            rent_own=self.extract_text(html, "//ul[@class='breakdown-facts']/li/div[@class='fact__table__row__value']/text()"),
            schools=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Public Schools')]/following-sibling::div/text()"),
            housing=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Housing')]/following-sibling::div/text()"),
            good_for_families=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Good for Families')]/following-sibling::div/text()"),
            jobs=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Jobs')]/following-sibling::div/text()"),
            cost_of_living=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Cost of Living')]/following-sibling::div/text()"),
            outdoor_activities=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Outdoor Activities')]/following-sibling::div/text()"),
            crime_safety=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Crime & Safety')]/following-sibling::div/text()"),
            nightLife=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Nightlife')]/following-sibling::div/text()"),
            diversity=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Diversity')]/following-sibling::div/text()"),
            weather=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Weather')]/following-sibling::div/text()"),
            health_fitness=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Health & Fitness')]/following-sibling::div/text()"),
            commute=self.extract_text(html, "//div[@class='profile-grade--two']/div[contains(text(), 'Commute')]/following-sibling::div/text()")
        )
        return asdict(new_item)


   
    def merged_item(self, scraper1_data, scraper2_data):
        # Create merged data using keys and values from both scraper1_data and scraper2_data
        try:
            merged_data = {
                key: scraper1_data.get(key, scraper2_data.get(key)) for key in set(scraper1_data) | set(scraper2_data)
            }
            
            # Convert the merged data to MergedItem object
            merged_item = MergedItem(
                city=merged_data.get('city'),
                neighborhood=merged_data.get('neighborhood'),
                image=merged_data.get('image'),
                zipcode=merged_data.get('zipcode'),
                ranking_in_city=merged_data.get('ranking_in_city'),
                overall_grade=merged_data.get('overall_grade'),
                short_description=merged_data.get('short_description'),
                population=merged_data.get('population'),
                median_home_value=merged_data.get('median_home_value'),
                rent=merged_data.get('rent'),
                rent_value=merged_data.get('rent_value'),
                rent_own=merged_data.get('rent_own'),
                schools=merged_data.get('schools'),
                housing=merged_data.get('housing'),
                good_for_families=merged_data.get('good_for_families'),
                jobs=merged_data.get('jobs'),
                cost_of_living=merged_data.get('cost_of_living'),
                outdoor_activities=merged_data.get('outdoor_activities'),
                crime_safety=merged_data.get('crime_safety'),
                nightLife=merged_data.get('nightLife'),
                diversity=merged_data.get('diversity'),
                weather=merged_data.get('weather'),
                health_fitness=merged_data.get('health_fitness'),
                commute=merged_data.get('commute'),
                no_of_MF_for_sale=merged_data.get('no_of_MF_for_sale'),
                avg_pri_UFR=merged_data.get('avg_pri_UFR'),
                YOY_Growth1=merged_data.get('YOY_Growth1'),
                no_of_homes_sold=merged_data.get('no_of_homes_sold'),
                YOY_Growth2=merged_data.get('YOY_Growth2'),
                MDOM=merged_data.get('MDOM'),
                YOY_Growth=merged_data.get('YOY_Growth'),
                avg_home_sale=merged_data.get('avg_home_sale'),
                sale_to_list_price=merged_data.get('sale_to_list_price'),
                Days_to_pending=merged_data.get('Days_to_pending')
            )
        
            return asdict(merged_item)
        except Exception as e:
            print(f"Error merging data between scraper1 and scraper2: {e}")
            print(f"scraper1_data: {scraper1_data}")
            print(f"scraper2_data: {scraper2_data}")

 

    def append_data_to_sheet(self, item):
        item_dict = item  # Assuming item is already a dictionary or from asdict(Item)
        
        data_to_append = []
        
        for header in self.headers:
            field_name = HEADER_TO_FIELD_MAP.get(header.strip())  # Find the corresponding field name
            value = item_dict.get(field_name) if field_name else None  # Get the value from the item
            data_to_append.append(value)

        try:
            # Append the row data to the sheet
            self.gs.add_row(data_to_append)
        except Exception as e:
            print(f"Error appending data to sheet: {str(e)}")



    def scrape(self):
        """Control the flow of scraping all pages."""
        try:
            for page in range(1, self.pages_to_scrape + 1):
                url = self.base_url.format(page)
                html = self.get_html(url)
    
                if html is not None:
                    links = list(self.parse_links(html))
                    time.sleep(2)
                    print(f'Got {len(links)} Links from page: {page}')
    
                    last_index = self.gs.get_last_index()
                    if last_index == 0:
                        last_index = 1
                    else:
                        last_index += 1
    
    
                    for link in links: 
                        print('processing Link....')
                        print(f'Getting page Details from Link: {link}...')
                        page_html = self.get_html(link)
                        if page_html is not None:
                            time.sleep(2)
                            scraper1_data= self.parse_page(page_html, link)
                            scraper2_data= self.scraper2.scrape()
                            
                            if scraper2_data is None:
                                print("scraper2_data returned None, skipping merging")
                            else:
                                item= self.merged_item(scraper1_data, scraper2_data)
                                print('Merged_Item:',item)
    
    
                            last_index += 1
                            item['index'] = last_index
                            self.append_data_to_sheet(item)
                            print("Sheet has been updated successfully.")
    
                        else:
                            print(f"Failed to get page_HTML for {link}")
    
                else:
                    print(f"Failed to get HTML for page: {page}")
        except Exception as e:
            print(f'Error running scrape: {e}')

       

# if __name__ == "__main__":
#     google_sheet_url = 'https://docs.google.com/spreadsheets/d/1nCBBF7Fh141aTi4TRiyU7wt32Mmf8gdSF4J5InWvlog/edit?gid=0#gid=0'
#     google_sheet_credentials = "GOOGLE_SHEET_CREDENTIALS"

#     scraper = NeighborhoodScraper(
#         base_url= 'https://www.niche.com/places-to-live/search/best-neighborhoods/t/chicago-cook-il/' + '?page={}',
#         redfin_url= 'https://www.redfin.com/city/16657/TX/San-Antonio/housing-market',
#         google_sheet_url= google_sheet_url,
#         google_sheet_credentials= google_sheet_credentials,  
#         sheetname= 'Testsheet2',
#     )
#     scraper.scrape()
#     print("Scraping completed.")
   
