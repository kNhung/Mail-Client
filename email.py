class Email:
    def __init__(self, sender, receiver, subject, content, attachment=None):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.content = content
        self.attachment = attachment

    def set_attachment(self, attachment):
        self.attachment = attachment

    def display_info(self):
        print("From:", self.sender)
        print("To:", self.receiver)
        print("Subject:", self.subject)
        print("Content:", self.content)
        if self.attachment:
            print("Attachment:", self.attachment)
