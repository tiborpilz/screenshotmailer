import smtplib
import json
import sys
import io
import pyscreenshot as ImageGrab
from time import sleep
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def main(argv):
    # Set global variables
    global config, server

    # Get Config data
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Mail Settings
    server = smtplib.SMTP(config['smtpServer'])

    # Main loop
    while True:
        sendMail(getScreenshot())
        sleep(config['delay'])

        print(('Sending screenshot to: '
               +config['targetMail']
               +'. Next screenshot in '
               +str(config['delay'])
               +' seconds'))

def getScreenshot():
    imageBuffer = io.BytesIO()
    image = ImageGrab.grab()
    image.save(imageBuffer, format="PNG")
    imageValue = imageBuffer.getvalue()
    imageBuffer.close()
    return imageValue

def sendMail(imgBuffer):
    # Define message
    message = MIMEMultipart()
    message['Subject'] = 'Automatic Screenshot'
    message['From'] = config['email']
    message['To'] = config['targetMail']

    text = MIMEText("Screenshot done")
    message.attach(text)
    image = MIMEImage(imgBuffer, name='screenshot.png')
    message.attach(image)

    # Log in yadda yadda
    server.login(config['email'], config['password'])

    # Send Mail
    server.sendmail(config['email'], config['targetMail'], message.as_string())

if __name__ == '__main__':
    main(sys.argv)
