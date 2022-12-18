from DatabaseAccess import * 

cur = getCursor()
conn = getConn()



# Dropping tables if they exist
cur.execute('''
DROP TABLE if exists Users
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

cur.execute('''
DROP TABLE if exists CinemaScreens
''')

cur.execute('''
DROP TABLE if exists Cinemas
''')

cur.execute('''
DROP TABLE if exists Cities
''')



# Creating tables
cur.execute('''
CREATE TABLE Users
(userID INTEGER PRIMARY KEY, email varchar(120) UNIQUE, password varchar(120) NOT NULL, user_type INT NOT NULL)
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

cur.execute('''
CREATE TABLE CinemaScreens
(cinema_screenID INTEGER PRIMARY KEY, lower_hall_capacity INTEGER, upper_hall_capacity INTEGER, VIP_capacity INTEGER)
''')

cur.execute('''
CREATE TABLE Cinemas
(cinemaID INTEGER PRIMARY KEY, cinema_name varchar(120), city_name varchar(120))
''')

cur.execute('''
CREATE TABLE Cities
(cityID INTERGER PRIMARY KEY, city_name varchar(120), morning_price REAL, afternoon_price REAL, evening_price REAL)
''')

# Insert mock data
cur.execute('''
INSERT INTO Users(email, password, user_type)
VALUES ('arthur@gmail.com', '12345', 0)
''')

conn.commit()