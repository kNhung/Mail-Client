import socket

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 7500
POP3_HOST = '127.0.0.1'
POP3_PORT = 8500

USERNAME = 'npkn'
PASSWORD = 'hihihihi'
DOMAIN = '@gmail.com'


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
    # Whenever u want to send your mail using SMTP, u have to send the following commands:
    # HELO / EHLO
    # MAIL FROM - includes a sender mailbox
    # RCPT TO - includes a destination mailbox
    # DATA - mail data
    # QUIT
    # After each command, u have to check the Code response by the server (using valid_response func)

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
    smtp_socket.sendall(('MAIL FROM: ' + USERNAME + DOMAIN + '\r\n').encode())
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
    


def receive_mail():
    # Whenever u want to send your mail using SMTP, u have to send the following commands:
    # USER
    # PASS
    # STAT
    # LIST
    # RETR
    print("Opening the first message:")

    pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    pop3_socket.connect((POP3_HOST, POP3_PORT))
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('USER ' + USERNAME + DOMAIN + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(1024).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('PASS ' + PASSWORD + '\r\n').encode())
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
    pop3_socket.sendall(('QUIT\r\n').encode())



send_mail()
receive_mail()
