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

# def get_avg_out():
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


print(avg_out)