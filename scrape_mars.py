from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()
    mars_data = {}

    # Mars News
    local_nasa_file = "News_NASA_Mars_Exploration_Program.html"
    nasa_html = open(local_nasa_file, "r").read()
    news_soup = bs(nasa_html, "html.parser")
    results = news_soup.find_all('div', class_="image_and_description_container")
    Title = news_soup.find('div', class_="content_title").text
    Article = news_soup.find('div', class_="article_teaser_body").text
    Article = Article.replace("\n", "")
    mars_data['Title'] = Title
    mars_data['Article'] = Article

    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    carousel = soup.find(class_="carousel_items")
    carousel = soup.find(class_="carousel_item")
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    mars_data['FeaturedImage'] = featured_image_url

    # MARS WEATHER
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find(class_='tweet-text').get_text()
    # mars_weather = soup.find(class_='tweet-text').get_text()
    mars_data['MarsWeather'] = mars_weather

    # Mars Facts
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')

    results = pd.read_html(facts_url)
    df = results[0]
    df.set_index(0, inplace=True)
    df.index.names = [None]
    df.columns = [' ']
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    mars_data['MarsFacts'] = html_table
    # Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    soup = BeautifulSoup(hemi_html, 'html.parser')
    mars_hemis=[]
    for image in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        time.sleep(5)
        images[image].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['MarsHenispheres'] = mars_hemis

    return mars_data

































