import socket
import client

def smtp_valid_reponse (code): 
    code = code[:3]
    code = int(code)
    if (200 <= code < 400) : return 1
    else : 
        print("Error occurred. Quitting...")
        print("Press Enter to continue.")
        input()
        return 0

def separating_comma(s):
    return s.split(',')

def get_content():
    print("Content:")
    print("(type '-end-' to end content part)")
    content = ""
    while True:
        line = input()
        if(line.lower()) == '-end-': # Nếu người dùng nhập '-end-', kết thúc nhập
            break
        content += line + '\n' # Kết hợp các dòng thành 1 chuỗi duy nhất
    return content.rstrip('\n') # Loại bỏ kí tự xuống dòng cuối cùng nếu có

def send_to (destination_user_to, subject, content) :
    destination_user_to = [item for item in destination_user_to if item != ""]
    n = len(destination_user_to)
    if (n == 0): 
        return -1;
    for i in range (n) :
        smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smtp_socket.connect((client.SMTP_HOST, client.SMTP_PORT))
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # HELO/EHLO
        smtp_socket.sendall(('EHLO testserver.com\r\n' ).encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1    
        # MAIL FROM
        smtp_socket.sendall(('MAIL FROM: ' + client.USERNAME + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # RCPT TO 
        smtp_socket.sendall(('RCPT TO: ' + destination_user_to[i]  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1

        data = "From: " + client.USERNAME  + "\r\nTo: "  + destination_user_to[i]  + "\r\nCC:\r\nBCC:\r\nSubject: " + subject + "\r\nContent: " + content + "\r\n"

        # DATA
        smtp_socket.sendall(('DATA\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall((data + '\r\n').encode())
        smtp_socket.sendall(('.\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall(('QUIT\r\n').encode())

def send_cc(destination_user_cc, subject, content) :
    destination_user_cc = [item for item in destination_user_cc if item != ""]
    n = len(destination_user_cc)
    if (n == 0): 
        return -1;
    for i in range (n) :
        smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smtp_socket.connect((client.SMTP_HOST, client.SMTP_PORT))
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # HELO/EHLO
        smtp_socket.sendall(('EHLO testserver.com\r\n' ).encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1    
        # MAIL FROM
        smtp_socket.sendall(('MAIL FROM: ' + client.USERNAME  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # RCPT TO 
        smtp_socket.sendall(('RCPT TO: ' + destination_user_cc[i]  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1

        data = "From: " + client.USERNAME + "\r\nTo:\r\nCC:" + ",".join(destination_user_cc[i] for i in range(n)) + "\r\nBCC:\r\nSubject:"  + subject + "\r\nContent: " + content + "\r\n"

        # DATA
        smtp_socket.sendall(('DATA\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall((data + '\r\n').encode())
        smtp_socket.sendall(('.\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall(('QUIT\r\n').encode())

def send_bcc(destination_user_bcc, subject, content) :
    destination_user_bcc = [item for item in destination_user_bcc if item != ""]
    n = len(destination_user_bcc)
    if (n == 0): 
        return -1;
    for i in range (n) :
        smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smtp_socket.connect((client.SMTP_HOST, client.SMTP_PORT))
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # HELO/EHLO
        smtp_socket.sendall(('EHLO testserver.com\r\n' ).encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1    
        # MAIL FROM
        smtp_socket.sendall(('MAIL FROM: ' + client.USERNAME  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # RCPT TO 
        smtp_socket.sendall(('RCPT TO: ' + destination_user_bcc[i]  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1

        data = "From: " + client.USERNAME + "\r\nTo:\r\nCC:\r\nBCC:" + destination_user_bcc[i] + "\r\nSubject:"  + subject + "\r\nContent: " + content + "\r\n"

        # DATA
        smtp_socket.sendall(('DATA\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall((data + '\r\n').encode())
        smtp_socket.sendall(('.\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall(('QUIT\r\n').encode())

def send_mail():
    # whenever u want to sent your mail using SMTP, u have to send these following commands:
    # HELO / EHLO
    # MAIL FROM - includes a sender mailbox
    # RCPT TO - includes a destination mailbox
    # DATA - mail data
    # QUIT
    # After each command, u have to check the Code respone by the server (using valid_response func)
    destination_user_to = separating_comma(input("To (seperate by a comma \',\', if none type \'none\'):"))
    destination_user_cc = separating_comma(input("CC (seperate by a comma \',\', if none type \'none\'):"))
    destination_user_bcc = separating_comma(input("BCC (seperate by a comma \',\', if none type \'none\'):"))
    if (destination_user_to[0] == "none" and destination_user_cc[0] == "none" and destination_user_bcc[0] == "none") :
        print("No receiver. Quitting...")
        print("Press Enter to continue.")
        input()
        return -1
    subject = input("Subject: ")
    content = get_content()
    # Manage "To" option
    send_to(destination_user_to, subject, content)
    # Manage "CC" option
    send_cc(destination_user_cc, subject, content)
    # Manage "BCC" option
    send_bcc(destination_user_bcc, subject, content)
