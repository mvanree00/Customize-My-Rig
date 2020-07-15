import requests
import bs4
from datetime import datetime,timezone
from homepage.models import *
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
def checkPart(obj): # makes sure price is actually correct and in stock
    if obj.last_updated:
        duration = datetime.now(timezone.utc) - obj.last_updated
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        if hours < 6: # less than 6 hours since price last updated
            return True
        else:
            obj.last_updated=datetime.now(timezone.utc)
            obj.save()
    else:
        obj.last_updated=datetime.now(timezone.utc)
        obj.save()
    output = getLink(obj.links)
    if output == 'OOS':
        obj.price=None
        obj.webpage=None
        obj.save()
    elif output[1] != obj.price: # if not same price as updated
        obj.webpage=output[0]
        if output[1]<obj.price:
            obj.price=output[1]
            obj.save()
            return True
        obj.price=output[1]
        obj.save()
    else:
        return True
    return False