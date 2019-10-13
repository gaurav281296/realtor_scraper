import pandas,math,re
from bs4 import BeautifulSoup
import threading
import requests
import random
import time
import socket
import socks
from stem import Signal
from stem.control import Controller

controller = Controller.from_port(port=9051)

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

def renew_tor():
    controller.authenticate('my_password')
    controller.signal(Signal.NEWNYM)

def show_my_ip():
    url = "https://httpbin.org/ip"
    r = requests.Session()
    page = r.get(url)
    print(page.content)


#some common user agents
user_agent_list = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0	Firefox 33',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; de-de) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)'
]

def get_details(re_dict):
    search_url = ''.join(re_dict["Link"])
    print(search_url)
    try:
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        r = requests.Session()
        page=r.get(url=search_url,headers=headers)

        #page=tr.get(url=search_url,headers=headers)

        c=page.content
        soup=BeautifulSoup(c,"html.parser")
        neighborhood=soup.find_all("div", {"class":"neighborhood-max-width-sm padding-bottom"})
    except Exception as e:
        time.sleep(2)
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        renew_tor()
        connectTor()
        show_my_ip()
        r = requests.Session()
        page=r.get(url=search_url,headers=headers)
        c=page.content
        soup=BeautifulSoup(c,"html.parser")
        neighborhood=soup.find_all("div", {"class":"neighborhood-max-width-sm padding-bottom"})
    try:
        neighbor = neighborhood[0].find('p').text
        neighborhood_area = re.search('is located in (.*) neighborhood in the city of ', neighbor).group(1)
    except Exception as e:
        neighborhood_area = "NOT LISTED"
    re_dict["neighborhood"] = neighborhood_area
        

def get_homes(soup, re_list, page_counter):
    print(page_counter)
    if page_counter!=1:
        search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA/pg-',(str(page_counter))])
        
        try:
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            r = requests.Session()
            page=r.get(url=search_url,headers=headers)
            c=page.content
            soup=BeautifulSoup(c,"html.parser")
            re_data=soup.find_all("li", {"class":"component_property-card js-component_property-card js-quick-view"})
        except Exception as e:
            time.sleep(2)
            renew_tor()
            connectTor()
            show_my_ip()
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            r = requests.Session()
            page=r.get(url=search_url,headers=headers)
            c=page.content
            soup=BeautifulSoup(c,"html.parser")
            re_data=soup.find_all("li", {"class":"component_property-card js-component_property-card js-quick-view"})
        
        print(search_url)
    re_data=soup.find_all("li", {"class":"component_property-card js-component_property-card js-quick-view"})
    for item in re_data:
        re_dict={}
        re_dict["Property Type"]=item.find("div",{"class":"property-type"}).text
    
        try:
            re_dict["Price"]=item.find("span",{"class":"data-price"}).text
        except:
            re_dict["Price"]="NOT LISTED"
        try:
            community = item.find("span",{"class":"listing-community"}).text.strip()
            community = community + " "
        except:
            pass
        try:
            re_dict["Address"]=community + item.find("span",{"class":"listing-street-address"}).text.strip().replace(",","")
        except:
            re_dict["Address"]="NOT LISTED"
        try:
            re_dict["Locality"]=item.find("span",{"class":"listing-city"}).text + ", " + item.find("span",{"class":"listing-region"}).text + " " + item.find("span",{"class":"listing-postal"}).text
        except:
            re_dict["Locality"]="NOT LISTED"
        try:
            re_dict["Beds"]=item.find("li",{"data-label":"property-meta-beds"}).text.strip()
        except:
            re_dict["Beds"]="NOT LISTED"
        try:
            re_dict["Baths"]=item.find("li",{"data-label":"property-meta-baths"}).text.strip()
        except:
            re_dict["Baths"]="NOT LISTED"
        try:
            re_dict["Home Size"]=item.find("li",{"data-label":"property-meta-sqft"}).text.strip()
        except:
            re_dict["Home Size"]="NOT LISTED"
        try:
            re_dict["Lot Size"]=item.find("li",{"data-label":"property-meta-lotsize"}).text.strip()
        except:
            re_dict["Lot Size"]="NOT LISTED"
        try:
            re_dict["Garage"]=item.find("li",{"data-label":"property-meta-garage"}).text.strip()
        except:
            re_dict["Garage"]="NOT LISTED"
        try:
            re_dict["Construction"]=item.find("span",{"data-label":"property-label-new_construction"}).text.strip()
        except:
            pass
        re_dict["Link"]=base_url + item['data-url']
        get_details(re_dict)
        re_list.append(re_dict)
        community=""



renew_tor()
connectTor()
show_my_ip()
print("connected to tor")
base_url='https://www.realtor.com'
re_list=[]
realtor_default_count=44
page_counter=1
search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA'])
try:
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    r = requests.Session()
    page=r.get(url=search_url,headers=headers)

    #page=tr.get(url=search_url,headers=headers)

    c=page.content
    soup=BeautifulSoup(c,"html.parser")
    total_homes=soup.find("span",{"class":"srp-footer-found-listing"}).text.strip().replace("\n","")
except Exception as e:
    time.sleep(2)
    renew_tor()
    connectTor()
    show_my_ip()
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    r = requests.Session()
    page=r.get(url=search_url,headers=headers)
    
    #page=tr.get(url=search_url,headers=headers)
    
    c=page.content
    soup=BeautifulSoup(c,"html.parser")
    print(soup)
    total_homes=soup.find("span",{"class":"srp-footer-found-listing"}).text.strip().replace("\n","")
total_homes=int(re.sub('[^0-9]','', total_homes))
total_pages=math.ceil(total_homes/realtor_default_count)
print(total_pages)
while page_counter <= total_pages:
    get_homes(soup, re_list, page_counter)
    page_counter+=1
    
re_df=pandas.DataFrame(re_list)
re_df.to_csv("RealtorData.csv")