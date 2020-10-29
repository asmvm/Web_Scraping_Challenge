#!/usr/bin/env python
# coding: utf-8

# Dependencies 
import selenium
from selenium import webdriver
# from splinter import Browser
# from selenium import webdriver
from bs4 import BeautifulSoup as BS
import pandas as pd
from pprint import pprint
from pymongo import MongoClient

def scrape_news():
    # NASA Mars News
    # URL of page to be scraped

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    driver = webdriver.Firefox()
    driver.get(url)

    news_title = driver.find_elements_by_class_name('content_title')

    body = driver.find_element_by_tag_name("body")
    body_html = body.get_attribute("innerHTML")

    soup = BS(body_html,'html.parser')

    news_titles=soup.find_all('div', class_='content_title')
    news_title = news_titles[1].text

    news_p=soup.find('div', class_='article_teaser_body').text
    
    print(f'The title is: {news_title}')
    print(f'Summary: {news_p}')

    news = {
        "title":news_title,
        "summary":news_p
    }

    driver.quit()
    return news
    
def scrape_feat_image():
    ## JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    driver = webdriver.Firefox()
    driver.get(url_2)

    body_2 = driver.find_element_by_tag_name("body")
    body_html_2 = body_2.get_attribute("innerHTML")
    soup_2 = BS(body_html_2,'html.parser')
    # print(soup_2.prettify())

    featured_image = driver.find_element_by_id("full_image")

    featured_image.click()

    featured_image_info = driver.find_element_by_partial_link_text("more info")
    featured_image_info.click()

    full_featured_image = driver.find_elements_by_class_name("main_image")
    full_featured_image

    main_image = []
    for img in full_featured_image:
        main_image.append(img.get_attribute('src'))

    main_image_url = main_image[0]
    image_featured = {"url":main_image_url}

    # feat_img = {"image":main_image_url}
    driver.quit()
    return image_featured

def scrape_mars_table():
    ## Mars Facts
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    mars_facts = tables[0]
    # mars_facts

    mars_facts.columns = ['Features','Data']
    # mars_facts

    html_table = mars_facts.to_html(classes = 'table table-striped')
    # html_table

    # mars_facts.to_html('mars_facts.html', index=False, index_names=False)
    return html_table


def scrape_hemispheres():
    ## Mars Hemispheres
    # URL of page to be scraped
    url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    driver = webdriver.Firefox()
    driver.get(url_3)

    body_3 = driver.find_element_by_tag_name("body")
    body_html_3 = body_3.get_attribute("innerHTML")
    soup_3 = BS(body_html_3,'html.parser')
    # print(soup_3.prettify())


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

    hemisphere_image_urls
    driver.quit()
    return hemisphere_image_urls

def scrape_all():
    mars_dict = {
        'news': scrape_news(),
        'featured_img': scrape_feat_image(),
        'table': scrape_mars_table(),
        'hemis': scrape_hemispheres()
    }
    return mars_dict