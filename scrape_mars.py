#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import re
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver


# In[46]:


executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html = browser.html
soup = bs(html,'html.parser')


# In[47]:


title = soup.find('div',class_='content_title').text
parag = soup.find('div',class_='article_teaser_body').text
print(f"{title}\n{parag}")


# In[55]:


executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
html = browser.html
soup = bs(html,'html.parser')


# In[63]:


img_url = soup.find('img', class_='thumb').get('src')
featured_img_url = "https://jpl.nasa.gov"+img_url
print(featured_img_url)


# In[68]:


url = 'https://twitter.com/marswxreport?lang=en'
html = requests.get(url)
soup = bs(html.text, 'html.parser')


# In[107]:


mars_weather = soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[1]
mars_weather = mars_weather.get_text()


# In[109]:


print(mars_weather)


# In[119]:


facturl = 'https://space-facts.com/mars/'
factdf = pd.read_html(facturl)[0]
factdf = factdf.rename(columns={'Mars - Earth Comparison':'Mars Planet Profile', 'Mars':''})
factdf = factdf.set_index('Mars Planet Profile', drop=True)
factdf = factdf.drop(columns='Earth')
factdf


# In[120]:


table = factdf.to_html(classes = 'table table-striped')
print(table)


# In[121]:


executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup = bs(html,'html.parser')


# In[135]:


mars_hemi = []


# In[136]:


products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")


# In[145]:


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


# In[146]:


mars_hemi


# In[ ]:




