
# scrap urls of top-25 accomodations from list of cities

# import libraries
import pandas as pd
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# get list of cities from file
data = pd.read_csv("cnm_bloc4_data1_weather.csv")
cities = data["city_name"].values

# define spider
class BookingSpider(scrapy.Spider):

    # name of the spider
    name = "booking"

    # url to start the spider from 
    start_urls = ["https://www.booking.com/index.fr.html"]

    # parse function for form request
    def parse(self, response):
        for city in cities:
            yield scrapy.FormRequest.from_response(
                response,
                formid = "input_destination",
                formdata = {"ss": city},
                callback = self.after_city_search,
                cb_kwargs = dict(city_current = city)
            )

    # callback used after city search
    def after_city_search(self, response, city_current):

        # set driver and waiting time
        driver = webdriver.Chrome()
        driver.get(response.request.url)
        driver.implicitly_wait(0.5)

        # get data
        hotels = driver.find_elements(By.CLASS_NAME, "e13098a59f")
        for hotel in hotels:
            yield {
                "city": city_current,
                "url": hotel.get_attribute("href")
            }

# name of the file where the results will be saved
filename = "cnm_bloc1_data2_urls.json"

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
process.crawl(BookingSpider)
process.start()