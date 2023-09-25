from browser_automation import BrowserAutomation
from messenger import Messenger
from database import Database
import dateparser
import time
import logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(debug = False):
    db = Database('appointments.db')
    browser = BrowserAutomation(debug)
    try:
        chatBot = Messenger(telegram=True, whatsapp=True)
        
        init_time = time.time()
        raw_date = browser.navigate_and_fetch_date() # magic happens here
        response_time = time.time() - init_time
        
        iso_date = transform_raw_date_format(raw_date)
        if db.upcoming_appointment_changed(iso_date):
            chatBot.notify(raw_date)
        db.insert_data(iso_date, response_time)
        
        if debug:
            browser.pause()
            time.sleep(1000)

    except Exception as e: 
        logging.error(f"An error occurred: {e}")

    finally:
        db.close()
        browser.close()

def transform_raw_date_format(date_text):
    date_obj = dateparser.parse(date_text, languages=['es'])
    if date_obj is not None:
        return date_obj.strftime('%Y-%m-%d')
    else:
        logging.error(f"Unable to parse date: {date_text}")
        return None


if __name__ == '__main__':
    main()
