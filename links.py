import requests
import bs4
def getLink(extension): # extension is the object 'links' attribute
    res = requests.get('https://pcpartpicker.com/product/'+extension+'/')
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    sels = soup.findAll('tr')
    link = 'http://pcpartpicker.com'+sels[1].find("td").find("a").attrs['href'] #gets link ext
    res = requests.get(link)
    output = res.url
    output = output[:output.find('?')]
    return output