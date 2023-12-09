import email
import json
import os
import base64
import client
import yaml
from typing import List, Dict


def process_mime_message(message_string, output_dir, indexMail):
    temp = message_string.split('\r\n',1)
    message = email.message_from_string(temp[1])

    # Extract desired data
    data = {
        "Flag" : 'unread',
        "From": message["from"],
        "To": message["to"],
        "Date": message["date"],
        "Subject": message["subject"],
    }

    # Extract content
    content = None
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            content = part.get_payload(decode=True).decode("utf-8")
            break

    data["Content"] = content

    # Extract attachments (if any)
    attachments = []
    for part in message.walk():
        if part.get_content_type() == "application/octet-stream":
            filename = part.get_filename()
            content_type = part.get_content_type()
            content = part.get_payload(decode=True)
            attachments.append({"filename": filename, "content_type": content_type, "content": content})

    data["Attachments"] = attachments
    # Encode attachment content
    for attachment in data["Attachments"]:
        attachment["content"] = base64.b64encode(attachment["content"]).decode("utf-8")
    
    create_folder(client.USERNAME)
    location = filter(data)
    for folder in location:
        with open(os.path.join(output_dir, folder, f"mail{indexMail + 1}.json"), "w") as f:
            json.dump(data, f, indent=4)

    # # Save data to JSON file 
    # with open(os.path.join(output_dir, "message_data.json"), "w") as f:
    #     json.dump(data, f, indent=4)


def filter(dict_):
    # Load the configuration file
    with open('config.yml', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Check against rules
    folder_list = []
    for rule in config["Rules"]:
        for field in ["Subject", "Content", "From"]:
            if any(keyword in dict_[field] for keyword in rule.get(field, [])):
                folder_list.append(rule["Folder"])
                break

    # Check against default folder if no rule matches
    if not folder_list:
        folder_list.append("Inbox")

    return folder_list


def create_folder(user):
	lists = ['Project', 'Important', 'Inbox', 'Work', 'Spam']
	for folder in lists:
		if not os.path.exists(f'all_user/{user}/{folder}'):
			os.makedirs(f'all_user/{user}/{folder}')