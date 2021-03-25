###########################
#import dependencies
###########################
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

###########################################################
#Visit site ('https://mars.nasa.gov/news/') and scrape 
#for title and related paragraph text for the latest  news
###########################################################

# Define scrape function
def scrape():

    #initialize the large dictionary to store all scraped information
    mars_dictionary = []

    # create path and open browser window
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # establish url
    url = 'https://mars.nasa.gov/news/'

    # visit site
    browser.visit(url)

    # grab page html
    nasa_html = browser.html

    # create soup object
    soup = BeautifulSoup(nasa_html,'html.parser')

    # find title for the latest one, which is the one in the first box
    news_title = soup.find_all('div',class_='content_title')
    news_title = news_title[1].text

    # pulling the text from the paragraph
    news_p = soup.find_all('div', class_= 'article_teaser_body')
    news_p = news_p[0].text

    #append the title and paragrapah text to the larger mars_dictionary
    mars_dictionary['current_title'] = news_title
    mars_dictionary['current_p'] = news_p

    #############################################################
    #Visit the site ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    #and scrape for the current featured image (the full size version)
    #############################################################

    # establish url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # visit site
    browser.visit(jpl_url)

    # grab page html
    jpl_html = browser.html

    # create soup object
    soup = BeautifulSoup(jpl_html,'html.parser')

    #Find the image at the top and click 
    target = 'a[class="group  cursor-pointer block"]'
    browser.find_by_tag(target).click()

    # grab page html
    target_html = browser.html

    # create soup object
    soup = BeautifulSoup(target_html,'html.parser')

    image = soup.find_all('a', class_='BaseButton text-contrast-none w-full mb-5 -primary -compact inline-block')
    featured_image_url = image[0]['href']

    #append the featured image url to the larger mars_dictionary
    mars_dictionary['featured_image_url'] = featured_image_url

    #############################################################################
    #Visit the site ('https://space-facts.com/mars/') and scrape the table with 
    #the mars data and convert back to html
    ##############################################################################

    # establish url
    facts_url = 'https://space-facts.com/mars/'

    # visit site
    browser.visit(facts_url)

    #pull the table from the site
    tables =pd.read_html('https://space-facts.com/mars/')
    #pull the specific table for just the Mars data
    mars_tables = tables[0]
    #rename columns
    mars_tables.columns = ['Fact','Value']
    #convert dataframe back to html
    mars_tables_html = mars_tables.to_html

    #append the mars_table to the larger mars_dictionary
    mars_dictionary['mars_tables_html'] =  mars_tables_html

    ################################################################
    # Visit the site ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    #scrape  for the title and image url for each of the hemisphere  and create a list with 
    #a mini dictionary for each hemisphere
    ################################################################

    # establish url
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # visit site
    browser.visit(hemi_url)

    # grab page html
    hemi_html = browser.html

    # create soup object
    soup = BeautifulSoup(hemi_html,'html.parser')

    #Find the all the titles to use for the click function 
    title_list = soup.find_all('div', class_='description')

    hemisphere_image_urls = []
    #loop through the title_list and pull title and imagine url
    for t in title_list:
        title = t.h3.text
        browser.find_by_text(title).click()

        # grab page html
        title_html = browser.html

        # create soup object
        soup = BeautifulSoup(title_html,'html.parser')

        image = soup.find_all('div', class_='downloads')
        image_url = image[0].li.a['href']

        #create mini-dictionary
        mini_dictionary = {'title': title, 'img_url':image_url}
        hemisphere_image_urls.append(mini_dictionary)

        # click back button
        browser.back()

    #quit browser
    browser.quit()

    #append the hemisphere list to the larger mars_dictionary
    mars_dictionary['hemisphere_image_urls'] = hemisphere_image_urls

    #returns the mars_dictionary
    return mars_dictionary