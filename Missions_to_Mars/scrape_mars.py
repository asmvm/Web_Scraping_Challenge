#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies 
import selenium
from selenium import webdriver
# from splinter import Browser
# from selenium import webdriver
from bs4 import BeautifulSoup as BS
import pandas as pd
from pprint import pprint
from pymongo import MongoClient


# In[2]:


## switched to selenium/gecko driver..no longer using chromedriver
# chromedriver='C:/Users/a_mcr/chromedriver_win32/chromedriver'
# driver = webdriver.Chrome(chromedriver)
# driver.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")


# In[3]:


# executable_path = {'executable_path': 'C:/Users/a_mcr/webdrivers/chromedriver_win32/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)


# ### Step 1 - Scraping
# ----------------------

# # NASA Mars News

# In[4]:


# URL of page to be scraped
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


# In[5]:


driver = webdriver.Firefox()
driver.get(url)


# In[7]:


news_title = driver.find_elements_by_class_name('content_title')
# news_title


# In[8]:


body = driver.find_element_by_tag_name("body")
body_html = body.get_attribute("innerHTML")
# body_html
soup = BS(body_html,'html.parser')
# soup


# In[9]:


news_titles=soup.find_all('div', class_='content_title')
news_title = news_titles[1].text
news_title

news_p=soup.find('div', class_='article_teaser_body').text

print(f'The title is: {news_title}')
print(f'Summary: {news_p}')


# In[10]:


driver.quit()


# # JPL Mars Space Images - Featured Image

# In[11]:


# URL of page to be scraped
url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


# In[12]:


driver = webdriver.Firefox()
driver.get(url_2)


# In[13]:


body_2 = driver.find_element_by_tag_name("body")
body_html_2 = body_2.get_attribute("innerHTML")
soup_2 = BS(body_html_2,'html.parser')
# print(soup_2.prettify())


# In[14]:


featured_image = driver.find_element_by_id("full_image")
featured_image


# In[15]:


featured_image.click()


# In[16]:


featured_image_info = driver.find_element_by_link_text("more info")
featured_image_info.click()


# In[17]:


full_featured_image = driver.find_elements_by_class_name("main_image")
full_featured_image


# In[18]:


main_image = []
for img in full_featured_image:
    main_image.append(img.get_attribute('src'))

main_image_url = main_image[0]
main_image_url


# In[19]:


driver.quit()


# # Mars Facts

# In[20]:


# URL of page to be scraped
url = 'https://space-facts.com/mars/'


# In[21]:


tables = pd.read_html(url)
mars_facts = tables[0]
# mars_facts


# In[22]:


mars_facts.columns = ['Features','Data']
# mars_facts


# In[23]:


html_table = mars_facts.to_html(classes = 'table table-striped')


# In[24]:


html_table


# In[25]:


pwd


# In[26]:


mars_facts.to_html('mars_facts.html', index=False, index_names=False)


# # Mars Hemispheres

# In[27]:


# URL of page to be scraped
url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[28]:


driver = webdriver.Firefox()
driver.get(url_3)


# In[33]:


body_3 = driver.find_element_by_tag_name("body")
body_html_3 = body_3.get_attribute("innerHTML")
soup_3 = BS(body_html_3,'html.parser')
# print(soup_3.prettify())


# In[34]:


# testing out a specific header to grab
# driver.find_elements_by_tag_name('h3')[3].click()


# In[35]:


# loop through all the hemisphere header tags to create dictionary of /n
# hemisphere data, iterate through each tag with selenium

hemisphere_image_urls = []
hemisphere_links = driver.find_elements_by_tag_name('h3')

for link in range(len(hemisphere_links)):
    hemisphere_data = {}
    
#     starting point
    hemisphere_links = driver.find_elements_by_tag_name('h3')
    
#     print(hemisphere_links[link].text)   
    title = hemisphere_links[link].text
    hemisphere_data['title'] = title

#     navigate to the h3 tag and get href attribute for the sample image
#     append the href url to the dictionary
    hemisphere_links[link].click()
    sample = driver.find_element_by_link_text('Sample').get_attribute('href')
    hemisphere_data['img_url'] = sample

#     append the image title and img url to the empty list
    hemisphere_image_urls.append(hemisphere_data)
    
#     return to previous page to iterate through remaining images
    driver.back()


# In[36]:


hemisphere_image_urls


# In[37]:


driver.quit()


# ## Step 2 - MongoDB and Flask Application

# # MongoDB

# In[ ]:


# client = MongoClient("mongodb://localhost:27017")
# db = client["Mars"]


# In[ ]:


# mars_data = {
#     'title':news_title,
#     'paragraph': news_p,
#     'image': main_image_url,
#     'table': mars_facts,
# }


# In[ ]:


# mars_collection = db.mars_scrape
# mars_collection.insert_one(mars_data)

