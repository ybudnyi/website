from email.mime.text import MIMEText
import smtplib


def send_letter(email, mass, average, users):
    from_email = 'budnyy5@gmail.com'
    from_password = 'Uralviv1987'
    to_email = email

    subject = 'Body mass index'
    if int(mass) > 25:
        message = f'Hi. Body mass index: <strong>{mass}</strong>,  among {users} users.' \
                  f' Your body mass index is <strong>higher</strong> of normal. You should do some exercises. ' \
                  f'Average mass index of our users is: {average}.'
    elif int(mass) < 18:
        message = f'Hi. Body mass index: <strong>{mass}</strong>,  among {users} users.' \
                  f'Your body max index is <strong>lover</strong> of normal. You should eat more meat. ' \
                  f'Average mass index of our users is: {average}'
    else:
        message = f'Hi. Body mass index: <strong>{mass}</strong>,  among {users} users.' \
                  f'Your body max index is <strong>normal</strong>. You are doing great.' \
                  f'Average mass index of our users is: {average}'
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)

