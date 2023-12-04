import socket
import yaml
from smtp_functions import *
from  pop3_functions import *
from menu import *

from consolemenu import *
from consolemenu.items import *


with open('config.yml', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

BUFFER_SIZE = config['Server']['bufferSize']
SMTP_HOST = config['Server']['SMTPServer']
SMTP_PORT = config['Server']['SMTP']
POP3_HOST = config['Server']['Pop3Server']
POP3_PORT = config['Server']['POP3']
DOMAIN = config['Server']['domain']
# USERNAME = config['Authentication']['username']
# PASSWORD = config['Authentication']['password']

if __name__ == "__main__":
    menu()
