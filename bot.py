from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, filters, MessageHandler

# BotFather API token and @
TOKEN: Final = '6867401223:AAGLE6Amnfo0hWD7ksmJAuya1UXtBDEGMpY'
BOT_USERNAME: Final = '@odds_v0_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Bet 🏀", callback_data="1"),
        ],
        [
            InlineKeyboardButton("View P&L", callback_data="2")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hello! I am OddsBot, how may I help you?', reply_markup=reply_markup)


async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Choose Your Team", callback_data="1"), # scrape teams, O&U, Against the Spread
        ],
        [
            InlineKeyboardButton("Bet Again", callback_data="2")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="Here are you bets",reply_markup=reply_markup) 

# testing functions
def hello():
    return "hello world"

# Control Flow 
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.data == "1":
        await query.answer("bet")
        await bet_command(update, context)
        # choose team
        # enter amount
        # record data into spreadsheet
    
    if query.data == "2":
        await query.answer("pnl")
        await bet_command(update, context)
        # query spreadsheet for profit, loss, and push records of user given his/her ID
        
    await query.answer()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help')
    
        # place how to use bot here
    
# Bot Text Responses    
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'i love odds' in processed:
        return 'I love odds too!'
    
    return 'I do not understand what you wrote...'

# Handle Message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text 
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)
    
    # for debugging
    print('Bot:', response)
    # ---------------------
    
    await update.message.reply_text(response)
    
# Handle Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
# Main Function
if __name__ == '__main__':
    print('Starting bot...')
    
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    
    # Buttons
    app.add_handler(CallbackQueryHandler(button))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)