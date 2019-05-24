from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
#    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
# browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    mars_data = {}

    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('div', class_="slide")
    try:
        # Identify and return title of listing
        news_title = results[0].find('div', class_="content_title").text
        # Identify and return paragraph
        news_p = results[0].find('div', class_="rollover_description_inner").text
    except AttributeError as e:
        print(e)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p
    }
 
     # Close the browser after scraping
    browser.quit()

    return mars_data

#print(scrape())