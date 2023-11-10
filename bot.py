#-----------------------------------------------------------------------------------------------------------------------------
# oddsBot - version 0.0
# This bot automates bettor NBA picks with reference to thescore.com.
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
# Imports / Packages / Libraries
#   
#  - python-telegram-bot package [https://docs.python-telegram-bot.org/en]
#-----------------------------------------------------------------------------------------------------------------------------
from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, filters, MessageHandler

# from teams_scraper import scrape_T

#-----------------------------------------------------------------------------------------------------------------------------
# BotFather API token and Username
#-----------------------------------------------------------------------------------------------------------------------------
TOKEN: Final = '6867401223:AAGLE6Amnfo0hWD7ksmJAuya1UXtBDEGMpY'
BOT_USERNAME: Final = '@odds_v0_bot'

#-----------------------------------------------------------------------------------------------------------------------------
# Commands
#-----------------------------------------------------------------------------------------------------------------------------


# This web scraper takes NBA match data from thescore.com
# data is as follows:
# - home/away team
# - over and under
# - against the spread
# - match time

# import statements
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from datetime import date, timedelta


# from tabulate import tabulate
# This Python Script is a Web Scraper that makes use of the BeautifulSoup library
# to display various information about fake news articles from "akoy-pilipino.blogspot.com".
def Scrape():
    options = webdriver.ChromeOptions()
    options.headless = True

    # URL of the website you want to scrape
    # path = 'https://www.cbssports.com/nba/expert-picks/20231103/'
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    next = date.today() + timedelta(1)
    print(next)
    path = f'https://www.thescore.com/nba/events/date/{next}'

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
    ats = driver.find_elements(By.CLASS_NAME, 'EventCard__scoreColumn--2JZbq')

    teamList = []
    scoreList = []

    for team in teams:
        heading = team.find_element(By.TAG_NAME, 'div').text
        teamList.append(heading)
        print(heading)

    for x in ats:
        num = x.find_element(By.TAG_NAME, 'div').text
        scoreList.append(num)
        print(num)

    return teamList,scoreList

# Store data
# - teams -> team name ACRONYMS
# - score -> against the spread, over & under
teams, score = Scrape()

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Picks 🏀", callback_data="1"),
        ],
        [
            InlineKeyboardButton("View Weekly P&L 💰", callback_data="2")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hello! I am OddsBot, how may I help you?', reply_markup=reply_markup)

# Bet command
async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Choose Your Team ⛹️", callback_data="3"), # scrape teams, O&U, Against the Spread
        ],
        [
            InlineKeyboardButton("Pick Again 💸", callback_data="4")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    out = ""
    for i in range(0, len(teams), 2):
        out += f'{teams[i][0:3]}@{teams[i + 1][0:3]} {score[i]}, {score[i + 1]}\n'
    await update.callback_query.edit_message_text(out,reply_markup=reply_markup) 

# Profit and Loss command
async def pnl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("View P&L 📈", callback_data="5"), 
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="Here is your P&L page",reply_markup=reply_markup) 
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help')
    
        # place how to use bot here
        
#-----------------------------------------------------------------------------------------------------------------------------
# Python Testing Functions
#-----------------------------------------------------------------------------------------------------------------------------
def hello():
    return "hello world"


#-----------------------------------------------------------------------------------------------------------------------------
# Control Flow
#----------------------------------------------------------------------------------------------------------------------------- 
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.data == "1":
        await query.answer("Place Bets view entered")
        await bet_command(update, context)
        
        # place format for bets
        
        # choose team
        # enter amount
        # record data into spreadsheet
    
    if query.data == "2":
        await query.answer("Profit & Loss view entered")
        await pnl_command(update, context)
        # query spreadsheet for profit, loss, and push records of user given his/her ID
    
    if query.data == "3":
        await query.answer("Choose Your Team view entered")
        await query.edit_message_text("test")
        # choose team
    
    if query.data == "4":
        await query.answer("Bet Again entered")
        await query.edit_message_text("test")
        # bet again
        
    if query.data == "5":
        await query.answer("P&L view entered")
        await query.edit_message_text("test")
        # view profit
           
    await query.answer()

#-----------------------------------------------------------------------------------------------------------------------------
# Bot Response Handler [Telegram Messages]
#-----------------------------------------------------------------------------------------------------------------------------     
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    # bet handler
    # bet confirm
    # show button done betting
    
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'i love odds' in processed:
        return 'I love odds too!'
    
    # if format wrong -> bet again
    
    return 'I do not understand what you wrote...'

# update.message.chat.id - get user id

#-----------------------------------------------------------------------------------------------------------------------------
# Bot Message Handler [Telegram Messages]
#----------------------------------------------------------------------------------------------------------------------------- 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text 
    
    print(f'User [{update.message.from_user.last_name}, {update.message.from_user.first_name}] in [{message_type} message]: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)
    
    # ---------------------
    #     for debugging
    print('Bot:', response)
    # ---------------------
    
    await update.message.reply_text(response)
    
#-----------------------------------------------------------------------------------------------------------------------------
# Bot Error Handler
#----------------------------------------------------------------------------------------------------------------------------- 
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
#-----------------------------------------------------------------------------------------------------------------------------
# Main Function
#----------------------------------------------------------------------------------------------------------------------------- 
if __name__ == '__main__':
    
    # Initiate Bot Start
    print('Starting bot...')
    
    # Bot Builder
    app = Application.builder().token(TOKEN).build()
    
    # Bot Command Handler
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    
    # Bot Control Flow
    app.add_handler(CallbackQueryHandler(button))
    
    # Bot Message Handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Bot Error Handler
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)