from splinter import Browser 
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = { "executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def article_scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    latest_news = {}
    
    try:
        article = soup.find("div", class_="list_text")
        link = article.find("a")
        latest_news['news_title'] = link.get_text()
        latest_news['news_p'] = article.find("div", class_="article_teaser_body").get_text()
        
    
    except:  
        print("Scrape Complete")
    browser.quit()

        
    return latest_news

def image_scrape():
    browser = init_browser()
    shorturl = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    homeurl = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(homeurl)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    try:
        relative_image_path = soup.find('img', class_='headerimage fade-in')["src"]
        featured_img_url = shorturl + relative_image_path
        
    
    except: 
        print("Image Scrape Complete")
    
    browser.quit()

    return featured_img_url

def facts_scrape():
    url = "https://space-facts.com/mars/"
    
    htmlFacts = pd.read_html(url)
    strTable = htmlFacts[0].to_html(header=False, index=False)
    marsFacts = BeautifulSoup(strTable, "html.parser").prettify()    
    
    return print(marsFacts)

def hemisphere_scrape():
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    baseurl = "https://astrogeology.usgs.gov"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    try:

        results = soup.find("div", class_="collapsible results")
        items = results.find_all("div", class_="item")

        hemispere_image_urls = []

        for item in items:
            hemispere = {}

            hemispere['title'] = item.find("h3").get_text()
            link = item.find("a", class_="itemLink")
            href = link["href"]

            hemispere_url = f'{baseurl}{href}'
            browser.visit(hemispere_url)

            browser.click_link_by_text('Sample')
            window = browser.windows[0]
            img_url = window.next.url
            window.close_others()
            browser.back()
            hemispere['img_url']= img_url    

            hemispere_image_urls.append(hemispere)

    
    except: 
        print("Hemisphere Scrape Complete")
    
    browser.quit()

    
    return hemispere_image_urls

def scrape():
    mars_data = {"article": article_scrape(),
                "featImage": image_scrape(),
                "marsFacts": facts_scrape(),
                "hemiData": hemisphere_scrape()
               }
    
    return mars_data