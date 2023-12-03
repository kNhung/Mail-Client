import socket
from email import Email

def input_content():
    print("Content:")
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
    mail = Email(sender,receiver,subject,content)
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

        smtp_socket.sendall(f'Subject: {mail.subject}\r\n'.encode())
        smtp_socket.sendall(b'\r\n')
        smtp_socket.sendall(f'{mail.content}\r\n'.encode())
        smtp_socket.sendall(b'.\r\n')  # Kết thúc nội dung email
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        # Đóng kết nối
        smtp_socket.sendall(b'QUIT\r\n')
        smtp_socket.close()

        print("Email sent successfully!")
