import socket
import base64
import os
from email import Email

MAX_FILES_SIZE = 3 * 1024 * 1024 # 3MB expressed in bytes

def attach_file():
    file_paths = []
    files_size = 0
    file_path =''
    print("<Press 'X' to end adding file>")
    print("Max files size: 3 MB")
    while file_path != 'X':
        file_path = input("Path to file: ")
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if files_size + file_size <= MAX_FILES_SIZE:
                files_size += file_size
                file_paths.append(file_path)
            else:
                print("File size exceeds!!")
                if file_size > 0:
                    print("Do you want to delete previous file?")
                    choice = input("y/Yes  n/No")
                    if choice == 'y':
                        file_paths.pop()
                        files_size -= os.path.getsize(file_paths)
            


        

def input_content():
    print("Content:")
    print("(type '-end-' to end content part)")
    content = ""
    while True:
        line = input()
        if(line.lower()) == '-end-': # Nếu người dùng nhập '-end-', kết thúc nhập
            break
        content += line + '\n' # Kết hợp các dòng thành 1 chuỗi duy nhất
    return content.rstrip('\n') # Loại bỏ kí tự xuống dòng cuối cùng nếu có

def write_mail():
    sender = input("From: ")
    receiver = input("To: ")
    subject = input("Subject: ")
    content = input_content()

    # Attach file
    print("Do you want to attach file?")
    choice = input("y/Yes   n/No: ")
    if choice == 'y':
        file_nums = input("Number of files: ")
        i = 1
        for i in file_nums:
            file_path = input("Path to file {i}: ")
            with open(file_path, 'rb') as attachment_file:
                attachment_data = attachment_file.read()
                base64_attachment = base64.b64encode(attachment_data).decode()
    else:
        file_path = None
        base64_attachment = None

    mail = Email(sender,receiver,subject,content, file_path, base64_attachment)
    return mail


def send_email(SMTP_HOST, SMTP_PORT):
    mail = write_mail()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as smtp_socket:
        # Kết nối đến SMTP Server
        smtp_socket.connect((SMTP_HOST, SMTP_PORT))
        respone = smtp_socket.recv(1024).decode()
        print(respone)

        # Gửi dữ liệu tới SMTP Server để gửi email
        smtp_socket.sendall(b'EHLO example.com\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)

        # Viết code để gửi email thông qua socket ở đây
        smtp_socket.sendall(f'MAIL FROM: {mail.sender}\r\n'.encode())
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(f'RCPT TO: {mail.receiver}\r\n'.encode())
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(b'DATA\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(f'From: {mail.sender}\r\n'.encode())
        smtp_socket.sendall(f'To: {mail.receiver}\r\n'.encode())
        smtp_socket.sendall(f'Subject: {mail.subject}\r\n'.encode())
        smtp_socket.sendall(b'\r\n')
        smtp_socket.sendall(f'{mail.content}\r\n'.encode())
        smtp_socket.sendall(b'\r\n')

        if mail.attachment != None:
            smtp_socket.sendall(f'Content-Type: application/octet-stream; name="{mail.file_path}"\r\nContent-Disposition: attachment; filename="{mail.file_path}"\r\nContent-Transfer-Encoding: base64\r\n\r\n{mail.attachment}\r\n'.encode())
        
        smtp_socket.sendall(b'.\r\n')  # Kết thúc nội dung email
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        # Đóng kết nối
        smtp_socket.sendall(b'QUIT\r\n')
        smtp_socket.close()

        print("Email sent successfully!")
