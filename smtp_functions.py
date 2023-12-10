import socket
import client
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

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

def to_cc_option (send_to, subject, content, files) :
    send_to = [item for item in send_to if item != ""]
    n = len(send_to)
    if (n == 0): 
        return -1
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
        smtp_socket.sendall(('RCPT TO: ' + send_to[i]  + '\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1

        # data = "From: " + client.USERNAME + "\r\nTo:" + ",".join(destination_user_to[i] for i in range(n)) + "\r\nCC:" + ",".join(destination_user_cc[i] for i in range(n)) + "\r\nBCC:\r\nSubject:"  + subject + "\r\nContent: " + content + "\r\nDate:" + date_and_time()
        data = create_message(client.USERNAME, send_to, subject, content, files)
        # DATA
        smtp_socket.sendall(('DATA\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        # smtp_socket.sendall((data + '\r\n').encode())
        smtp_socket.sendall((data + '\r\n').encode())

        smtp_socket.sendall(('.\r\n').encode())
        if (smtp_valid_reponse(smtp_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            smtp_socket.sendall(('QUIT\r\n').encode())
            return -1
        smtp_socket.sendall(('QUIT\r\n').encode())

def bcc_option(destination_user_bcc, subject, content, files) :
    destination_user_bcc = [item for item in destination_user_bcc if item != ""]
    n = len(destination_user_bcc)
    if (n == 0): 
        return -1
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

        # data = "From: " + client.USERNAME + "\r\nTo:\r\nCC:\r\nBCC:" + destination_user_bcc[i] + "\r\nSubject:"  + subject + "\r\nContent: " + content + "\r\nDate:" 
        data = create_message(client.USERNAME, [destination_user_bcc[i]], subject, content, files)
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
    destination_user_to = separating_comma(input("To (seperate by a comma \',\', or leave blank to finish):"))
    destination_user_cc = separating_comma(input("CC (seperate by a comma \',\', or leave blank to finish):"))
    destination_user_bcc = separating_comma(input("BCC (seperate by a comma \',\', or leave blank to finish):"))
    destination_user_to = [item for item in destination_user_to if item != ""]
    destination_user_cc = [item for item in destination_user_cc if item != ""]
    destination_user_bcc = [item for item in destination_user_bcc if item != ""]

    # if (destination_user_to[0] == "" and destination_user_cc[0] == "" and destination_user_bcc[0] == "") :
    #     print("No receiver. Quitting...")
    #     print("Press Enter to continue.")
    #     input()
    #     return -1
    subject = input("Subject: ")
    content = get_content()
    files = get_user_files()
    send_to_cc_receiver = destination_user_cc + destination_user_to
    send_bcc_receiver = destination_user_bcc
    # Manage "To" and "CC" option
    to_cc_option(send_to_cc_receiver, subject, content, files)
    #  Manage "BCC" option
    bcc_option(send_bcc_receiver, subject, content, files)

def create_message(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    # msg.attach(text)

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    return msg.as_string()

def get_user_files():
  """
  Prompts the user to attach files and returns a list of file paths.

  Returns:
    A list of file paths entered by the user.
  """
  files = []
  # Prompt user for file attachment
  print("Do you want to attach file?")
  choice = input("Y/Yes   N/No: ").lower()
  if choice == 'y':
    while True:
      user_input = input("Enter a file path (or leave blank to finish): ")
      if not user_input:
        break
      files.append(user_input)
  return files