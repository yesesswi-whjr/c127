from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import requests
start_url="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("C:/Python311/c127/chromedriver.exe")
browser.get(start_url)
time.sleep(10)

headers=["name","distance","mass","radius"]
stardata=[]

def scrape():
 
    
    for i in range(1,5):
        while  True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            current_page_number=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_number<i:
                browser.find_element("xpath",'//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_number>i:
                browser.find_element("xpath",value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul",attrs={"class","List_of_brightest_stars_and_other_record_stars"}):
                li_tags=ul_tag.find_all("li")
                templist=[]
                for index,li_tag in enumerate(li_tags):
                    if index==0:
                     templist.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            templist.append(li_tag.contents[0])
                        except:
                            templist.append("")
                hyperlink_li_tag=li_tags[0]
                templist.append("https://en.wikipedia.org/wiki/"+ hyperlink_li_tag.find_all("a",href=True)[0]["href"])
                
                stardata.append(templist)

        browser.find_element("xpath",'//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print("page scraping completed")

        
scrape()
stardata=[]   
def scrapemore(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    templist.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        stardata.append(templist)            
    except:
        time.sleep(1)
        scrapemore(hyperlink)
for index, data in enumerate(stardata):
    scrapemore(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(stardata[0:10])

final_planet_data = []

for index, data in enumerate(stardata):
    new_star_data_element = stardata[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    new_star_data_element = new_planet_data_element[:7]
    final_star_data.append(data + new_planet_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_star_data)