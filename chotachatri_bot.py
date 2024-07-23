from telegram import Update
from selenium import webdriver
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime


TOKEN = '7302240229:AAE2tPS8W7A4ZFF_zIUQeclHN1-MlJXbZuY'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('what you want to in amazon type a keyword')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message.lower().startswith("scrape "):
        query = user_message[7:]
        response, filename = await flipkart_scrap(query)
        if response:
            await update.message.reply_text(response)
        else:
            await update.message.reply_document(open(filename, 'rb'))
    else:
        await update.message.reply_text(f'use scrap + {user_message}')

async def flipkart_scrap(query: str) -> tuple:
    driver = webdriver.Chrome()
    filename = "query2.txt"
    try:
        for i in range(1,2):
            driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}")
            elems = driver.find_elements(By.CLASS_NAME,"_75nlfW")
            print(f"{len(elems)} found")

            for elem in elems:
                content  = elem.text
                await append_file(filename, content)
                print(f"Content has been appended to '{filename}'")
                
        return None, filename 
    except Exception as e:
        return f"An error occurred: {str(e)}", None
    finally:
        driver.quit()

    
async def append_file(filename, content):
    with open(filename,"a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"\n\n--- Scrape performed at {timestamp} ---\n\n")
        file.write(content)



    

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
