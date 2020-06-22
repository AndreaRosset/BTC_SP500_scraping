from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pika
import threading
import json
import time

#firefox_driver = "./drivers/geckodriver"
chrome_driver = "./drivers/chromedriver"
rabbitMQ = 'localhost'

url_btc_usd = "https://www.investing.com/indices/investing.com-btc-usd"
url_SP500 = "https://www.investing.com/indices/us-spx-500"

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQ))
channel = connection.channel()
BTC_channel = connection.channel()
SP500_channel = connection.channel()
channel.queue_declare(queue='BTC+SP500')
BTC_channel.queue_declare(queue='BTC')
SP500_channel.queue_declare(queue='SP500')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox");

driver1 = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
driver2 = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
driver1.get(url_btc_usd)
driver2.get(url_SP500)

def get_element_value():
    threading.Timer(0.5, get_element_value).start()
    
    content_element = driver1.find_element_by_id("last_last")
    content_html = content_element.get_attribute("innerHTML")
    soup1 = BeautifulSoup(content_html, "html.parser")
    
    content_element = driver2.find_element_by_id("last_last")
    content_html = content_element.get_attribute("innerHTML")
    soup2 = BeautifulSoup(content_html, "html.parser")

    new_data_entry = { 
        "timestamp":time.time(), 
        "BTC_value": str(soup1), 
        "SP500_value": str(soup2)
    }
    
    new_data_entry = json.dumps(new_data_entry)
    
    infos = channel.basic_publish(exchange='',
                      routing_key='BTC+SP500',
                      body=new_data_entry)
    print(infos)
    
get_element_value()