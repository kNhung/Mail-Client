import socket
from email import Email
from email import parse_emails

def display_mail(mail):
    mail.display_info(mail)
    if(mail.attachment != None):
        print("Mail này có đính kèm, bạn có muốn tải xuống không?")
        while True:
            choice = input("y/Yes    n/No:   ")
            if choice == 'y':
                # Viết hàm tải file
                break
            elif choice == 'n':
                break
            else:
                print("Mời nhập lại!")
    print('\n')

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
        emails_info = pop3_socket.recv(1024).decode()
        print(emails_info)
        
        # Lặp qua danh sách các email và lấy nội dung của từng email
        emails = emails_info.strip().split('\n')[1:]
        emails_list = []  # Danh sách lưu trữ các đối tượng Email

        for email in emails:
            email_number = email.split()[0]
            # Lấy nội dung của email có số thứ tự là email_number
            pop3_socket.sendall(f'RETR {email_number}\r\n'.encode())
            email_content = pop3_socket.recv(4096).decode()

            # Tạo đối tượng Email và thêm nội dung email vào thuộc tính content
            new_email = Email(sender='', receiver='', subject='', content=email_content, attachment=None)
            emails_list.append(new_email)  # Thêm đối tượng Email vào danh sách

        # In danh sách mail
        for mail in emails_list:
            display_mail(mail)

        # Đóng kết nối
        pop3_socket.sendall(b'QUIT\r\n')
        pop3_socket.close()

        print("Email received successfully!")
