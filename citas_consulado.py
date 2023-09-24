from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from dotenv import load_dotenv
from datetime import datetime
import dateparser
import logging
import requests
import sqlite3
import random
import string
import time
import os
from database import Database
from messenger import send_telegram_message
from browser_automation import setup_browser, navigate_and_fetch_date


logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




DEBUG = True
# DEBUG = False
load_dotenv()
#proxies
USER_ID = os.environ.get('PROXY_USER_ID')
PASSWORD = os.environ.get('PROXY_PASSWORD')
PROXY_URL = os.environ.get('PROXY_URL')
#telegram
TOKEN =  os.environ.get('TELEGRAM_BOT_API_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
# bookit it
BOOKITIT_API = os.environ.get('BOOKITIT_API')

# navigation
SITE_URL = "https://www.exteriores.gob.es/Consulados/amsterdam/en/ServiciosConsulares/Paginas/inicio.aspx"
CITA_LINK_SELECTOR = f"a[href='https://app.bookitit.com/es/hosteds/widgetdefault/{BOOKITIT_API}#services']"
INSCRIPCION_LINK_TEXT = "[K]... INSCRIPCIÓN CONSULAR"
DATE_ELEMENT_SELECTOR = "#idDivBktDatetimeSelectedDate"

if not USER_ID or not PASSWORD:
    raise ValueError("Please set the BRD_USER_ID and BRD_PASSWORD environment variables.")


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
    if last_entry is None or last_entry[2] != new_appointment_date:
        send_telegram_message(f'Próxima cita: {date_text}')
    db.insert_data(new_appointment_date, new_server_response_time)


def main():
    db = Database()
    with sync_playwright() as p:
        context = setup_browser(p, USER_ID, PASSWORD, PROXY_URL, DEBUG)
        page = context.new_page()
        start_time = time.time()

        try:
            date_text = navigate_and_fetch_date(page, SITE_URL, CITA_LINK_SELECTOR, INSCRIPCION_LINK_TEXT, DATE_ELEMENT_SELECTOR)
            handle_new_data(db,date_text, start_time)
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
