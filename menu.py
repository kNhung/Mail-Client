import pop3_functions
import smtp_functions
import client
import socket
from consolemenu import *
from consolemenu.items import *

def change_username():
    global username
    print("Please enter your username:")
    username = input()


def menu():
    # Initialize socket:
    smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = "dn24"
    password = "xxxx"
    # Create the menu
    menu = ConsoleMenu("SIMPLE MAIL CLIENT", "Group 12!")
    change_user_option = FunctionItem("Choose Username", change_username)
    send_option = FunctionItem("Send Mail Using SMTP", lambda:smtp_functions.send_mail(client.SMTP_HOST, client.SMTP_PORT, client.BUFFER_SIZE, client.DOMAIN, smtp_socket, username))
    receive_option = FunctionItem("Receive Mail Using Pop3", lambda:pop3_functions.receive_mail(client.POP3_HOST, client.POP3_PORT, client.BUFFER_SIZE, client.DOMAIN, pop3_socket, username, password))

    menu.append_item(change_user_option)
    menu.append_item(send_option)
    menu.append_item(receive_option)
    menu.show()
