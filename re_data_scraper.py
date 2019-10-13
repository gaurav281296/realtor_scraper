import pandas,math,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading

def get_homes(soup, re_list, page_counter):
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    dr = webdriver.Chrome(executable_path='./chromedriver', desired_capabilities=capa)
    wait = WebDriverWait(dr, 60)

    print(page_counter)
    if page_counter!=1:
        search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA/pg-',(str(page_counter))])
        print(search_url)
        dr.get(search_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'srp-list')))
        dr.execute_script("window.stop();")
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
        re_list.append(re_dict)
        community=""
    dr.close()



dr = webdriver.Chrome(executable_path='./chromedriver')
base_url='https://www.realtor.com'
re_list=[]
realtor_default_count=44
page_counter=1
search_url=''.join([base_url, '/realestateandhomes-search/Sacramento_CA'])
dr.get(search_url)
soup=BeautifulSoup(dr.page_source,"html.parser")
print("made soup")
total_homes=soup.find("span",{"class":"srp-footer-found-listing"}).text.strip().replace("\n","")
total_homes=int(re.sub('[^0-9]','', total_homes))
total_pages=math.ceil(total_homes/realtor_default_count)
print(total_pages)
dr.close()
while page_counter <= total_pages:
    get_homes(soup, re_list, page_counter)
    page_counter+=1
    
re_df=pandas.DataFrame(re_list)
re_df.to_csv("RealtorData.csv")

