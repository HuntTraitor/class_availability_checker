import requests
from bs4 import BeautifulSoup
import time
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

def send_notification():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = 'Class Available!'
    body = 'The class you are monitoring now has an open spot.'
    message = f'Subject: {subject}\n\n{body}'

    server.sendmail(sender_email, receiver_email, message)

    server.quit()

def check_availability():
    url = "https://pisa.ucsc.edu/class_search/index.php?action=detail&class_data=YToyOntzOjU6IjpTVFJNIjtzOjQ6IjIyNDAiO3M6MTA6IjpDTEFTU19OQlIiO3M6NToiMzExMzkiO30%253D"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    class_status_wrappers = soup.find_all('dl', {'class':'dl-horizontal'})

    for class_status_wrapper in class_status_wrappers:
        dt_tag = class_status_wrapper.find('dt', string='Available Seats')

        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd')
            if dd_tag:
                return dd_tag.text.strip()
                
while True:
    seats = check_availability()
    seats = int(seats)

    if seats != 0:
        send_notification()
        print("notification sent!")

    print(seats)
    time.sleep(30)
    