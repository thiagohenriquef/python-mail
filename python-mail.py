import smtplib
import os
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MY_ADDRESS = os.environ.get('MY_ADDRESS')
PASSWORD = os.environ.get('EMAIL_PASSWORD')
TITLE_EMAIL = os.environ.get('TITLE_EMAIL')

def find_contacts(filename):    
    countries = []
    embassies = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            countries.append(a_contact.split(';')[0])
            embassies.append(a_contact.split(';')[1])
            emails.append(a_contact.split(';')[2])
    return countries, embassies, emails

def find_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    countries, embassies, emails = find_contacts('adresses.txt')
    message_template = find_template('email-content.txt')

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    for country, embassy, email in zip(countries, embassies, emails):
        msg = MIMEMultipart()
        message = message_template.substitute(EMBASSY_NAME=embassy.title(), COUNTRY_NAME=country.title())

        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']=TITLE_EMAIL.format(country=country)
        
        print(message)

        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg
        
    s.quit()
    
if __name__ == '__main__':
    main()