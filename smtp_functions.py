import socket
from email import Email

def input_content():
    print("Content:\n")
    lines = []
    while True:
        line = input()
        if(line.lower()) == '-end-': # Nếu người dùng nhập '-end-', kết thúc nhập
            break
        lines.append(line)
    return lines

def send_email(SMTP_HOST, SMTP_PORT):
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
        sender = input("From: ")
        smtp_socket.sendall(f'MAIL FROM: {sender}\r\n'.encode())
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        recipient = input("To: ")
        smtp_socket.sendall(f'RCPT TO: {recipient}\r\n'.encode())
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(b'DATA\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        subject = input("Subject: ")
        smtp_socket.sendall(f'Subject: {subject}\r\n'.encode())
        smtp_socket.sendall(b'\r\n')
        content = input_content()
        smtp_socket.sendall(f'{content}\r\n'.encode())
        smtp_socket.sendall(b'.\r\n')  # Kết thúc nội dung email
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        # Đóng kết nối
        smtp_socket.sendall(b'QUIT\r\n')
        smtp_socket.close()

        print("Email sent successfully!")
