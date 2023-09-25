import requests
from settings import *

class Messenger:
    def __init__(self, telegram=True, whatsapp=True):
        self.tg_token = TG_TOKEN
        self.tg_chat_id = TG_CHAT_ID
        self.wa_phone = WA_CONTACT_ID
        self.wa_token = WA_TOKEN
        self.telegram = telegram
        self.whatsapp = whatsapp

    def _send_telegram_message(self, text):
        url = f'https://api.telegram.org/bot{self.tg_token}/sendMessage'
        payload = {'chat_id': self.tg_chat_id, 'text': text}
        response = requests.post(url, data=payload)
        return response.json()

    def _send_whatsapp_message(self, text):
        url = 'https://api.callmebot.com/whatsapp.php'
        params = { 'phone': self.wa_phone, 'text': text, 'apikey': self.wa_token }
        response = requests.get(url, params=params)
        return response

    def notify(self, text):
        responses = {}
        if self.telegram:
            responses['telegram'] = self._send_telegram_message(text)
        if self.whatsapp:
            responses['whatsapp'] = self._send_whatsapp_message(text)
        return responses
