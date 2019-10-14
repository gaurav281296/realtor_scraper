import pandas,math,re
from bs4 import BeautifulSoup
import threading
import requests
import random
import time
from selenium import webdriver

delays = [7,8,9,10,11]

def get_details(re_dict):
    with webdriver.Chrome(executable_path='./chromedriver') as dr:
        search_url = ''.join(re_dict["Link"])
        print(search_url)
        dr.get(search_url)
        time.sleep(random.choice(delays))
        soup=BeautifulSoup(dr.page_source, "html.parser")
        neighborhood=soup.find_all("div", {"class":"neighborhood-max-width-sm padding-bottom"})
        try:
            neighbor = neighborhood[0].find('p').text
            re_dict["neighborhood"] = re.search('is located in (.*) neighborhood in the city of ', neighbor).group(1)
        except Exception as e:
            re_dict["neighborhood"] = "NOT LISTED"
        
        soup=BeautifulSoup(dr.page_source, "html.parser")
        details = soup.find_all("li", {"class":"ldp-key-fact-item"})
        for detail in details:
            try:
                re_dict[detail.find("div").text] = detail.find("div",{"class":"key-fact-data ellipsis"}).text.strip()
            except Exception as e:
                pass
        try:
            soup = BeautifulSoup(dr.page_source,"html.parser")
            table = soup.find("div",{"class":"listing-subsection listing-subsection-price"})
            table = table.find("table",{"class":"table"})
            prop_hist = pandas.read_html(table.prettify())[0]
        except Exception as e:
            prop_hist = pandas.DataFrame()
        prop_hist.to_csv("./prop_history/"+re_dict["Link"].split("/")[-1]+".csv")

        

def get_homes(soup, re_list, page_counter):
    if page_counter!=1:
        with webdriver.Chrome(executable_path='./chromedriver') as dr:
            search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA/pg-',(str(page_counter))])
            print(search_url)
            dr.get(search_url)
            time.sleep(random.choice(delays))
            soup=BeautifulSoup(dr.page_source,"html.parser")
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


dr = webdriver.Chrome(executable_path='./chromedriver')
base_url='https://www.realtor.com'
re_list=[]
realtor_default_count=44
page_counter=1
search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA'])
dr.get(search_url)
time.sleep(random.choice(delays))
soup=BeautifulSoup(dr.page_source, "html.parser")
total_homes=soup.find("span",{"class":"srp-footer-found-listing"}).text.strip().replace("\n","")
total_homes=int(re.sub('[^0-9]','', total_homes))
total_pages=math.ceil(total_homes/realtor_default_count)
dr.close()
print("total_pages: {}".format(total_pages))
while page_counter <= total_pages:
    get_homes(soup, re_list, page_counter)
    page_counter+=1
    
re_df=pandas.DataFrame(re_list)
re_df.to_csv("RealtorData.csv")