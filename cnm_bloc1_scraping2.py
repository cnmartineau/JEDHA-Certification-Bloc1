
# scrap accomodation information from list of urls

# import libraries
import json
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# get list of urls from file
file = open("cnm_bloc4_data2_urls.json")
file = json.load(file)
list_urls = [element["url"] for element in file]

# define spider
class BookingSpider2(scrapy.Spider):

    # name of the spider
    name = "booking2"

    # starting URLs
    start_urls = list_urls

    # parse function to scrap data
    def parse(self, response):

        # set driver and waiting time
        driver = webdriver.Chrome()
        driver.get(response.request.url)
        driver.implicitly_wait(0.5)

        # get data
        try:
            city = driver.find_element(By.ID, ":Rp5:").get_attribute("value")
        except:
            city = None
        try:
            name = driver.find_element(By.CLASS_NAME, "d2fee87262").text
        except:
            name = None
        try:
            address = driver.find_element(By.CLASS_NAME, "hp_address_subtitle").text
        except:
            address = None
        try:
            coordinates = driver.find_element(By.ID, "hotel_address").get_attribute("data-atlas-latlng")
        except:
            coordinates = "None,None"
        try:
            score = driver.find_element(By.CLASS_NAME, "b5cd09854e").text
        except:
            score = None
        try:
            descriptions = driver.find_elements(By.ID, "property_description_content")
            description = [paragraph.text for paragraph in descriptions]
        except:
            description = None

        return {
            "city_name": city,
            "hotel_name": name,
            "hotel_url": response.request.url,
            "hotel_address": address,
            "hotel_latitude": coordinates.split(",")[0],
            "hotel_longitude": coordinates.split(",")[1],
            "hotel_score": score,
            "hotel_description": description
        }

# name of the file where the results will be saved
filename = "cnm_bloc1_data3_hotels.json"

# delete previous file before crawling
if filename in os.listdir():
    os.remove(filename)

# declare crawlerProcess 
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/113.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename : {"format": "json"},
    }
})

# start the crawling 
process.crawl(BookingSpider2)
process.start()