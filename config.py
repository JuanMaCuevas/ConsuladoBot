from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        # proxies
        self.USER_ID = os.environ.get('PROXY_USER_ID')
        self.PASSWORD = os.environ.get('PROXY_PASSWORD')
        self.PROXY_URL = os.environ.get('PROXY_URL')
        # telegram
        self.TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
        self.CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
        # bookit it
        self.BOOKITIT_API = os.environ.get('BOOKITIT_API')
        # navigation
        self.SITE_URL = "https://www.exteriores.gob.es/Consulados/amsterdam/en/ServiciosConsulares/Paginas/inicio.aspx"
        self.CITA_LINK_SELECTOR = f"a[href='https://app.bookitit.com/es/hosteds/widgetdefault/{self.BOOKITIT_API}#services']"
        self.INSCRIPCION_LINK_TEXT = "[K]... INSCRIPCIÓN CONSULAR"
        self.DATE_ELEMENT_SELECTOR = "#idDivBktDatetimeSelectedDate"

        if not self.USER_ID or not self.PASSWORD:
            raise ValueError("Please set the BRD_USER_ID and BRD_PASSWORD environment variables.")
