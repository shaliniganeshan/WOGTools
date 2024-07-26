from sanic import Sanic
from sanic.response import text
from loguru import logger
from sanic import html,json
import csv ,os 
from mailSend import sendEmail
from threading import Thread
from datetime import datetime

dataCol='./userDetail.csv'
app=Sanic("subcriptionPage")

def send_email_thread(emailId, subject, body):
    mail = sendEmail(emailId, subject, body)
    return mail

def responseText(statusCode, message, emailId):
    if statusCode == 200:
        mail_thread = Thread(target=send_email_thread, args=(emailId, 'register', 'register'))
        mail_thread.start()
        SC = send_email_thread(emailId, 'register', 'register').get('statusCode')
        # SC=sendEmail(emailId,'register','register').get('statusCode')
        emailSent= True if SC ==200 else False
    else:
        emailSent=False

    with open(dataCol,'a',newline='') as file:
        writer = csv.writer(file)
        if os.path.getsize(dataCol)>0:
            writer.writerow([emailId,str(statusCode),message])
        else:
            writer.writerow(["emailID", "statusCode", "message"])
            writer.writerow([emailId,str(statusCode),message])

    output={
        'statusCode':statusCode,
        'message':f'{emailId} registeration {message}',
        'userInput':emailId,
        'emailSent': emailSent,
        'subscription':emailSent
    }
    return output

@app.route('/subscription',methods=['POST'])
async def subcPage(request):
    c_time=datetime.now()
    data=request.json
    logger.info(data)
    emailId=data['emailId']
    if emailId != '':
        if emailId.split('@')[1]=="gmail.com":
            res=responseText(200,'successfull',emailId)
        else:
            res=responseText(400,'failed',emailId)
    else:
        res=responseText(404,'failed',emailId)
    c1_time=datetime.now()
    logger.info(c1_time-c_time)
    return json(res)
