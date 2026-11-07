#
import pymysql
from pwd_context import hash_password
conn = pymysql.connect(read_default_file='~/.my.cnf', database='squest_db')


def insert_user(user):
    '''Use user dict to insert into user table, might need separate function for deaing w passwords
    this function should return the uid to then redirect to user.html, add cookie to session'''
    hashed = hash_password(user['password'])

    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        try:
            curs.execute('''INSERT INTO user(name, class, bio, dob, email, password)
                        VALUES (%s, %s, %s, %s, %s, %s)''', 
                        [user['name'], user['class'],  user['bio'],
                         user['dob'], user['email'], hashed])
            conn.commit()
            uid = curs.lastrowid
            return uid
        except pymysql.err.IntegrityError as err:
            details = err.args
            print('error',details)
            if details[0] == pymysql.constants.ER.DUP_ENTRY:
                print(f'duplicate key for username {user['email']}')
            else:
                print('some other error!')
            # return None on any error
            return None

def insert_event(event, uid):
    '''Use event dict to insert into event table, return eid and redirect to event.html'''
    with conn.cursor(pymysql.cursor.DictCursor) as curs:
        try:
            curse.execute(
                '''INSERT INTO (uid, event_name, event_type, city, date, meeting_point, description, attachment, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', [ uid, event['event_name'],event['event_type'], event['city'],
                event['date'], event['meeting_point'], event['description'], event['attachment'], event['price']])
            conn.commit()
            eid = curs.lastrowid
            return eid
        except pymysql.err.IntegrityError as err:
            details = err.args
            print('error',details)

def insert_comment(comment):
    '''Use comment dict to insert a comment into the comment table, return cid and 
        redirect to event.html'''
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute('''INSERT INTO comment(uid, eid, response)
            VALUES (%s, %s, %s, %s)''', [comment['uid'], comment['eid'], comment['comment']])
        conn.commit()


def insert_response(response):
    '''Use response dict to insert a response into the response table, return rid and 
    redirect to event.html'''
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute('''INSERT INTO response(uid, eid, cid, response)
            VALUES (%s, %s, %s, %s)''', [response['uid'], response['eid'], response['cid'],
                                          response['response']])
        conn.commit()

def insert_rsvp(rsvp):
    '''Use rsvp dict to insert a response into the rsvp table, return status and 
    redirect to event.html'''
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute('''INSERT INTO rsvp(uid, eid, status)
            VALUES (%s, %s, %s)''', [rsvp['uid'], rsvp['eid'], rsvp['status']])
        conn.commit()
    

def find_user(uid):
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        curs.execute('''SELECT name, class, bio, dob, email
                        FROM user
                        WHERE uid = %s;''', [uid])
        user = curs.fetchone()
        return user 


