#!/usr/bin/env python3
from selenium import webdriver
import os
from time import sleep
from selenium.webdriver.chrome.options import Options
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def banner():
    print('''
		  ##              ##  =======     ####       ####    ####     =======
		  \ \    ####    / /  #      #  ##    ##    / /\ \  / /\ \    #      #
		   \ \  / /\ \  / /   #======   ##    ##   / /  \ \/ /  \ \   #====== 
		    \ \/ /  \ \/ /    #      #  ##    ##  / /    ####    \ \  #      #
		     ####    ####     =======     ####    ##              ##  =======
		''')

def search_contact(driver,name,time: int):
    print(f'waiting for login for {time} seconds')

    try:
        searchBox = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'))
        )
    except:
        print('Timeout while waiting for search box')
        quit()
    print(f'login successful, searching for \033[3m{name}\033[0m ...')
    searchBox.send_keys(name)

def parse_arguments():
    parser = argparse.ArgumentParser(description='WhatsApp Bomber')
    parser.add_argument('-n', '--name', help='Name of the contact or group', required=True)
    parser.add_argument('-m', '--message', help='Message to be sent', required=True)
    parser.add_argument('-c', '--count', help='Number of messages to be sent', required=True)
    parser.add_argument('--head', help='Run with open browser window', action='store_true')
    parser.add_argument('-t', '--time', help='Time to wait for login in seconds', required=False, default=20)
    return parser.parse_args()

def main(args):
    options = Options() 
    options.add_argument('--headless')
    if args.head:
        options.arguments.remove("--headless")  

    options.add_argument('--user-data-dir=/home/cederic/programming/python/whatsappweb_scraper/User_Data')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # 2nd change
    driver.get('https://web.whatsapp.com/')

    name, msg, count, time= args.name, args.message, int(args.count), int(args.time)
    print(f'Name: {name}, Message: {msg}, Count: {count}')

    search_contact(driver,name,time)

    # sleep(1)
    try:
        chats = WebDriverWait(driver, time).until(
            EC.presence_of_all_elements_located((By.XPATH, f'//span[contains(@title, "{name}")]'))
        )
    except Exception as e:
        print(e)
        print(f'Chat with \033[3m{name}\033[0m not found')
        quit()
    
    if len(chats) > 1:
        print(f'Found {len(chats)} chats that contain \033[3m{name}\033[0m')
        for i,chat in enumerate(chats,1):
            print(f'{i}: {chat.get_attribute("title")}')
        selection = int(input('Select the correct chat by entering the number: '))
        chat = chats[selection-1]
    else:
        chat = chats[0]

    name = chat.get_attribute('title') 
    input(f'Press Enter to send message(s) to {name}:')
    chat.click()

    # The classname of message box may vary.
    msg_box = driver.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    print(f'Sending {count} messages to {name}...')
    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
        button.click()
    sleep(2)
    print('Bombing Complete!!')
    driver.quit()

args = parse_arguments()
banner()
main(args)
