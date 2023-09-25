import os
from dotenv import load_dotenv

load_dotenv()

# proxies
USER_ID = os.environ.get('PROXY_USER_ID')
PASSWORD = os.environ.get('PROXY_PASSWORD')
PROXY_URL = os.environ.get('PROXY_URL')

# telegram
TG_TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
TG_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# whatsapp
WA_TOKEN = os.environ.get('WHATSAPP_BOT_API_TOKEN')
WA_CONTACT_ID = os.environ.get('WHATSAPP_CONTACT_ID')

# bookit it
BOOKITIT_API = os.environ.get('BOOKITIT_API')

# navigation
SITE_URL = "https://www.exteriores.gob.es/Consulados/amsterdam/en/ServiciosConsulares/Paginas/inicio.aspx"
CITA_LINK_SELECTOR = f"a[href='https://app.bookitit.com/es/hosteds/widgetdefault/{BOOKITIT_API}#services']"
INSCRIPCION_LINK_TEXT = "[K]... INSCRIPCIÓN CONSULAR"
DATE_ELEMENT_SELECTOR = "#idDivBktDatetimeSelectedDate"

if not USER_ID or not PASSWORD:
    raise ValueError("Please set the PROXY_USER_ID and PROXY_PASSWORD environment variables.")
