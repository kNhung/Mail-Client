import email
import json
import os
import base64

def process_mime_message(message_string, output_dir):
    temp = message_string.split('\r\n',1)
    message = email.message_from_string(temp[1])

    # Extract desired data
    data = {
        "Form": message["from"],
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
    
    # Save data to JSON file
    with open(os.path.join(output_dir, "message_data.json"), "w") as f:
        json.dump(data, f, indent=4)
