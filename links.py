import requests
import bs4
def getLink(extension): # extension is the object 'links' attribute
    #proxies = {"https": "http://140.227.175.225:1000"}
    #res = requests.get('https://pcpartpicker.com/product/'+extension+'/',proxies=proxies)
    res = requests.get('https://pcpartpicker.com/product/'+extension+'/')
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    sels = soup.findAll('tr')
    f = None
    for i in range(1,len(sels)):
        f = sels[i].find('td',{"class":"td__availability td__availability--inStock"})
        if f:
            val = sels[i].find('td',{"class":"td__finalPrice"}).text
            try:
                val = float(val.strip()[1:])
            except ValueError:
                continue
            link = 'http://pcpartpicker.com'+sels[i].find("td").find("a").attrs['href'] #gets link ext
            res = requests.get(link)
            output = res.url
            output = output[:output.find('?')]
            return [output,val]
    return 'OOS' # set null