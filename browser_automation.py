from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from settings import *
import logging
import random
import string
import time

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BrowserAutomation:
    def __init__(self,isDebug, proxy_customer=PROXY_CUSTOMER, proxy_password=PROXY_PASSWORD, proxy_server=PROXY_SERVER ):
        session_id = self._generate_session_id()
        proxy_user = f"brd-customer-{proxy_customer}-zone-datacenter_proxy-session-{session_id}"
        proxy = {'server': f'https://{proxy_server}', 'username': proxy_user, 'password': proxy_password }
        random_ua = self._generate_user_agent()            
        
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir='./chrome_cache',
            headless = not isDebug,
            proxy = proxy,
            args=[f'--user-agent={random_ua}']
        )
        self.page = self.context.new_page()

    def navigate_and_fetch_date(self):
        # maec
        self.page.goto(CONSULADO_URL)        
        cita_link = self.page.wait_for_selector(CITA_LINK_SELECTOR)
        cita_link.click()

        # bookitit inscripcion
        inscripcion_link = self.page.wait_for_selector(f"a:visible:text-is('{INSCRIPCION_LINK_TEXT}')", timeout=100000)
        time.sleep(random.uniform(1, 2))
        inscripcion_link.click()

        date_element = self.page.wait_for_selector(DATE_ELEMENT_SELECTOR, timeout=10000)
        return date_element.inner_text()
            
    def _generate_session_id(self,length=8):
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def _generate_user_agent(self):
        try:
            ua = UserAgent()
            return ua.chrome
        except Exception as e:
            logging.error(f"Error generating user agent: {e}")
            return 'default_user_agent'
    
    def pause(self):
        self.page.pause()

    def close(self):
        self.page.close()
        self.context.close()
        self.playwright.stop()
