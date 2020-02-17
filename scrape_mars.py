
# Author: JoTing Wong
# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd


def scrape():
# NASA Mars News page to be scraped
    nasa_mars_url= 'https://mars.nasa.gov/news/'
# Retrieve Nasa Mars News page with the requests module
    nasa_response = requests.get(nasa_mars_url)
# nasa_response

# Create BeautifulSoup object; parse with 'lxml'
    nasa_soup = BeautifulSoup(nasa_response.text, 'lxml')
# print(nasa_soup.prettify())

# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

    news_title = nasa_soup.find('div', class_='content_title').find('a').text
    news_p = nasa_soup.find('div', class_='rollover_description_inner').text

# print(news_title)
# print(news_p)

# JPL Mars Space Images - Featured Image
# Visit the url for JPL Featured Space Image here.
# Use splinter to navigate the site and find the image url for the current Featured Mars Image 

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    jpl_mars_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_mars_url)

# click through the page
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_id('page')

# assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image.

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    image = jpl_soup.find('img')
    featured_image_url = image.get('src')

# featured_image_url

# Mars Weather
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called mars_weather.

    mars_weather_url= 'https://twitter.com/marswxreport?lang=en'

    mars_weather_response = requests.get(mars_weather_url)
# mars_weather_response

    mars_weather_soup = BeautifulSoup(mars_weather_response.text, 'lxml')
# print(mars_weather_soup.prettify())

    mars_weather_tweets = mars_weather_soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

# print(mars_weather_tweets)


# Mars Facts
# Visit the Mars Facts webpage here and use Pandas to scrape the table 
# containing facts about the planet including Diameter,Mass, etc.
# Use Pandas to convert the data to a HTML table string

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_tables = pd.read_html(mars_facts_url)
# mars_facts_tables

# type(mars_facts_tables)

# put the table in the data frame
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['description','value']
    mars_facts_df.set_index('description',inplace=True)
# mars_facts_df.head()

# convert data frame into html
    mars_facts_html_table = mars_facts_df.to_html()
# mars_facts_html_table

# drop line break \n
    mars_facts_html_table.replace('\n', '')

# Mars Hemispheres
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, 
# and the Hemisphere title containing the hemisphere name. 
# Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. 
# This list will contain one dictionary for each hemisphere.

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_hemispheres_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    hemisphere_image_urls = []

# find all h3 tag
    link_cnt = browser.find_by_tag('h3')

# loop through all h3 tag 
    for item in range(len(link_cnt)):
        mars_hemispheres = {}
    
     # click on each h3 item
        browser.find_by_tag('h3')[item].click()
    
    # Get Mars Hemispheres Title
        mars_hemispheres["title"] = browser.find_by_tag("h2.title").text

    # Find Sample Image Tag & get url
        sample = browser.find_link_by_text("Sample").first
        mars_hemispheres["img_url"] = sample["href"]
    
    # Append Mars Hemispheres to List
        hemisphere_image_urls.append(mars_hemispheres)
    
    # Navigate Backwards
        browser.back()
    
    # hemisphere_image_urls   
    mars_data={
            'New_Title': news_title,
            'News_Paragraph': news_p,
            'Feature_Image': featured_image_url,
            'Mars_Weather': mars_weather_tweets,
            'Mars_Facts': mars_facts_html_table,
            'Mars_Hemisphere': hemisphere_image_urls
        }

    return mars_data
