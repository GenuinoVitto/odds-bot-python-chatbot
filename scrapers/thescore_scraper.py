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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def scrape_T():
    options = webdriver.ChromeOptions()
    options.headless = True

    # URL of the website you want to scrape
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    path = 'https://www.thescore.com/nba/events/date/2023-11-10'


    driver.get(path)
    # print(driver.page_source)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")
        
    teams = driver.find_elements(By.CLASS_NAME, 'EventCard__teamName--JweK5')
    team_names = []
    for team in teams: 
        heading = team.find_element(By.TAG_NAME, 'div').text
        team_names.append(heading)
        # print(heading)

    ats = driver.find_elements(By.CLASS_NAME, 'EventCard__scoreColumn--2JZbq')
    ats_onu = []
    for x in ats:
        num = x.find_element(By.TAG_NAME, 'div').text
        ats_onu.append(num)
        # print(num)
            
    