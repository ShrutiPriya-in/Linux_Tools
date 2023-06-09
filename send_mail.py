import os
import smtplib

emailAddress = os.environ.get('GMAIL_UNAME')
emailPassword = os.environ.get('GMAIL_PASS') 
print(emailPassword)


with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo() 
    smtp.starttls()
    smtp.ehlo()

    smtp.login(emailAddress, emailPassword)

    subject = 'Changes detected'
    body = 'test body matter'
    msg = f'Subject: {subject}\n\n{body}'

    # smtp.sendmail(SENDER, RECEIVER, EMAIL_MSG)
    smtp.sendmail(emailAddress,'shrutipriyain1@gmail.com',msg)

print("code completed") 