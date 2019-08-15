from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject,template,to,**kwargs):
    sender_email = 'njugunadaniel364@gmail.com'

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)

# import os
# import smtplib


# EMAIL_ADDRESS = os.environ.get('MAIL_USERNAME')
# EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()

#     smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

#     subject = 'Setup flask mail?'
#     body = 'How about getting to work in our project.'

#     msg = f'Subject: {subject}\n\n{body}'
#     smtp.sendmail(EMAIL_ADDRESS, "njugunadaniel364@gmail.com", msg) 
