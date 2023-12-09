import socket
import client
import os
import json
import time
import save_local_file
from extract_message import process_mime_message

absolute_path = os.path.dirname(__file__) # đường dẫn tới project
lists = ['Inbox', 'Project', 'Important', 'Work', 'Spam'] # điều chỉnh lại danh sách theo thứ tự trong hướng dẫn

def count_files_in_specific_folder(username, filter): # đếm số lượng mail có trong 1 folder nhất định (ví dụ folder inbox có 3 mail thì trả ra 3)
  file_list = []
  folder_path = os.path.join(absolute_path, f"all_user\\{username}\\{filter}")
  for root, _, files in os.walk(folder_path):
    for file in files:
        file_list.append(file)
  return len(set(file_list))

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


def show_mail_choices():
    #get user input into _option variable
    _option = 0
    #handle if DIR = absolute_path + f'\\all_user\\{client.USERNAME} does not exist
    if not os.path.exists(absolute_path + f'\\all_user\\{client.USERNAME}'):
        print(f"Username: \'{client.USERNAME}\' haven't loaded any mail yet")
        input("Press Enter to go back to main menu")
        return
    
    while _option not in [f"{i}" for i in range(1, len(lists) + 1)]:
        print(f"This is {client.USERNAME} folders.")
        cnt = 1
        for folder in lists:
            print(f"{cnt}. {folder}")
            cnt += 1
        _option = input("Select a folder in your mailbox (Press Enter to go back to main Menu): ")
        if _option == "":
            return
        if _option not in [f"{i}" for i in range(1, len(lists) + 1)]:
            print("Invalid")
            #when user input invalid choice, clear the screen and show the menu again
            os.system('cls')
            continue
    _option = int(_option) - 1
    #get number of files in folder
    number_of_files_a_folder = count_files_in_specific_folder(client.USERNAME, lists[_option]) # số lượng mail
    #get folder name
    DIR = absolute_path + f'\\all_user\\{client.USERNAME}\\{lists[_option]}\\'

    #get file names
    file_names = os.listdir(DIR) # tên các mail trong folder (ví dụ khi print(file_names) sẽ ra ['mail1.json','mail2.json'])
    num_of_mail = [] 
    for file_name in file_names:
        pos = file_name.find('.')
        num_of_mail.append(file_name[4:pos])    # do các mail được pop theo thứ tự mail1, mail2, mail3, ... Vào các folder riêng biệt nên cần biết danh sách thứ tự các mail trong 1 folder
                                                # ví dụ như trong 'inbox' có 3 mail là ['mail3.json','mail7.json','mail8.json'] thì output num_of_mail = ['3','7','8']
    print(f"Your mails in {lists[_option]} folder:")
    #handle the case when there is no mail in folder
    if number_of_files_a_folder == 0:
        print("\nThere is no mail in this folder\n")
        input("Press Enter to go back to main menu")
        os.system('cls')
        show_mail_choices()
        return
    for i in range(number_of_files_a_folder):
        # problem here
        with open(os.path.join(absolute_path, f'all_user\\{client.USERNAME}\\{lists[_option]}\\mail{num_of_mail[i]}.json'),'r') as json_data:
            obj = json.load(json_data) # chạy theo thứ tự mail đầu tiên, mail thứ 2, .. Trong folder 'inbox' hoặc...
        if str(obj["Flag"]) == 'unread':
            print(f'{i + 1}. <{str(obj["Flag"])}> <From: {str(obj["From"])}>, <Subject: {str(obj["Subject"])}>')
        elif str(obj["Flag"]) == 'read':
            print(f'{i + 1}. <From: {str(obj["From"])}>, <Subject: {str(obj["Subject"])}>')
    choice_1 = input("Select which mail you want to read (Press Enter to Go back): ") #sau khi hiển thị danh sách các mail và trạng thái đã đọc hay chưa thì cho người dùng chọn mail bất kỳ để đọc
    if choice_1 == '': # #nếu nhấn Enter thì thoát về danh sách các folder 1. Inbox, 2. Important,...
        os.system('cls')
        show_mail_choices()
    else :
        choice_1_ = int(choice_1)
        if choice_1_ < 1 or choice_1_ > number_of_files_a_folder:
            return
        else:
            os.system('cls')
            with open(os.path.join(absolute_path, f'all_user\\{client.USERNAME}\\{lists[_option]}\\mail{num_of_mail[choice_1_ - 1]}.json'),'r') as json_data_1:
                obj = json.load(json_data_1) # truy cập và đọc file json
            print("Your mail:")
            print("\tFrom: " + str(obj["From"]))
            print("\tTo: " + str(obj["To"]))
            print("\tDate: " + str(obj["Date"]))
            print("\tSubject: " + str(obj["Subject"]))
            print("\tContent: " + str(obj["Content"]))
            if obj["Attachments"] != []:
                # show the list of file in Attachments
                m = len(obj["Attachments"])
                for i in range(m):
                    print(f"\tAttachment {i + 1}: {obj['Attachments'][i]['filename']}")
                print("This mail contains files. Do you want to download this file/these files from it?")
                # get user input into choice_2 variable
                choice_2 = input("Enter your choice (Y/N): ")
                if choice_2 == "":
                    os.system('cls')
                    show_mail_choices()
                #if user input invalid choice
                elif (choice_2).lower() not in ['y', 'n']:
                    print("Invalid choice")
                    # clear the screen
                    os.system('cls')
                    # show the menu again
                    show_mail_choices()
                #if user input valid choice
                else:
                    choice_2 = (choice_2).lower()
                    if choice_2 == 'y':
                        save_local_file.show_attachments(obj,"downloaded_files")
                    else:
                        os.system('cls')
                        show_mail_choices()

            obj["Flag"] = 'read' #sau khi đọc mail này thì chuyển trạng thái của mail thành 'đã đọc'
            with open(os.path.join(absolute_path, f'all_user\\{client.USERNAME}\\{lists[_option]}\\mail{num_of_mail[choice_1_ - 1]}.json'),'w') as json_data_1:
                json.dump(obj, json_data_1)
        input(f"\nPress Enter to go back {lists[_option]} folder:") # sau khi đọc mail thì nhấn Enter để về danh sách các mail trong folder đang đọc
        os.system('cls')
        show_mail_choices()

    
