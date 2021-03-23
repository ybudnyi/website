from email.mime.text import MIMEText
import smtplib


def send_letter(email):
    from_email = ''
    from_password = ''
    to_email = email

    subject = ''

    message =''

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)

