from flask import Flask, url_for, request, render_template, redirect, session
import db
import pymysql
from pwd_context import verify_password
import sys, os, random

app = Flask(__name__)

app.secret_key = "".join(
    [
        random.choice(
            ("ABCDEFGHIJKLMNOPQRSTUVXYZ" + "abcdefghijklmnopqrstuvxyz" + "0123456789")
        )
        for i in range(20)
    ]
)


@app.route("/", methods=["POST", "GET"])
def login():
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        if request.method == "GET":
            return render_template("login.html")

        # find user, check if exists
        login = request.form
        user = db.login_user(login["email"], conn)

        if user:
            # check password
            valid, update = verify_password(login["password"], user["password"])
            if valid:
                session["user"] = db.find_user(user["uid"], conn)
                return redirect(url_for("main"))

            message = "Incorrect login. Please try again"
            return render_template("login.html", message=message)
        # should message be no user found?
        message = "Incorrect login. Please try again"
        return render_template("login.html", message=message)


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/new-user", methods=["POST", "GET"])
def new_user():
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        if request.method == "GET":
            return render_template(
                "new_user.html",
                user={"name": "", "email": "", "class": "", "dob": "", "bio": ""},
            )
        user = request.form
        uid = db.insert_user(user, conn)

        # check if uid is none, meaning duplicate email
        if uid:
            user = db.find_user(uid, conn)
            session["user"] = user
            return redirect(url_for("user", uid=uid))

        message = "Username already taken, please change"
        return render_template("new_user.html", user=user, message=message)


@app.route("/new-event", methods=["POST", "GET"])
def new_event():
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        if request.method == "GET":
            return render_template("new_event.html")

        event = request.form
        eid = db.insert_event(event, session["user"]["uid"], conn)
        return redirect(url_for("event", eid=eid))

@app.route("/event/<eid>")
def event(eid):
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        event = db.find_event(eid, conn)
        if event:
            event['event_type'] = event['event_type'].split(',')
            comments = db.find_comments(eid, conn)
            if comments:
                return render_template("event.html", event=event, comments=comments)

                # for comment in comments:
                #     responses = db.find_responses(comment['cid'], conn)
                #     comment['responses'] = responses
            return render_template("event.html", event=event) 
        if request.method == 'POST':
            button_value = request.form.get('update')
            if button_value == 'update':
                return redirect(url_for('update_event', eid=eid))

            # instead of this, maybe making the "button" a
            # link to the correct endpoint?
        return redirect(url_for("main"))


@app.route("/user/<uid>", methods=["POST", "GET"])
def user(uid):
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        # parametrize, query from user table, maybe INNER JOIN RSVP table?
        # in main.html url_for user pass cookie UID as arg "My Profile"
        # look at shopping cart ex for cookie demonstration
        if request.method == "GET":
            user = db.find_user(uid, conn)
            if user:
                return render_template("user.html", user=user)
            return redirect(url_for("main"))
        user = request.form
        user = db.update_user(uid, user, conn)
        session["user"] = user
        return redirect(url_for("user", uid=uid))

#search function 
@app.route("/search")
def search():
    search_text = request.args.get("search", "").strip()
    
    # If there is no search query, redirect back to the main page
    if not search_text:
        return redirect(url_for("main"))
        
    with pymysql.connect(read_default_file="~/.my.cnf", database="squest_db") as conn:
        pattern = f"%{search_text}%"
        events = db.search_events(pattern, conn)

        print(f"Found {len(events)} events matching the search pattern '{search_text}'.")

        # If no events found, flash a message and redirect back
        if len(events) == 0:
            return render_template("main.html", events=events)

        # Redirect to the event page if there is only one match
        if len(events) == 1:
            eid = events[0]['eid']
            return redirect(url_for("event", eid=eid))

        # Multiple matches found: render the main page passing the filtered events
        return render_template("main.html", events=events)

# creating endpoints for new comment and new response, which will update respective data
# bases and redirect to event.html

if __name__ == "__main__":
    import os

    uid = os.getuid()
    app.debug = True
    app.run("0.0.0.0", uid)
