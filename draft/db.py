#
import pymysql
from pwd_context import hash_password


def insert_user(user, conn):
    """Use user dict to insert into user table, might need separate function for deaing w passwords
    this function should return the uid to then redirect to user.html, add cookie to session
    """
    hashed = hash_password(user["password"])

    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        # is there another way to check if a username already exists to not cause the auto
        # incrementer to trigger?
        try:
            curs.execute(
                """INSERT INTO user(name, class, bio, dob, email, password)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                [
                    user["name"],
                    user["class"],
                    user["bio"],
                    user["dob"],
                    user["email"],
                    hashed,
                ],
            )
            conn.commit()
            uid = curs.lastrowid
            return uid
        except pymysql.err.IntegrityError as err:
            details = err.args
            print("error", details)
            if details[0] == pymysql.constants.ER.DUP_ENTRY:
                print(f"duplicate key for username {user['email']}")
            else:
                print("some other error!")
            # return None on any error
            return None


def insert_event(event, uid, conn):
    """Use event dict to insert into event table, return eid and redirect to event.html"""
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        price = event.get("price", 0) or 0
        attachment = event.get("attachment", None)
        event_type = ",".join(event.getlist('event_type'))
        curs.execute(
            """INSERT INTO event(uid, event_name, event_type, city, date, meeting_point, description, attachment, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            [
                uid,
                event["event_name"],
                event_type,
                event["city"],
                event["date"],
                event["meeting_point"],
                event["description"],
                attachment,
                price,
            ],
        )
        conn.commit()
        eid = curs.lastrowid
        return eid


def insert_comment(comment, conn):
    """Use comment dict to insert a comment into the comment table, return cid and
    redirect to event.html"""
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """INSERT INTO comment(uid, eid, response)
            VALUES (%s, %s, %s, %s)""",
            [comment["uid"], comment["eid"], comment["comment"]],
        )
        conn.commit()


def insert_response(response, conn):
    """Use response dict to insert a response into the response table, return rid and
    redirect to event.html"""
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """INSERT INTO response(uid, eid, cid, response)
            VALUES (%s, %s, %s, %s)""",
            [response["uid"], response["eid"], response["cid"], response["response"]],
        )
        conn.commit()


def insert_rsvp(rsvp, conn):
    """Use rsvp dict to insert a response into the rsvp table, return status and
    redirect to event.html"""
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """INSERT INTO rsvp(uid, eid, status)
            VALUES (%s, %s, %s)""",
            [rsvp["uid"], rsvp["eid"], rsvp["status"]],
        )
        conn.commit()


def login_user(email, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT uid, password
                        FROM user
                        WHERE email = %s;""",
            [email],
        )
        user = curs.fetchone()
        return user


def find_user(uid, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT uid, name, class, bio, dob, email
                        FROM user
                        WHERE uid = %s;""",
            [uid],
        )
        user = curs.fetchone()
        return user


def find_event(eid, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT uid, name, event_name, event_type, city, date, meeting_point, description, attachment, price
                        FROM event
                        INNER JOIN user USING (uid)
                        WHERE eid = %s;""",
            [eid],
        )
        event = curs.fetchone()
        return event


def find_comments(eid, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT cid, name, comment
                        FROM comment
                        INNER JOIN user USING (uid)
                        WHERE eid = %s;""",
            [eid],
        )
        comments = curs.fetchall()
        return comments



def find_responses(cid, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT name, response
                        FROM response
                        INNER JOIN user USING (uid)
                        WHERE cid = %s;""",
            [cid],
        )
        responses = curs.fetchall()
        return responses

def update_user(uid, user, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """UPDATE user SET name = %s,
                        class = %s,
                        bio = %s,
                        dob = %s
                        WHERE uid = %s;""",
               [user["name"],
                user["class"],
                user["bio"],
                user["dob"], 
                uid],
        )
        conn.commit()
        curs.execute(
            """SELECT uid, name, class, bio, dob, email
                        FROM user
                        WHERE uid = %s;""",
            [uid],
        )
    return curs.fetchone()

def search_events(pattern, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT uid, name, eid, event_name, event_type, city, date, meeting_point, description, attachment, price
                        FROM event
                        INNER JOIN user USING (uid)
                        WHERE event_name LIKE %s;""",
            [pattern],
        )
        events = curs.fetchall()
        return events

def month_events(conn):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute(
            """SELECT uid, name, eid, event_name, event_type, city, date, meeting_point, description, attachment, price
                        FROM event
                        INNER JOIN user USING (uid)
                        WHERE MONTH(date) = MONTH(CURDATE()) 
                        AND YEAR(date) = YEAR(CURDATE());"""
        )
        events = curs.fetchall()
        return events