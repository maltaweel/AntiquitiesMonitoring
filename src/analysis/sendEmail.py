'''
Created on Feb 17, 2020

@author: mark
'''
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import os

'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

def send_mail(send_from,send_to,subject,text,server,port,username='',password='',isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    filename=os.path.join(filenameToOutput(),'output','scotlandFinds.csv')
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filename, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="scrapedOutput.csv"')
    msg.attach(part)

    #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
    #SSL connection only working on Python 3+
    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    
    '''
Method to run the module and launch the analysis
'''                    
def run():
    
    send_mail('antiquitiies.scotland@gmail.com','maltaweel@yahoo.com','This is it','This is the text','smtp.gmail.com',587,'antiquitiies.scotland','prath4a$')
    print("Finished")
   
if __name__ == '__main__':
    run()
    
