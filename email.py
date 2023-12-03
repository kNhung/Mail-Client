class Email:
    def __init__(self, sender, receiver, subject, content, file_path=None, attachment=None):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.content = content
        self.file_path = file_path
        self.attachment = attachment

    def set_attachment(self, attachment):
        self.attachment = attachment

    def display_info(self):
        print("From:", self.sender)
        print("To:", self.receiver)
        print("Subject:", self.subject)
        print("Content:\n", self.content)
        # if self.attachment:
        #     print("Attachment:", self.attachment)

def parse_emails(emails_info):
        print("Received emails_info:", emails_info)
        emails = emails_info.strip().split('\n')[1:]
        email_list = []
        for email in emails:
            email_info = email.split()
            print(email_info)
            email_number = email_info[0]
            email_sender = email_info[1]
            email_subject = ' '.join(email_info[2:])
            new_email = Email(sender=email_sender, receiver='', subject=email_subject, content='', attachment=None)
            email_list.append(new_email)
        return email_list