import smtplib
import json
import sys

def main(argv):
    # Set global variables
    global config, server

    # Get Config data
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Mail Settings
    server = smtplib.SMTP(config['smtpServer'])
    server.login(config['email'], config['password'])

    sendMail()

def sendMail():
    # Send Mail
    message = "\nTestwurst"
    server.sendmail(config['email'], config['targetMail'], message)

if __name__ == '__main__':
    main(sys.argv)
