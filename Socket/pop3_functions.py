import socket

def receive_email(POP3_HOST, POP3_PORT):
    # Kết nối đến POP3 Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pop3_socket:
        pop3_socket.connect((POP3_HOST, POP3_PORT))
        response = pop3_socket.recv(1024).decode()
        print(response)

        # Viết code để nhận email từ server POP3 thông qua socket ở đây
        pop3_socket.sendall(b'USER receiver@example.com\r\n')
        response = pop3_socket.recv(1024).decode()
        print(response)  # Phản hồi từ server

        pop3_socket.sendall(b'PASS your_password\r\n')
        response = pop3_socket.recv(1024).decode()
        print(response)

        #Gửi lệnh để lấy số lượng email
        pop3_socket.sendall(b'STAT\r\n')
        response = pop3_socket.recv(1024).decode()
        print(response)

        #Lấy danh sách email
        pop3_socket.sendall(b'LIST\r\n')
        response = pop3_socket.recv(1024).decode()
        print(response)

        #Lấy nội dung email
        pop3_socket.sendall(b'RETR 1\r\n')
        email_content = b''
        while True:
            part = pop3_socket.recv(1024)
            if not part:
                break
            email_content += part
        email_content = email_content.decode()
        print(email_content)

        # Đóng kết nối
        pop3_socket.sendall(b'QUIT\r\n')
        pop3_socket.close()

        print("Email received successfully!")
