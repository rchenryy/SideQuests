from flask import (Flask, url_for, request, render_template, redirect)

app = Flask(__name__)

users = [{"name": "RC", "email": "rh107", "class_year": 2027, "dob": "10/05/2004", "bio": "I like to think of myself as extremely mediocre."}]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/main")
def main():
    return render_template("main.html")
            
@app.route("/new-user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return render_template("new_user.html")
    user = request.form.to_dict()
    # TODO:save to your database here
    return redirect(url_for("user"))
    # return redirect(url_for("user.html", user=user))

@app.route("/new-event", methods=['POST', 'GET'])
def new_event():
    if request.method == 'GET':
        return render_template("new_event.html")
    
    # TODO:save to your database here
    return redirect(url_for("event"))

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

@app.route("/user/")
def user():
    # parametrize, query from user table, maybe INNER JOIN RSVP table?
    # in main.html url_for user pass cookie UID as arg "My Profile"
    # look at shopping cart ex for cookie demonstration
    return render_template("user.html", user=user)

if __name__ == '__main__':
    import os
    uid = os.getuid()
    app.debug = True
    app.run('0.0.0.0',uid)