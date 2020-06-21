from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
import time

url1 = "https://www.investing.com/indices/investing.com-btc-usd"
url2 = "https://www.investing.com/indices/us-spx-500"


driver1 = webdriver.Firefox(executable_path="./drivers/geckodriver")
driver2 = webdriver.Firefox(executable_path="./drivers/geckodriver")
driver1.get(url1)
driver2.get(url2)

while 1 == 1:

    content_element = driver1.find_element_by_id("last_last")
    content_html = content_element.get_attribute("innerHTML")
    soup1 = BeautifulSoup(content_html, "html.parser")
    
    content_element = driver2.find_element_by_id("last_last")
    content_html = content_element.get_attribute("innerHTML")
    soup2 = BeautifulSoup(content_html, "html.parser")

    
    

    print(soup1)
    print(soup2)