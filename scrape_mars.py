from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver


def scrape():


    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    datascrape={}
    title = soup.find('div',class_='content_title').text
    parag = soup.find('div',class_='article_teaser_body').text
    datascrape['data1'] = title
    datascrape['data2'] = parag


    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    img_url = soup.find('img', class_='thumb').get('src')
    featured_img_url = "https://jpl.nasa.gov"+img_url
    datascrape['image'] = featured_img_url


    url = 'https://twitter.com/marswxreport?lang=en'
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    mars_weather = soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[1]
    mars_weather = mars_weather.get_text()
    datascrape['weather'] = mars_weather


    facturl = 'https://space-facts.com/mars/'
    factdf = pd.read_html(facturl)[0]
    factdf = factdf.rename(columns={'Mars - Earth Comparison':'Mars Planet Profile', 'Mars':''})
    factdf = factdf.set_index('Mars Planet Profile', drop=True)
    factdf = factdf.drop(columns='Earth')
    factdf
    table = factdf.to_html(classes = 'table table-striped')
    datascrape['table'] = table





    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    mars_hemi = []
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemi.append({"title": title, "img_url": image_url})
    datascrape['hemispheres']=mars_hemi
    return datascrape





