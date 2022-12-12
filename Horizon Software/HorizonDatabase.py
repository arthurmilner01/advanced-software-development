from DatabaseAccess import * 

cur = getCursor()
conn = getConn()

cur.execute('''
DROP TABLE if exists BookingStaff
''')

cur.execute('''
CREATE TABLE BookingStaff
(email varchar(120) PRIMARY KEY, password varchar(120) NOT NULL, cinema_name varchar(120) NOT NULL)
''')
