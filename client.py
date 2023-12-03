import socket

from consolemenu import *
from consolemenu.items import *

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 7500
POP3_HOST = '127.0.0.1'
POP3_PORT = 8500

DOMAIN = '@gmail.com'

username = 'npkn'
password = 'hihihihi'

def smtp_valid_reponse (code): 
    code = code[:3]
    code = int(code)
    if (200 <= code < 400) : return 1
    else : 
        print("Error occurred. Quitting...")
        return 0

def pop3_valid_reponse(code) :
    code = code[:3]
    if (code == "+OK") : return 1
    else :
        print("Error occurred. Quiting...")
        return 0


def send_mail():
    # whenever u want to sent your mail using SMTP, u have to send these following commands:
    # HELO / EHLO
    # MAIL FROM - includes a sender mailbox
    # RCPT TO - includes a destination mailbox
    # DATA - mail data
    # QUIT
    # After each command, u have to check the Code respone by the server (using valid_response func)

    print("Enter destination mail: ")
    destination_user = input()
    print("Enter mail content: ")
    data = input()

    smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    smtp_socket.connect((SMTP_HOST, SMTP_PORT))
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    # HELO/EHLO
    smtp_socket.sendall(('EHLO testserver.com\r\n' ).encode())
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1    
    # MAIL FROM
    smtp_socket.sendall(('MAIL FROM: ' + username + DOMAIN + '\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1
    # RCPT TO
    smtp_socket.sendall(('RCPT TO: ' + destination_user + DOMAIN + '\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    # DATA
    smtp_socket.sendall(('DATA\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1
    smtp_socket.sendall((data + '\r\n').encode())
    smtp_socket.sendall(('.\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(1024).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    smtp_socket.sendall(('QUIT\r\n').encode())
    print("Press Enter to continue.")
    input()
    


def receive_mail():
    # whenever u want to sent your mail using SMTP, u have to send these following commands:
    # USER
    # PASS
    # STAT
    # LIST
    # RETR
    print("Opening the first unread message:")

    pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    pop3_socket.connect((POP3_HOST, POP3_PORT))
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('USER ' + username + DOMAIN + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('PASS ' + password + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('STAT' + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1

    pop3_socket.sendall(('LIST' + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1

    # Return the content of the first mail
    pop3_socket.sendall(b'RETR 1\r\n')
    message = pop3_socket.recv(1024).decode()
    if (pop3_valid_reponse(message) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    print(message)
    pop3_socket.sendall(b'DELE 1\r\n')
    message = pop3_socket.recv(1024).decode()
    if (pop3_valid_reponse(message) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    pop3_socket.sendall(('QUIT\r\n').encode())
    print("Press Enter to continue.")
    input()


def login():
    global username
    print("Please enter your username:")
    username = input()


def menu():
    # Create the menu
    menu = ConsoleMenu("SIMPLE MAIL CLIENT", "Group 12!")
    login_option = FunctionItem("Choose Username", login)
    send_option = FunctionItem("Send Mail Using SMTP", send_mail)
    receive_option = FunctionItem("Receive Mail Using Pop3", receive_mail)
    menu.append_item(login_option)
    menu.append_item(send_option)
    menu.append_item(receive_option)
    menu.show()

menu()
