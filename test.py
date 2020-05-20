import sqlite3
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from datetime import datetime
import time
from functions import *

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

# # def longest_wait_time():
# # connecting to the database  
# conn = sqlite3.connect("clicks.db", check_same_thread=False) 
# # create cursor 
# db = conn.cursor()
# # Create click
# with conn:
#     db.execute("SELECT * FROM click_tracker")
#     x = db.fetchall()

# def get_avg_stay():
# avg_stay = get_avg_out() - get_avg_in()
    # return avg_stay

a = get_avg_in()
print(a)

b = get_avg_out()
print(b)

c = b-a
print(c)