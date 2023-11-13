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

# from tabulate import tabulate
# This Python Script is a Web Scraper that makes use of the BeautifulSoup library
# to display various information about fake news articles from "akoy-pilipino.blogspot.com".

options = webdriver.ChromeOptions()
options.headless = True

# URL of the website you want to scrape
#path = 'https://www.cbssports.com/nba/expert-picks/20231103/'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
path = 'https://www.thescore.com/nba/events/date/2023-11-10'

def scrape_S():
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
    ats_onu = driver.find_elements(By.CLASS_NAME, 'EventCard__scoreColumn--2JZbq')

    team_names = []
    ats_list = []

    # Extract team names and ATS data
    for team, ats in zip(teams, ats_onu):
        team_name = team.find_element(By.TAG_NAME, 'div').text
        ats_value = ats.find_element(By.TAG_NAME, 'div').text
        team_names.append(team_name)
        ats_list.append(ats_value)

    # Calculate the number of games (assuming each game is represented by two teams)
    num_games = len(team_names) // 2

    # Format the data into lines
    formatted_lines = []
    for i in range(num_games):
        home_team = team_names[i * 2]
        away_team = team_names[i * 2 + 1]
        spread = ats_list[i * 2]
        over_under = ats_list[i * 2 + 1]
        
        formatted_line = f"{home_team}@{away_team} {spread} {over_under}"
        formatted_lines.append(formatted_line)

    # Join the formatted lines into a single string with newlines
    formatted_data = '\n'.join(formatted_lines)

    # Print or use the formatted data
    print(formatted_data)