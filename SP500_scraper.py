from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pika
import threading
import json
import time

chrome_driver = "./drivers/chromedriver"
rabbitMQ = "localhost"

url_SP500 = "https://www.investing.com/indices/us-spx-500"

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQ))
SP500_channel = connection.channel()
SP500_channel.queue_declare(queue='SP500')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)

driver.get(url_SP500)

def get_sp500_value():
    threading.Timer(0.5, get_sp500_value).start()
    
    content_element = driver.find_element_by_id("last_last")
    content_html = content_element.get_attribute("innerHTML")
    soup = BeautifulSoup(content_html, "html.parser")

    new_data_entry = { 
        "timestamp":time.time(), 
        "SP500_value": str(soup)
    }
    
    new_data_entry = json.dumps(new_data_entry)
    
    SP500_channel.basic_publish(exchange='',
                      routing_key='SP500',
                      body=new_data_entry)
    
get_sp500_value()