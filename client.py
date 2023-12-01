import socket
from smtp_functions import send_email
from pop3_functions import receive_email

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 2225
POP3_HOST = '127.0.0.1'
POP3_PORT = 3335

def main():
    # Gửi email
    send_email(SMTP_HOST, SMTP_PORT)

    # Nhận email
    receive_email(POP3_HOST, POP3_PORT)

if __name__ == "__main__":
    main()