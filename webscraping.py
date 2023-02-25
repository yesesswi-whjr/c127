from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
start_url="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("C:/Python311/c127/chromedriver.exe")
browser.get(start_url)
time.sleep(10)

def scrape():
    headers=["name","distance","mass","radius"]
    stardata=[]
    for i in range(0,210):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","brightest_stars"}):
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
                stardata.append(templist)
        browser.find_element("xpath",'//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        with open("starscrape.csv","w")as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(headers)
            csvwriter.writerows(stardata)
scrape()
    