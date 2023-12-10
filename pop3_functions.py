import socket
import client
import os
import time
from extract_message import process_mime_message

def pop3_valid_reponse(code) :
    code_ = code[:3]
    if (code_ == "+OK") : return 1
    else :
        print("Error occurred while loading mail.")
        return 0
    
def receive_mail():
    # whenever u want to sent your mail using SMTP, u have to send these following commands:
    # USER
    # PASS
    # STAT
    # LIST
    # RETR
    pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    message = pop3_socket.recv(client.BUFFER_SIZE).decode()
    if (pop3_valid_reponse(message) == 0) : 
        pop3_socket.sendall(('QUIT\r\n').encode())
        return -1
    temp = message.split(' ')
    total_mail = int(temp[1])
    loaded_mail = count_files_in_folder(client.USERNAME)
    while (loaded_mail < total_mail):
        pop3_socket.sendall(('LIST' + '\r\n').encode())
        if (pop3_valid_reponse(pop3_socket.recv(client.BUFFER_SIZE).decode()) == 0) : 
            pop3_socket.sendall(('QUIT\r\n').encode())
            return -1
        pop3_socket.sendall(f'RETR {loaded_mail + 1}\r\n'.encode())
        message = b''
        while True:
            part = pop3_socket.recv(client.BUFFER_SIZE)
            message += part
            if len(part) < client.BUFFER_SIZE:
                # either 0 or end of data
                break
        message = message.decode()
        if (pop3_valid_reponse(message) == 0) : 
            pop3_socket.sendall(('QUIT\r\n').encode())
            return -1
        # Define the directory path
        user_folder_path = os.path.join(os.getcwd(), "all_user", str(client.USERNAME))

        # Check if the directory exists
        if not os.path.exists(user_folder_path):
            # Create the directory
            os.makedirs(user_folder_path)
        process_mime_message(message, user_folder_path, loaded_mail)
        loaded_mail = count_files_in_folder(client.USERNAME)
    #print("All unloaded mails have been loaded.")
    pop3_socket.sendall(('QUIT\r\n').encode())

def count_files_in_folder(username):
  """
  Counts the number of files in a folder, including files in subfolders.

  Args:
    username: The username we are counting file.

  Returns:
    The number of files in the folder and its subfolders.
  """
  file_list = []
  folder_path = os.path.join(os.getcwd(), "all_user/" + username)
  for root, _, files in os.walk(folder_path):
    for file in files:
        file_list.append(file)
  return len(set(file_list))

