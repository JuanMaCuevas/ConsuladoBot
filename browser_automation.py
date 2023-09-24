# browser_automation.py

from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import logging
import random
import string
import time

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


def setup_browser(playwright, USER_ID, PASSWORD, PROXY_URL, DEBUG):
    random_ua = generate_user_agent()
    session_id = generate_session_id()
    
    proxy_auth = f"brd-customer-{USER_ID}-zone-datacenter_proxy-session-{session_id}:{PASSWORD}"

    context = playwright.chromium.launch_persistent_context(
        user_data_dir='./chrome_cache',
        headless=not DEBUG,
        proxy={
            'server': f'http://{PROXY_URL}',
            'username': proxy_auth.split(":")[0],
            'password': PASSWORD
        },
        args=[f'--user-agent={random_ua}']
    )
    return context

def navigate_and_fetch_date(page, SITE_URL, CITA_LINK_SELECTOR, INSCRIPCION_LINK_TEXT, DATE_ELEMENT_SELECTOR):
    navigate_to_site(page, SITE_URL)
    click_cita_link(page, CITA_LINK_SELECTOR)
    click_inscripcion_link(page, INSCRIPCION_LINK_TEXT)
    return fetch_date_text(page, DATE_ELEMENT_SELECTOR)

def navigate_to_site(page, SITE_URL):
    page.goto(SITE_URL)

def click_cita_link(page, CITA_LINK_SELECTOR):
    cita_link = page.wait_for_selector(CITA_LINK_SELECTOR)
    cita_link.click()

def click_inscripcion_link(page, INSCRIPCION_LINK_TEXT):
    inscripcion_link = page.wait_for_selector(f"a:visible:text-is('{INSCRIPCION_LINK_TEXT}')", timeout=20000)
    time.sleep(random.uniform(1, 2))
    inscripcion_link.click()

def fetch_date_text(page, DATE_ELEMENT_SELECTOR):
    date_element = page.wait_for_selector(DATE_ELEMENT_SELECTOR, timeout=10000)
    return date_element.inner_text()
