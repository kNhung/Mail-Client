import socket
import client
import os
from extract_message import process_mime_message

def pop3_valid_reponse(code) :
    code = code[:3]
    if (code == "+OK") : return 1
    else :
        print("Error occurred. Quiting...")
        print("Press Enter to continue.")
        print("here?")
        input()
        return 0
    
def receive_mail():
    # whenever u want to sent your mail using SMTP, u have to send these following commands:
    # USER
    # PASS
    # STAT
    # LIST
    # RETR
    pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Opening the first unread message:")
    pop3_socket.connect((client.POP3_HOST, client.POP3_PORT))
    if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('USER ' + client.USERNAME + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('PASS ' + client.PASSWORD + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    
    pop3_socket.sendall(('STAT' + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1

    pop3_socket.sendall(('LIST' + '\r\n').encode())
    if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1

    # Return the content of the first mail
    pop3_socket.sendall(b'RETR 1\r\n')
    message = pop3_socket.recv(client.BUFFER_SIZE).decode()
    if (pop3_valid_reponse(message) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    # Define the directory path
    user_folder_path = os.path.join(os.getcwd(), "all_user/" +str(client.USERNAME))

    # Check if the directory exists
    if not os.path.exists(user_folder_path):
        # Create the directory
        os.makedirs(user_folder_path)
    process_mime_message(message, user_folder_path)
    pop3_socket.sendall(b'DELE 1\r\n')
    message = pop3_socket.recv(client.BUFFER_SIZE).decode()
    if (pop3_valid_reponse(message) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    pop3_socket.sendall(('QUIT\r\n').encode())
    print("Press Enter to continue.")
    input()
