from lxml import etree
from io import StringIO
from rich import print
# from dataclasses import asdict, dataclass
from curl_cffi import requests as cureq

url= 'https://check-long-term-flood-risk.service.gov.uk/risk#'
r= cureq.get(url, impersonate='chrome')
print(r.status_code)
html = etree.HTML(r.content)

parser = etree.HTMLParser()
response = etree.parse(StringIO(str(html)), parser)
print(etree.tostring(response, pretty_print=True).decode())


# title= resp.xpath('//div[@class="govuk-grid-column-two-thirds"]/h1/text()')[0]
# print(title)