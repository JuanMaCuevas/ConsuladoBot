from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from datetime import datetime
import dateparser
import logging
import requests
import sqlite3
import random
import string
import time
import os

from settings import *
from database import Database
from messenger import send_message
from browser_automation import setup_browser, navigate_and_fetch_date


logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


DEBUG = True
# DEBUG = False

def generate_session_id(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_user_agent():
    try:
        ua = UserAgent()
        return ua.chrome
    except Exception as e:
        logging.error(f"Error generating user agent: {e}")
        return 'default_user_agent'


def parse_date(date_text):
    date_obj = dateparser.parse(date_text, languages=['es'])
    return date_obj.strftime('%Y-%m-%d')


def handle_new_data(db,date_text, start_time):
    new_appointment_date = parse_date(date_text)
    new_server_response_time = time.time() - start_time
    last_entry = db.fetch_last_entry()
    notify = last_entry is None or last_entry[2] != new_appointment_date
    db.insert_data(new_appointment_date, new_server_response_time)
    return notify


def main():
    db = Database()
    with sync_playwright() as p:
        context = setup_browser(p, USER_ID, PASSWORD, PROXY_URL, DEBUG)
        page = context.new_page()
        start_time = time.time()

        try:
            date_text = navigate_and_fetch_date(page, SITE_URL, CITA_LINK_SELECTOR, INSCRIPCION_LINK_TEXT, DATE_ELEMENT_SELECTOR)
            if handle_new_data(db,date_text, start_time):
                send_message(TG_TOKEN, TG_CHAT_ID,WA_TOKEN,WA_CONTACT_ID, text)
            handle_new_data
            if DEBUG:
                page.pause()
                time.sleep(1000)

        except Exception as e:  # Replace with specific exception
            logging.error(f"An error occurred: {e}")

        finally:
            page.close()
            context.close()
            db.close()

if __name__ == '__main__':
    main()
