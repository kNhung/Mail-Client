import socket
from smtp_functions import send_email
from pop3_functions import receive_email

# HOST = "127.0.0.1"  # IP adress server
# PORT = 3335        # port is used by the server

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = (HOST, PORT)
# print("Client connect to server with port: " + str(PORT))
# client.connect(server_address)

# try:
#     while True:
#         msg = input('Client: ')
#         client.sendall(bytes(msg, "utf8"))

#         if msg == "quit":
#             break
#     # client.sendall(b"This is the message from client")
# except KeyboardInterrupt:
#     client.close()
# finally:
#     print('closing socket')
#     client.close()

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 2225
POP3_HOST = '127.0.0.1'
POP3_PORT = 3335

def main():
    # Gửi email
    #send_email(SMTP_HOST, SMTP_PORT)

    # Nhận email
    receive_email(POP3_HOST, POP3_PORT)

if __name__ == "__main__":
    main()