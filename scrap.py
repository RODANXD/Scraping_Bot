from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def append_file(filename, content):
    with open(filename,"a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"\n\n--- Scrape performed at {timestamp} ---\n\n")
        file.write(content)
    

driver = webdriver.Chrome()
query = "mobile"
for i in range(1,5):
    driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}")
    elems = driver.find_elements(By.CLASS_NAME,"_75nlfW")
    print(f"{len(elems)} found")

    for elem in elems:
        content  = elem.text
        filename = "query.txt"
        append_file(filename, content)
        print(f"Content has been appended to '{filename}'")


driver.quit()