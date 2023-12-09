import pop3_functions
import smtp_functions
import client
import socket
import show_mail
from consolemenu import *
from consolemenu.items import *

def change_username():
    client.USERNAME = input("Please enter your username:")
    print(client.USERNAME)
    print("Press Enter to continue.")
    input()

def show_current_user(): 
    print(client.USERNAME)
    print("Press Enter to continue.")
    input()

def menu():
    # Create the menu
    menu = ConsoleMenu("SIMPLE MAIL CLIENT", "Group 12!")
    change_user_option = FunctionItem("Choose Username", change_username)
    send_option = FunctionItem("Send Mail Using SMTP", smtp_functions.send_mail)
    receive_option = FunctionItem("Receive Mail Using Pop3", pop3_functions.receive_mail)
    show_mail_option = FunctionItem("Show Mail", show_mail.show_mail_choices)
    test_option = FunctionItem("Show current user", show_current_user)
    menu.append_item(change_user_option)
    menu.append_item(send_option)
    menu.append_item(receive_option)
    menu.append_item(show_mail_option)
    menu.append_item(test_option)
    menu.show()
