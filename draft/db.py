import pymysql
conn = pymysql.connect(read_default_file='~/.my.cnf', database='squest_db')


def insert_user(user):
    '''Use user dict to insert into user table, might need separate function for deaing w passwords
    this function should return the uid to then redirect to user.html, add cookie to session'''
    with conn.cursor(pymysql.cursors.DictCursor) as curs:
        try:
            curs.execute('''INSERT INTO user(name, class, bio, dob, email, password)
                        VALUES (%s, %s, %s, %s, %s, %s)''', [user['name'], ])
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
    with conn.cursor(pymysql.cursor.DictCursor) as curs:
        try:
            curse.execute(
                '''INSERT INTO (event_name, event_type, city, date, meeting_point, description, attachment, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', [event['name'], ])
            conn.commit()
            eid = curs.lastrowid
            return eid
        except pymysql.err.IntegrityError as err:
            details = err.args
            print('error',details)

    
def insert_comment():
    return

def insert_response():
    return

