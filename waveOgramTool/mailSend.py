import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import os
import json
from loguru import logger

load_dotenv()


smtpUser = os.getenv('SMTP_USER')
smtpPassword = os.getenv('SMTP_PASSWORD')
subject_dic={
    'register':'🎉 Welcome to waveOgram!  Your Subscription is Confirmed 🎉'
}
body_dic={
    'register': 'Hi ,\n We are thrilled to welcome you to waveOgram! Your subscription is now active, and you are ready to explore all the fantastic features we have to offer.'
}

def sendEmail(recipient,subject,body):
    sender = smtpUser
    recipient = recipient
    subject = subject_dic[subject]
    body = body_dic[body]

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  
            server.login(smtpUser, smtpPassword)  
            server.send_message(msg) 
            logger.info("email send successfully")
            return {'message':'success','statusCode':200}
    except Exception as e:
        logger.info(f'Failed to send email: {e}')
        return {'message':'failure','statusCode':400}
    
