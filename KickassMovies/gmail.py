import email
import imaplib
import smtplib
import logging

import keyring
import yagmail

logger=logging.getLogger(__name__)
class Gmail:
    def __init__(self, email_address):
        self.email_address = email_address
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

    def login_imap(self):
        self.imap.login(self.email_address, keyring.get_password("KickassMovies", self.email_address))

    def login_yagmail(self):
        self.yagmail = yagmail.SMTP(self.email_address, keyring.get_password("KickassMovies", self.email_address))

    def get_unread(self):
        self.login_imap()
        retcode, messages = "", ""
        try:
            self.imap.list()
            self.imap.select('inbox')
            (retcode, messages) = self.imap.search(None, '(UNSEEN)')
        except self.imap.abort:
            logger.error("imaplib abort, waiting until next turn")
            print("")
        except TimeoutError:
            logger.error("Inbox timed out")
            print("")

        unread = []
        if retcode == "OK":
            for num in messages[0].split():
                typ, data = self.imap.fetch(num,'(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        unread.append(email.message_from_bytes(response_part[1]))
                        self.imap.store(num, '+FLAGS', '\\Seen')
        else:
            logger.warning("Inbox retrieval failed")
            print("")

        self.imap.logout()
        return unread

    def send_email(self, receivers, subject, message):
        try:
            self.yagmail.send(receivers, subject, message)
        except smtplib.SMTPException:
            self.login_yagmail()
            self.yagmail.send(receivers, subject, message)