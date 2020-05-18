from flask import Flask, render_template, request, redirect, url_for,send_file
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
    try:
        avg_in = get_avg_in()
    except:
        avg_in = 0
    try:
        avg_out = get_avg_out()
    except:
        avg_out = 0
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
    return redirect(url_for('click'))

@app.route('/reset', methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        resetDB()
    return redirect(url_for('click'))

@app.route('/download', methods=['GET','POST'])
def download():
    if request.method == 'POST':
        filename_1 = request.form.get("filename_1")
        convert_to_excel(filename_1)
        path = 'filesforuser\\' + filename_1 + '.xlsx'
    return send_file(path, as_attachment=True)

# To run
if __name__ == "__main__":
    app.run(debug=True)