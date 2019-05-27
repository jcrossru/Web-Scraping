from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from pandas import *


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

    # URL of jpl image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Visit URL
    browser.visit(jpl_url)
    # Find and click the 'search' button
    browser.click_link_by_partial_text('FULL IMAGE')
   # Retrieve page with the requests module
    response = requests.get(jpl_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soupFigure = BeautifulSoup(response.text, 'html.parser')

    # results are returned as an iterable list
    results = soupFigure.find('a', class_="fancybox")

    imgLink = results['data-fancybox-href']
    featured_img_link = 'https://www.jpl.nasa.gov' + imgLink

    # scrape the table
    res = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    df_values = df[0][1]
    equatorial_diameter = df_values[0] 
    polar_diameter = df_values[1] 
    mass = df_values[2] 
    moons = df_values[3] 
    orbit_distance = df_values[4] 
    orbit_period = df_values[5] 
    surface_temperature = df_values[6] 
    first_record = df_values[7] 
    recorded_by = df_values[8] 

    # get mars weather
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    weather_resp = requests.get(mars_weather_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    weather_soup = BeautifulSoup(weather_resp.text, 'html.parser')
    # results are returned as an iterable list
    weather_results = weather_soup.find('p', class_="tweet-text").text   

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img": featured_img_link,
        "weather": weather_results,
        "equatorial_diameter": equatorial_diameter,
        "polar_diameter":polar_diameter,
        "mass":mass,
        "moons":moons,
        "orbit_distance":orbit_distance,
        "orbit_period":orbit_period,
        "surface_temperature":surface_temperature,
        "first_record":first_record,
        "recorded_by":recorded_by
    }
 

     # Close the browser after scraping
    browser.quit()
# add code for jpg here
    return mars_data

#print(scrape())