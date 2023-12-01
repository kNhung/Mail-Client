from menu import display_menu
from smtp_functions import send_email
from pop3_functions import receive_email

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 2225
POP3_HOST = '127.0.0.1'
POP3_PORT = 3335

def main():
    while True:
        choice = display_menu()
        if choice == 1:
            send_email(SMTP_HOST, SMTP_PORT)
        elif choice == 2:
            receive_email(POP3_HOST,POP3_PORT)
        elif choice == 3:
            print("Xincamon")
            return
        else:
            print("Mời chọn lại!")
    return


if __name__ == "__main__":
    main()