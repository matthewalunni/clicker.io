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

convert_to_excel(filename_1="hello")