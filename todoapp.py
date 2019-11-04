#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Flask web app

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import re

app = Flask(__name__)
to_do_list = []
status = ""


class Task:

    def __init__(self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority


@app.route('/')
def index():
   
    return render_template('index.html', to_do_list=to_do_list,
                           status=status)


@app.route('/submit', methods=['POST'])
def submit():

    global status
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if task == "":
        status = "Error: You must enter a task."
        return redirect("/")
    else:
        status = ""

    pattern = "^[^@]+[@]{1}[a-zA-Z0-9]+([\-]+[a-zA-Z0-9]+)*([\.]{1}[a-zA-Z" \
              "0-9]+([\-]+[a-zA-Z0-9]+)*)+"

    if not re.search(pattern, email):
        status = "Error: There was a problem adding the task. Try entering" \
                 " a valid e-mail."
        return redirect("/")
    else:
        status = ""

    if priority != "High" and priority != "Medium" and priority != "Low":
        status = "Error: There was a problem adding the task. Please select" \
                 " a priority."
        return redirect("/")
    else:
        status = ""

    t = Task(task, email, priority)
    to_do_list.append(t)

    return redirect("/")


@app.route('/clear', methods=['POST'])
def clear():

    del to_do_list[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():

    delete_index = int(request.form['index'])
    del to_do_list[delete_index]
    return redirect("/")

if __name__ == "__main__":

    app.run()
