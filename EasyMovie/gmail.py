import imaplib, smtplib, yagmail, os, email


def __init__(self):
    self.imap = imaplib.IMAP4_SSL("imap.gmail.com")


def login_imap(self):
    self.imap.login("addtowunasmovies@gmail.com","")


def login_yagmail(self):
    self.yagmail = yagmail.SMTP("addtowunasmovies@gmail.com","")


def get_unread(self):
    try:
        self.imap.list()
        self.imap.select('inbox')
        (retcode, messages) = self.imap.search(None, '(UNSEEN)')
    except self.imap.abort:
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.login_imap()

        self.imap.list()
        self.imap.select('inbox')
        (retcode, messages) = self.imap.search(None, '(UNSEEN)')

    unread = []
    if retcode == "OK":
        for num in messages[0].split():
            typ, data = self.imap.fetch(num,'(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                     unread.append(email.message_from_bytes(response_part[1]))
                     self.imap.store(num, '+FLAGS', '\\Seen')
    return unread


def send_email(self, receivers, subject, message):
    try:
        self.yagmail.send(receivers, subject, message)
    except smtplib.SMTPException:
        self.login_yagmail()
        self.yagmail.send(receivers, subject, message)
