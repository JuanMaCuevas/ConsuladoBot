import requests

def send_message(tg_token, tg_chat_id,wa_phone,wa_token, text):
    url = f'https://api.telegram.org/bot{tg_token}/sendMessage'
    payload = {'chat_id': tg_chat_id, 'text': text}
    response = requests.post(url, data=payload)
    telegram_response = response.json()


    url = 'https://api.callmebot.com/whatsapp.php'
    params = {
        'phone': wa_phone,
        'text': text,
        'apikey':wa_token
    }

    whatsapp_response = requests.get(url, params=params)

    return telegram_response,whatsapp_response
