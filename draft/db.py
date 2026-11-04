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

def insert_event(event):
    '''Use event dict to insert into event table, return eid and redirect to event.html'''
    return

def insert_comment():
    return

def insert_response():
    return




