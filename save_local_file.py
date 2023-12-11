# Description: using binary data from a json file to recreate the original file
import os
import base64
import json
import client

# function that takes binary data from a json file and recreate the original file
def recreate_file(folder_name,file_base_name, file_name_extension, binary_data):
    if not os.path.exists(f'all_user/{folder_name}'):
        os.makedirs(f'all_user/{folder_name}')
    absolute_path = os.path.dirname(__file__) # đường dẫn tới project
    # get the path to the folder
    folder_path = os.path.join(absolute_path, f"all_user\\{folder_name}")
    # get the path to the file
    file_path = os.path.join(folder_path, f"{file_base_name}.{file_name_extension}")
    # create the file
    with open(file_path, 'wb') as f:
        f.write(binary_data)

#show list of attachments stored in a json file
def show_attachments(json_obj, folder_name):
    while(True):
        os.system('cls')
        # get the list of attachments
        attachments = json_obj['Attachments']
        # get the number of attachments
        number_of_attachments = len(attachments)
        # if there is no attachment
        if number_of_attachments == 0:
            print("There is no attachment")
        # if there is at least 1 attachment
        else:
            # print the list of attachments
            print("List of attachments:")
            for i in range(number_of_attachments):
                print(f"{i+1}. {attachments[i]['filename']}")
        # get the user's choice
        choice = input("Enter the number indicating the attachment you want to download (Press Enter to go back to main menu): ")
        # if the user press Enter
        if choice == "":
            return
        # if the user enter an invalid choice
        elif not choice.isdigit() or int(choice) < 1 or int(choice) > number_of_attachments:
            print("Invalid choice")
            # clear the screen
            os.system('cls')
            # show the menu again
            show_attachments(json_obj, folder_name)
            return
        # else recreate the file
        else:
            # get the index of the attachment in the list
            index = int(choice) - 1
            # get the attachment's file base name
            file_base_name = attachments[index]['filename'].split('.')[0]
            # get the attachment's file name extension
            file_name_extension = attachments[index]['filename'].split('.')[1]
            # get the attachment's binary data
            binary_data = base64.b64decode(attachments[index]['content'])
            # recreate the file
            recreate_file(folder_name, file_base_name, file_name_extension, binary_data)
            # show the message
            print(f"Downloaded {attachments[index]['filename']}")
            input("Press Enter to continue")


