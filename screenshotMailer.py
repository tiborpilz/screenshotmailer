import smtplib
import json
import sys
import io


import pyscreenshot as ImageGrab
from time import sleep
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import multiprocessing

# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen

def main(argv):
    print('Starting Automatic Screencapture')
    # Set global variables
    global config, server

    # Get Config data
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Mail Settings
    server = smtplib.SMTP(config['smtpServer'])

    # Main loop
    while True:
        print(('Sending screenshot to: '
           +config['targetMail']
           +'. Next screenshot in '
           +str(config['delay'])
           +' seconds'))

        sendMail(getScreenshot())
        sleep(config['delay'])

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
    server.login(config['username'], config['password'])

    # Send Mail
    server.sendmail(config['email'], config['targetMail'], message.as_string())

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main(sys.argv)
