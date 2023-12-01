import socket

def send_email(SMTP_HOST, SMTP_PORT):
    # Kết nối đến SMTP Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as smtp_socket:
        smtp_socket.connect((SMTP_HOST, SMTP_PORT))
        respone = smtp_socket.recv(1024).decode()
        print(respone)

        # Gửi dữ liệu tới SMTP Server để gửi email
        smtp_socket.sendall(b'EHLO example.com\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)

        # Viết code để gửi email thông qua socket ở đây
        smtp_socket.sendall(b'MAIL FROM: <sender@example.com>\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(b'RCPT TO: <receiver@example.com>\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(b'DATA\r\n')
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        smtp_socket.sendall(b'Subject: Test email\r\n')
        smtp_socket.sendall(b'\r\n')
        smtp_socket.sendall(b'This is a test email\r\n')
        smtp_socket.sendall(b'.\r\n')  # Kết thúc nội dung email
        response = smtp_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        # Đóng kết nối
        smtp_socket.sendall(b'QUIT\r\n')
        smtp_socket.close()

        print("Email sent successfully!")
