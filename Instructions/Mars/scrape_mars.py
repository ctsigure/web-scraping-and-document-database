from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():

    url1 = "https://mars.nasa.gov/news/8364/martian-skies-clearing-over-opportunity-rover/"
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3 = "https://twitter.com/marswxreport?lang=en"
    url4 = "https://space-facts.com/mars/"
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    listings = {}
    browser = init_browser()
    

    
    browser.visit(url1)
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.title.text.strip()
    news_p1 = soup.body.find_all('p')[1].text
    news_p2 = soup.body.find_all('p')[2].text
    news_p3 = soup.body.find_all('p')[3].text

    s = "\n"
    cons =(news_p1,news_p2,news_p3)
    news_p = s.join(cons)

    listings["news_title"] = news_title
    listings["news_p"] = news_p


    browser.visit(url2)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    listings["featured_image_url"] = featured_image_url


    browser.visit(url3)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break
    listings["mars_weather"] = mars_weather



    df = pd.read_html(url4, attrs = {'id': 'tablepress-mars'})[0]
    df = df.rename(columns={0:"Index",1:"Value"})
    df = df.set_index("Index")
    del df.index.name
    html_table = df.to_html(justify='left')
    listings["mars_facts"] = html_table
    


    browser.visit(url5)
    cerberus = browser.find_by_tag('h3')[0].text
    schiaparelli = browser.find_by_tag('h3')[1].text
    syrtis = browser.find_by_tag('h3')[2].text
    valles = browser.find_by_tag('h3')[3].text

    browser.find_by_css('.thumb')[0].click()
    cerberus_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    schiaparelli_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    syrtis_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    valles_img = browser.find_by_text('Sample')['href']

    hemisphere_image_urls = [
    {'title': cerberus, 'img_url': cerberus_img},
    {'title': schiaparelli, 'img_url': schiaparelli_img},
    {'title': syrtis, 'img_url': syrtis_img},
    {'title': valles, 'img_url': valles_img}
    ]
    listings["hemisphere_image_urls"] = hemisphere_image_urls
    
    return listings

