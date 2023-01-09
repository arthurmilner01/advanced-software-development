#Arthur Milner 21035478
#Joseph Cauvy-Foster 21031786
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
(userID INTEGER PRIMARY KEY, email varchar(120) UNIQUE, password varchar(120) NOT NULL, user_type INT NOT NULL, user_cinema varchar(120))
''')

cur.execute('''
CREATE TABLE Bookings
(bookingID INTEGER PRIMARY KEY, seat_type varchar(20) NOT NULL, seat_numbers varchar(50) NOT NULL, 
price REAL NOT NULL, number_of_tickets INTEGER NOT NULL, screeningID INTEGER NOT NULL)
''')

cur.execute('''
CREATE TABLE Films
(filmID INTEGER PRIMARY KEY, film_name varchar(120) NOT NULL, film_description varchar(120) NOT NULL, 
film_actors varchar(120) NOT NULL, film_genre varchar(120) NOT NULL, film_age INTEGER NOT NULL, film_rating REAL NOT NULL)
''')

cur.execute('''
CREATE TABLE FilmScreenings
(screeningID INTEGER PRIMARY KEY, screening_time varchar(120) NOT NULL, screening_date varchar(120) NOT NULL, screening_screen INTEGER NOT NULL, cinema_name varchar(120) NOT NULL, film_name varchar(120) NOT NULL, 
lower_hall_tickets_left INTEGER NOT NULL DEFAULT '30', upper_hall_tickets_left INTEGER NOT NULL DEFAULT '60', VIP_tickets_left INTEGER NOT NULL DEFAULT '10')
''')

cur.execute('''
CREATE TABLE CinemaScreens
(cinema_screenID INTEGER PRIMARY KEY, cinema_name varchar(120), lower_hall_capacity INTEGER DEFAULT '30', upper_hall_capacity INTEGER DEFAULT '60', VIP_capacity INTEGER DEFAULT '10')
''')

cur.execute('''
CREATE TABLE Cinemas
(cinemaID INTEGER PRIMARY KEY, cinema_name varchar(120) UNIQUE, city_name varchar(120))
''')

cur.execute('''
CREATE TABLE Cities
(cityID INTEGER PRIMARY KEY, city_name varchar(120), morning_price REAL, afternoon_price REAL, evening_price REAL)
''')

# Insert booking staff account
cur.execute('''
INSERT INTO Users(email, password, user_type, user_cinema)
VALUES ('arthur@gmail.com', '12345', 0, 'Cabot Circus')
''')
# Insert admin account
cur.execute('''
INSERT INTO Users(email, password, user_type)
VALUES ('henry@gmail.com', 'hello', 1)
''')
#Insert manager account
cur.execute('''
INSERT INTO Users(email, password, user_type)
VALUES ('milner@gmail.com', 'bye12', 2)
''')
#Insert film data
cur.execute('''
INSERT INTO Films(film_name, film_description, film_actors, film_genre, film_age, film_rating)
VALUES ('Avengers', 'Avengers fight crime.', 'Robert Downey Jr., Chris Evans and More', 'Superhero', 18, 7.6),
('UP', 'balloon on the house', 'Old man and Kid and Dog', 'Family adventure', 7, 10),
('The Menu', 'Flim about food', 'Anya Taylor Joy, Ralph Fienes and More', 'Horror', 18, 7.2)
''')
#Insert cities
cur.execute('''
INSERT INTO Cities(city_name, morning_price, afternoon_price, evening_price)
VALUES ('Bristol', 6.00, 7.00, 8.00),
('Birmingham', 5.00, 6.00, 7.00),
('Cardiff', 5.00, 6.00, 7.00),
('London', 10.00, 11.00, 12.00)
''')
#Insert cinemas
cur.execute('''
INSERT INTO Cinemas(cinema_name, city_name)
VALUES ('Cabot Circus', 'Bristol'),
('Cribbs Causeway', 'Bristol'),
('Bullring', 'Birmingham'),
('Solihul', 'Birmingham'),
('Canton', 'Cardiff'),
('Cathays', 'Cardiff'),
('Stratford', 'London'),
('Waterloo', 'London')
''')
#Create 6 cinema screens for each cinema, up to 6
cur.execute('''
INSERT INTO CinemaScreens(cinema_name)
VALUES ('Cabot Circus'),
('Cabot Circus'),
('Cabot Circus'),
('Cabot Circus'),
('Cabot Circus'),
('Cabot Circus'),
('Cribbs Causeway'),
('Cribbs Causeway'),
('Cribbs Causeway'),
('Cribbs Causeway'),
('Cribbs Causeway'),
('Cribbs Causeway'),
('Bullring'),
('Bullring'),
('Bullring'),
('Bullring'),
('Bullring'),
('Bullring'),
('Solihul'),
('Solihul'),
('Solihul'),
('Solihul'),
('Solihul'),
('Solihul'),
('Canton'),
('Canton'),
('Canton'),
('Canton'),
('Canton'),
('Canton'),
('Cathays'),
('Cathays'),
('Cathays'),
('Cathays'),
('Cathays'),
('Cathays'),
('Stratford'),
('Stratford'),
('Stratford'),
('Stratford'),
('Stratford'),
('Stratford'),
('Waterloo'),
('Waterloo'),
('Waterloo'),
('Waterloo'),
('Waterloo'),
('Waterloo')
''')
#Insert some random film screenings
cur.execute('''
INSERT INTO FilmScreenings(screening_time, screening_date, screening_screen, cinema_name, film_name)
VALUES ('15:00', '20/01/2023', 1, 'Cabot Circus', 'Avengers'),
('19:00', '20/01/2023', 13, 'Bullring', 'Avengers'),
('19:00', '20/01/2023', 1, 'Cabot Circus', 'UP'),
('15:00', '21/01/2023', 40, 'Stratford', 'The Menu'),
('10:00', '20/01/2023', 33, 'Cathays', 'Avengers'),
('10:00', '21/01/2023', 33, 'Cathays', 'Avengers'),
('15:00', '21/01/2023', 33, 'Cathays', 'Avengers'),
('10:00', '21/01/2023', 31, 'Cathays', 'The Menu')
''')


conn.commit()