from flask import (Flask, url_for, request, render_template, redirect)

app = Flask(__name__)

users = [{"name": "RC", "email": "rh107", "class_year": 2027, "dob": "10/05/2004", "bio": "I like to think of myself as extremely mediocre."}]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/main")
def main():
    return render_template("main.html", users=users)
            
@app.route("/new-user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return render_template("new_user.html")
    name = request.form['name']
    email = request.form['email']
    class_year = request.form["classYear"]
    dob = request.form["dob"]
    bio = request.form.get("bio", "")
    user = {"name":name, "email":email, "class_year":class_year, "dob":dob, "bio":bio}
    users.append(user)
    # TODO:save to your database here
    return redirect(url_for("user"))
    # return redirect(url_for("user.html", user=user))

@app.route("/new-event")
def new_event():
    return render_template("new_event.html")

@app.route("/event")
def event():
    return render_template("event.html")

@app.route("/user/")
def user():
    return render_template("user.html", user=user)

# @app.route("/user", methods=["POST"])
# def user():
#     return render_template("user.html",user=users[0])#dictionary using user ID




if __name__ == '__main__':
    import os
    uid = os.getuid()
    app.debug = True
    app.run('0.0.0.0',uid)