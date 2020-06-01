from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

my_url = "https://www.newegg.com/p/pl?N=100007671%20601295136%20601295137%20601295139%20601295141%20601300154%20601350560%20601350561%20601350562&cm_sp=Cat_CPU-Processors_1-_-Visnav-_-Intel-CPU_4"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {"class": "item-container"})
print(len(containers))

for step in range(len(containers)):

    container = containers[step]
#print(container.text)

    name = container.findAll("a", {"class": "item-title"})
    print(name[0].text)
    price = container.findAll("li", {"class": "price-current"})
    print(price[0].text)