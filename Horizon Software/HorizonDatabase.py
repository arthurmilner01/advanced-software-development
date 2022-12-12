from DatabaseAccess import * 

cur = getCursor()
conn = getConn()



# Dropping tables if they exist
cur.execute('''
DROP TABLE if exists BookingStaff
''')

cur.execute('''
DROP TABLE if exists Admin
''')

cur.execute('''
DROP TABLE if exists Manager
''')

cur.execute('''
DROP TABLE if exists Bookings
''')

cur.execute('''
DROP TABLE if exists Films
''')

cur.execute('''
DROP TABLE if exists FilmScreenings
''')



# Creating tables
cur.execute('''
CREATE TABLE BookingStaff
(email varchar(120) PRIMARY KEY, password varchar(120) NOT NULL, cinema_name varchar(120) NOT NULL)
''')

cur.execute('''
CREATE TABLE Admin
(email varchar(120) PRIMARY KEY, password varchar(120) NOT NULL)
''')

cur.execute('''
CREATE TABLE Manager
(email varchar(120) PRIMARY KEY, password varchar(120) NOT NULL)
''')

cur.execute('''
CREATE TABLE Bookings
(bookingID INTEGER PRIMARY KEY, seat_type varchar(20) NOT NULL, seat_numbers varchar(50) NOT NULL, 
price REAL NOT NULL, customer_name varchar(120) NOT NULL, customer_email varchar(120) NOT NULL, 
customer_phone INTEGER NOT NULL, number_of_tickets INTEGER NOT NULL)
''')

cur.execute('''
CREATE TABLE Films
(filmID INTEGER PRIMARY KEY, film_name varchar(120) NOT NULL, film_description varchar(120) NOT NULL, 
film_actors varchar(120) NOT NULL, film_genre varchar(120) NOT NULL, film_age INTEGER NOT NULL, film_rating REAL NOT NULL)
''')

cur.execute('''
CREATE TABLE FilmScreenings
(screeningID INTEGER PRIMARY KEY, screening_time varchar(120) NOT NULL, screening_screen INTEGER NOT NULL, film_name varchar(120) NOT NULL, 
lower_hall_tickets_left INTEGER NOT NULL, upper_hall_tickets_left INTEGER NOT NULL, VIP_tickets_left INTEGER NOT NULL)
''')

