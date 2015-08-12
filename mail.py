#
# main source of reference at this point is from:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#


import sys
import imaplib
import getpass
import email
import datetime


def process_mailbox(mail_item):
	rv, data = mail_item.search(None, "ALL")
	if rv != 'OK':
		print "No messages found!"
		return

	for num in data[0].split():
		rv, data = mail_item.fetch(num, '(RFC822)')
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


server_entry = input(("Select the email service\n1: Yahoo Mail\n2: Gmail\n3: Microsoft Email"
                      "(Hotmail, outlook.com, live.com)\n[1, 2, 3, etc.]: "))

if server_entry == 1:
	mail_item = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
	account = raw_input("Enter Yahoo email address: ")
	pwd = getpass.getpass()
elif server_entry == 2:
	mail_item = imaplib.IMAP4_SSL("imap.gmail.com")
	account = raw_input("Enter Gmail address: ")
	pwd = getpass.getpass()
elif server_entry == 3:
	mail_item = imaplib.IMAP4_SSL("imap-mail.outlook.com")
	account = raw_input("Enter Microsoft email address: ")
	pwd = getpass.getpass()
else:
	print "Please choose a supported email domain."
	sys.exit(0)

try:
	mail_item.login(account, pwd)
except imaplib.IMAP4.error:
	print "LOGIN FAILED!!! "

# next steps: reformat the retrieved mail folder lists
# and enumerate results
rv, mailboxes = mail_item.list()
mailboxes = ''.join(mailboxes).translate(None, ')(/\\"').replace('HasChildren', '') \
	.replace('HasNoChildren', '')
if rv == "OK":
	print "Mailboxes: "
	print mailboxes

selection = raw_input("Select a mailbox: ")

# next steps:
# change to display current messages first
# limit rresults to twenty retrieved at a time
# implement a way to continue getting messages after the first 20
rv, data = mail_item.select(selection)
if rv == "OK":
	print "Processing mailbox...\n"
	process_mailbox(mail_item)
	mail_item.close()

# next steps:
# add mechanism to pick message to view
# read, format and display header info (to, from, remote IP)
# parse message content for URLs (optimally those different that originating domain)

mail_item.logout()
