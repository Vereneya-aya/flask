import os
import zipfile
from PIL import Image, ImageFilter
import smtplib
import json
from email.message import EmailMessage
from celery_app import celery

UPLOAD_FOLDER = 'static/uploads'
ARCHIVE_FOLDER = 'static/archives'
SUBSCRIBERS_FILE = 'subscribers.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

@celery.task
def blur_image(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img = Image.open(filepath)
    blurred = img.filter(ImageFilter.GaussianBlur(10))
    blurred.save(filepath)
    return filename

@celery.task
def send_archive(email, filenames):
    archive_path = os.path.join(ARCHIVE_FOLDER, f'{email}_images.zip')
    with zipfile.ZipFile(archive_path, 'w') as archive:
        for filename in filenames:
            archive.write(os.path.join(UPLOAD_FOLDER, filename), arcname=filename)

    # Теперь отправляем письмо
    send_email(
        to=email,
        subject='Ваши обработанные изображения',
        content='Смотрите вложение!',
        attachments=[archive_path]
    )

def send_email(to, subject, content, attachments=[]):
    # Настройка для SMTP сервера (замени на свою, если нужно)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'  # ❗ придумай как безопасно передать

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to
    msg.set_content(content)

    for path in attachments:
        with open(path, 'rb') as f:
            data = f.read()
            filename = os.path.basename(path)
            msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=filename)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

@celery.task
def send_newsletter():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'r') as f:
            emails = json.load(f)
        for email in emails:
            send_email(
                to=email,
                subject='Еженедельная рассылка!',
                content='Спасибо, что пользуетесь нашим сервисом!'
            )