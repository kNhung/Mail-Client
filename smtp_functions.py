import socket


def smtp_valid_reponse (code): 
    code = code[:3]
    code = int(code)
    if (200 <= code < 400) : return 1
    else : 
        print("Error occurred. Quitting...")
        return 0
    

def send_mail(SMTP_HOST, SMTP_PORT, BUFFER_SIZE, DOMAIN, smtp_socket, username):
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

    smtp_socket.connect((SMTP_HOST, SMTP_PORT))
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    # HELO/EHLO
    smtp_socket.sendall(('EHLO testserver.com\r\n' ).encode())
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1    
    # MAIL FROM
    smtp_socket.sendall(('MAIL FROM: ' + username + DOMAIN + '\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1
    # RCPT TO
    smtp_socket.sendall(('RCPT TO: ' + destination_user + DOMAIN + '\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    # DATA
    smtp_socket.sendall(('DATA\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1
    smtp_socket.sendall((data + '\r\n').encode())
    smtp_socket.sendall(('.\r\n').encode())
    if (smtp_valid_reponse(smtp_socket.recv(BUFFER_SIZE).decode()) == 0) : 
        smtp_socket.sendall(('QUIT\r\n').encode())
        return -1

    smtp_socket.sendall(('QUIT\r\n').encode())
    print("Press Enter to continue.")
    input()
