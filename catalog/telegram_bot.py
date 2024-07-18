import os
import django
import requests
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django_q.tasks import async_task
from catalog.models import Borrowing


TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")
TELEGRAM_WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
TELEGRAM_WEBHOOK_URL = f"{NGROK_TUNNEL_URL}/bot/{NGROK_TUNNEL_URL}"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)


def notify_borrowing_created(borrowing_id):
    borrowing = Borrowing.objects.get(id=borrowing_id)
    books = ', '.join(book.title for book in borrowing.book_id.all())
    message = (f"New borrowing created by {borrowing.user_id.username} on {borrowing.borrow_date} "
               f"for books: {books} ID: {borrowing.id}")
    async_task(send_telegram_message, message)


def notify_borrowing_overdue(borrowing_id):
    borrowing = Borrowing.objects.get(id=borrowing_id)
    message = (f"Borrowing overdue: id: {borrowing.id}, username: {borrowing.user_id.username}, "
               f"expected return {borrowing.expected_return}")
    async_task(send_telegram_message, message)


def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    data = {'url': TELEGRAM_WEBHOOK_URL}
    response = requests.post(url, data=data)
    print(response.text)


set_webhook()