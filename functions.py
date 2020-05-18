from flask import Flask, render_template, request
import sqlite3
from functions import * 
import smtplib
import os
from email.message import EmailMessage
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from datetime import datetime
import time

def resetDB():
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    
    # create cursor  
    db = conn.cursor()

    # Drop table
    with conn: 
        db.execute("DROP TABLE click_tracker")

    # Create Giftcard Table
    with conn:
        db.execute("""CREATE TABLE click_tracker (
                    click_id INTEGER PRIMARY KEY,
                    click_type bool,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total INTEGER
                    )""")

def record_click(click_type, new_total):
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    
    # create cursor 

    # Grab current count 
    db = conn.cursor()

    # Create click
    with conn:
        db.execute("""INSERT INTO click_tracker (click_type, total) 
        VALUES (:click_type, :new_total)""", {
            "click_type": click_type,
            "new_total": new_total
        })  

def get_total():

    # connecting to the database  
    conn = sqlite3.connect('clicks.db', check_same_thread=False) 

    # create cursor  
    db = conn.cursor()
    db.execute("SELECT total FROM click_tracker WHERE click_id = (SELECT max(click_id) FROM click_tracker)")

    #Unpack vounter value
    fetch = db.fetchall()

    try:
        total = int(fetch[0][0])
    except:
        total = 0

    return total

def send_mail(receiver):
    # EMAIL
    my_email = "foodforalltest@gmail.com"
    my_password = "welovefood"
    EMAIL_ADDRESS = my_email
    EMAIL_PASSWORD = my_password

    msg = EmailMessage()
    msg['Subject'] = 'TEST'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver
    msg.set_content('This is the body of a TEST Email created and sent using PYTHON')

    msg.add_alternative("""
<!DOCTYPE html>
<html>
    <body>
        <body>
            This is a test.
        </body>
    </body>
</html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)

def get_avg_in():
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    # create cursor 
    db = conn.cursor()

    # Create click
    with conn:
        db.execute("SELECT min(click_id), click_type,timestamp FROM click_tracker where click_type = 1")
        x = db.fetchall()
        df = DataFrame(data = x, columns = ['click_id', 'click_type', 'timestamp'])
        first_in = df['timestamp'][0]

    with conn:
        db.execute ("SELECT max(click_id), click_type, timestamp FROM click_tracker WHERE click_type = 1")
        y = db.fetchall()
        df2 = DataFrame(data = y, columns = ['click_id', 'click_type', 'timestamp'])
        last_in = df2['timestamp'][0]

    with conn:
        db.execute ("SELECT count(click_id) FROM click_tracker WHERE click_type = 1")
        in_count = db.fetchall()
        in_count = in_count[0][0]

    if first_in != None: 
        first_in = datetime.strptime(first_in, '%Y-%m-%d %H:%M:%S')
        last_in = datetime.strptime(last_in, '%Y-%m-%d %H:%M:%S')
        diff = last_in - first_in
        avg_in = diff/in_count
    else:
        avg_in = 0

    avg_in = convert_timedelta(avg_in)

    return avg_in


def get_avg_out():
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    # create cursor 
    db = conn.cursor()

    # Create click
    with conn:
        db.execute("SELECT min(click_id), click_type,timestamp FROM click_tracker where click_type = 0")
        x = db.fetchall()
        df = DataFrame(data = x, columns = ['click_id', 'click_type', 'timestamp'])
        first_out = df['timestamp'][0]

    with conn:
        db.execute ("SELECT max(click_id), click_type, timestamp FROM click_tracker WHERE click_type = 0")
        y = db.fetchall()
        df2 = DataFrame(data = y, columns = ['click_id', 'click_type', 'timestamp'])
        last_out = df2['timestamp'][0]

    with conn:
        db.execute ("SELECT count(click_id) FROM click_tracker WHERE click_type = 0")
        out_count = db.fetchall()
        out_count = out_count[0][0]

    if first_out != None:     
        first_out = datetime.strptime(first_out, '%Y-%m-%d %H:%M:%S')
        last_out = datetime.strptime(last_out, '%Y-%m-%d %H:%M:%S')
        diff = last_out - first_out
        avg_out = diff/out_count
    else:
        avg_out = 0

    avg_out = convert_timedelta(avg_out)

    return avg_out

def get_max():

    # connecting to the database  
    conn = sqlite3.connect('clicks.db', check_same_thread=False) 

    # create cursor  
    db = conn.cursor()
    db.execute("SELECT max(total) FROM click_tracker")

    #Unpack vounter value
    fetch = db.fetchall()

    try:
        max = int(fetch[0][0])
    except:
        max = 0

    return max

def get_avg_stay():
    avg_stay = get_avg_in() - get_avg_out()
    return avg_stay

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return '{}h {}m {}s'.format(hours, minutes, seconds)

def convert_to_excel(filename_1):
    # connecting to the database  
    conn = sqlite3.connect('clicks.db', check_same_thread=False) 

    # create cursor  
    db = conn.cursor()
    db.execute("SELECT * FROM click_tracker")

    #Unpack vounter value
    fetch = db.fetchall()

    filename_1 = filename_1 + '.xlsx'

    df = DataFrame(data=fetch, columns = ['click_id','click_type', 'timestamp', 'total'] )
    
    path = 'filesforuser\\' + filename_1
    
    df.to_excel(path, sheet_name='you_rock')
