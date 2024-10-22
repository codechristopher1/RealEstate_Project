import time
import re
from lxml import etree
from rich import print
from dataclasses import asdict, dataclass
from curl_cffi import requests as cureq
from dotenv import load_dotenv
import os


@dataclass
class Item:
    no_of_MF_for_sale: str | None
    avg_pri_UFR: str | None
    YOY_Growth1: str | None
    no_of_homes_sold: str | None
    YOY_Growth2: str | None
    MDOM: str | None
    YOY_Growth: str | None
    sale_to_list_price: str | None
    avg_home_sale: str | None
    Days_to_pending: str | None


class RedFinScraper:
    
    def __init__(self, base_url):
        self.base_url = base_url
        

    def get_html(self, url):
        """Send request and get the HTML body as response."""
        load_dotenv()
        try:
            resp = cureq.get(url, impersonate='chrome', proxy=os.getenv("PROXY"))
            resp.raise_for_status()
            html = etree.HTML(resp.content)
            return html

        except cureq.exceptions.RequestException as e:
            print(f"HTTP Request failed: {str(e)}")
            return None
        except Exception as e:
            print(f"Error sending request: {str(e)}")
            return None

    
    def extract_text(self, html, sel):
        """Extract the text from the given XPath selector."""
        try:
            result = html.xpath(sel)
            text = result[0] if result else None
            if text:
                return self.clean_data(text)
        except AttributeError:
            return None


    def clean_data(self,value):
        """Clean the extracted text data."""
        try:
            if value:
                return value.strip().replace(' pt', '')
            return None
        except Exception as e:
            print('Error cleaning data:', e)


    def clean_data_days(self, value):
        if value:
            # Strip leading/trailing spaces
            value = value.strip()
            
            # Use regex to find the last occurrence of a number followed by 'days'
            match = re.search(r'(\d+ days)', value)
            
            if match:
                return match.group(1)
        
        return None



    def parse_page(self, html):
        """Parse product page and get product details."""
        new_item = Item(
            no_of_MF_for_sale= '',
            avg_pri_UFR=self.extract_text(html, '(//div[@class="value"]/text())[1]'),
            YOY_Growth1= self.extract_text(html, '//div[contains(text(), "Median Sale Price")]/following-sibling::div/div/following-sibling::div/text()'),
            no_of_homes_sold=self.extract_text(html, '(//div[@class="value"]/text())[2]'),
            YOY_Growth2=self.extract_text(html, '//div[contains(text(), "# of Homes Sold")]/following-sibling::div/div/following-sibling::div/text()'),
            MDOM=self.extract_text(html, '(//div[@class="value"]/text())[3]'),
            YOY_Growth=self.extract_text(html, '(//div[@class="yoyChange font-b1 pct-up"]/text())[1]'),
            sale_to_list_price=self.extract_text(html, '//div[contains(text(),"Sale-to-List Price")]/following-sibling::div/div[@class="value"]/text()'),
            avg_home_sale=self.extract_text(html, '//div[contains(text(), "Sale-to-List Price")]/following-sibling::div/div/following-sibling::div/text()'),
            Days_to_pending= self.clean_data_days(self.extract_text(html, '(//ul[@class="details"]/li[2]/span//text())[4]'))
            
        )
        return asdict(new_item)


    def scrape(self):
        """Control the flow of scraping all pages."""
        
        url = self.base_url
        html = self.get_html(url)
        if html is not None:
            time.sleep(2)
            scraper2_data= self.parse_page(html)
            # print('scraper2_data:', scraper2_data)
            return scraper2_data
        else:
            print(f"Failed to get HTML")


