from flask import Flask, render_template, request
import sqlite3
from functions import * 
import smtplib
import os
from email.message import EmailMessage

app = Flask(__name__)


# Connecting to the database  
connection = sqlite3.connect("clicks.db", check_same_thread=False) 
# Cursor  
db = connection.cursor() 

@app.route('/', methods=['GET','POST'])
def click():
    total = get_total()
    if request.method == 'POST':
        total = get_total()
        if request.form['clicker'] == 'In':
            click_type = 1
            new_total = total + 1
        elif request.form['clicker'] == 'Out':
            click_type = 0
            new_total = total - 1  
        record_click(click_type, new_total)
        print("There's A Click!")
        total = get_total()
    avg_in = get_avg_in()
    avg_out = get_avg_out()
    max = get_max()
    return render_template("click.html", total=total, avg_in = avg_in, avg_out=avg_out, max=max)

# EMAIL
my_email = "foodforalltest@gmail.com"
my_password = "welovefood"

@app.route('/email', methods=['GET','POST'])
def email():
    total = get_total()
    if request.method == 'POST':
        receiver = request.form.get("email")
        send_mail(receiver)
    avg_in = get_avg_in()
    return render_template("click.html", total=total, avg_in = avg_in)

@app.route('/reset', methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        resetDB()
        total = 0
    return render_template("click.html", total=total)

# To run
if __name__ == "__main__":
    app.run(debug=True)