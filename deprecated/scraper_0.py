# This web scraper takes NBA match data from thescore.com
    # data is as follows:
    # - home/away team
    # - over and under 
    # - against the spread
    # - match time

# import statements
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

Selenium
# from tabulate import tabulate
# This Python Script is a Web Scraper that makes use of the BeautifulSoup library
# to display various information about fake news articles from "akoy-pilipino.blogspot.com".


# URL of the website you want to scrape
#path = 'https://www.cbssports.com/nba/expert-picks/20231103/'
driver = webdriver.Chrome()
path = 'https://www.thescore.com/nba/events/date/2023-11-04'
timeout = 3

driver.get(path)
html=driver.page_source

try:
    element_present = EC.presence_of_element_located((By.ID, 'main'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")

# Send a GET request to the website
# response = requests.get(path)
while(1):
    try:
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html, "html.parser")

        # Find the HTML elements that contain the fake news articles

        matches = soup.findAll("div", {"class":"EventCard__teamName--JweK5"})

        #matches = soup.findAll(class_="EventCard__teamName--JweK5")
        # Create empty lists to store the data
        away_teams = []
        times = []
        over_and_under = []
        against_the_spread = []

        # Extract information from each article
        for match in matches:
            # Get the title of the article
            team = match.text.strip()
            # team = soup.find('div', class_ = False, id_ = False).text.strip()
            away_teams.append(team)
            # print(team)
            # Get the publication date of the article
            # time = article.find('div', id='meta-post').text.strip()
            # times.append(time)

            # Get the preview description of the article
            # preview = article.find('div', class_='resumo').text.strip()
            # previews.append(preview)

        # Create a DataFrame to store the data
        df = pd.DataFrame({
            'Away Team': away_teams,
            #'Date Posted': times,
            # 'Description': previews
        })

        # Print the data

        # normal view
        print(df)
        # pretty view
        # print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    except AttributeError:
        print('retrying...')
    else:
        break

