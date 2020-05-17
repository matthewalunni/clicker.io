import sqlite3
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from datetime import datetime
import time

def line_graph():
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    # create cursor 
    db = conn.cursor()

    # Create click
    with conn:
        db.execute("SELECT * FROM click_tracker")
        x = db.fetchall()

    df = DataFrame(data = x, columns = ['ID', 'Type', "Time", "Total"])

    df.plot(x="Time", y='Total', kind = 'line')
    plt.show()

def get_avg_in():
    # connecting to the database  
    conn = sqlite3.connect("clicks.db", check_same_thread=False) 
    # create cursor 
    db = conn.cursor()

    # Create click
    with conn:
        db.execute("SELECT click_id, click_type,timestamp FROM click_tracker where click_id = 1 AND click_type = 1")
        x = db.fetchall()
        df = DataFrame(data = x, columns = ['click_id', 'click_type', 'timestamp'])
        first_in = df['timestamp'][0]

    with conn:
        db.execute ("SELECT max(click_id), click_type, timestamp FROM click_tracker WHERE click_type = 1")
        y = db.fetchall()
        df2 = DataFrame(data = y, columns = ['click_id', 'click_type', 'timestamp'])
        last_in = df2['timestamp'][0]

    # print(type(timestamp(first_in)))
    print(type(last_in))

    first_in = datetime.strptime(first_in, '%Y-%m-%d %H:%M:%S')
    last_in = datetime.strptime(last_in, '%Y-%m-%d %H:%M:%S')
    diff = last_in - first_in

    with conn:
        db.execute ("SELECT count(click_id) FROM click_tracker WHERE click_type = 1")
        in_count = db.fetchall()
        in_count = in_count[0][0]

    avg_in = diff/in_count

    return avg_in
