#
# main source of reference at this point is from:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#


import sys
import imaplib
import getpass
import email
import datetime


mailitem = imaplib.IMAP4_SSL("imap.mail.yahoo.com")


def process_mailbox(mailitem):
	rv, data = mailitem.search(None, "ALL")
	if rv != 'OK':
		print "No messages found!"
		return

	for num in data[0].split():
		rv, data = mailitem.fetch(num, '(RFC822)')
		if rv != 'OK':
			print "ERROR getting message", num
			return

		msg = email.message_from_string(data[0][1])
		print 'Message %s: %s' % (num, msg['Subject'])
		print 'Raw Date:', msg['Date']
		date_tuple = email.utils.parsedate_tz(msg['Date'])
		if date_tuple:
			local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
			print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")


account = raw_input("Enter Yahoo email address: ")
pwd = getpass.getpass()

try:
	mailitem.login(account, pwd)
except imaplib.IMAP4.error:
	print "LOGIN FAILED!!! "

rv, mailboxes = mailitem.list()
if rv == "OK":
	print "Mailboxes: "

	print mailboxes

selection = raw_input("Select a mailbox: ")

rv, data = mailitem.select(selection)
if rv == "OK":
	print "Processing mailbox...\n"
	process_mailbox(mailitem)
	mailitem.close()
mailitem.logout()
