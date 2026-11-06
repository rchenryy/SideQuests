from flask import (Flask, url_for, request, render_template, redirect, session)
import db

import sys,os,random

app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/main")
def main():
    return render_template("main.html")
            
@app.route("/new-user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return render_template("new_user.html", user={'name':'','email':'','class':'','dob':'','bio':''})
    user = request.form.to_dict()
    uid = db.insert_user(user)
    
    # check if uid is none, meaning duplicate email
    if uid:
        session['uid'] = uid
        return redirect(url_for("user", uid=uid))

    message = 'Username already taken, please change'
    return render_template("new_user.html", user=user, message=message)

@app.route("/new-event", methods=['POST', 'GET'])
def new_event():
    if request.method == 'GET':
        return render_template("new_event.html")

    event = request.form.to_dict()
    db.insert_event(event, session['uid'])
    return redirect(url_for("event", event=event))

#event placeholder data for html
events = [
    {
        "id": 0,
        "event_name": "Kelela Concert",
        "city": "Boston",
        "date": "2026-11-15T20:00",
        "meeting_point": "Main Entrance",
        "price": "100",
        "description": "Hi, just found out Kelela is coming to town! I have an extra ticket for sale if anyone is interested.",
        "comments": [
            {
                "username": "Mary",
                "comment_text": "That sounds fun, I would like to go!",
                "timestamp": "2026-10-20 14:30:00",
                "replies": [
                    {
                        "username": "Alice",
                        "comment_text": "I would love to join as well.",
                        "timestamp": "2026-10-20 15:00:00"
                    }
                ]
            },
            {
                "username": "Lucy",
                "comment_text": "I'm interested, how can I get the ticket?",
                "timestamp": "2026-10-20 16:00:00",
                "replies": []
            }
        ]
    }
]

@app.route("/event/")
def event():
    return render_template("event.html", event=events[0]) 

@app.route("/user/<uid>")
def user(uid):
    # parametrize, query from user table, maybe INNER JOIN RSVP table?
    # in main.html url_for user pass cookie UID as arg "My Profile"
    # look at shopping cart ex for cookie demonstration
    user = db.find_user(uid)
    return render_template("user.html", user=user)

# creating endpoints for new comment and new response, which will update respective data
# bases and redirect to event.html

if __name__ == '__main__':
    import os
    uid = os.getuid()
    app.debug = True
    app.run('0.0.0.0',uid)