import re
from DatabaseAccess import *

conn = getConn()
cur = getCursor()

class LoginModel:
    def __init__(self):
        self.__email = ""
        self.__password = ""

    def getEmail(self):
        return self.__email

    def getPassword(self):
        return self.__password

    def setEmail(self, email):
        if self.validateEmailSyntax(email):
            self.__email = email
            return 1
        else:
            return 0

    def setPassword(self, password):
        if self.validatePasswordSyntax(password):
            self.__password = password
            return 1
        else:
            return 0

    def validateEmailSyntax(self, email):
        if len(email) > 0:
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(pattern, email):
                return 1
            else:
                return 0
        else: 
            return 0

    def validatePasswordSyntax(self, password):
        if len(password) > 0:
            pattern = r'[A-Za-z0-9 ]{5,}'
            if re.fullmatch(pattern, password):
                return 1
            else:
                return 0
        else:
            return 0

    def checkAccountInDB(self, email, password):
        query = 'SELECT email, password FROM Users WHERE email = ? AND password = ?'
        cur.execute(query, (email, password))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account found")
            return 1
        else:
            print("Account not found")
            return 0

    def getAccountUserType(self, email, password):
        query = 'SELECT user_type FROM Users WHERE email = ? AND password = ?'
        cur.execute(query, (email, password))
        record = cur.fetchone()
        userType = int(''.join(map(str, record)))
        print(userType)
        return userType
    
    def getAccountCinema(self, email, password):
        query = 'SELECT user_cinema FROM Users WHERE email = ? AND password = ?'
        cur.execute(query, (email, password))
        record = cur.fetchone()
        if record != None:
            userCinema = ''.join(map(str, record))
            print(userCinema)
            return userCinema
        else:
            userCinema = None
            return userCinema

class ViewFilmListingsModel:
    def __init__(self):
        self.__filmName = ""
        self.__cinemaName = ""

    def validateFilmNameSyntax(self, filmName):
        if len(filmName) > 0:
            pattern = r'[A-Za-z0-9 ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, filmName):
                return 1
            else:
                return 0
        else:
            return 0
    
    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            pattern = r'[A-Za-z ]{0,50}' #Letters and up to 50 char
            if re.fullmatch(pattern, cinemaName):
                return 1
            else:
                return 0
        else:
            return 0

    def checkForScreenings(self, filmName, cinemaName):
        query = 'SELECT film_name, cinema_name FROM FilmScreenings WHERE film_name = ? AND cinema_name = ?'
        cur.execute(query, (filmName, cinemaName))
        record = cur.fetchall()
        if len(record) > 0:
            print("Screenings found.")
            return 1
        else:
            print("Screenings not found.")
            return 0

    def returnScreeningsInfo(self, filmName, cinemaName):
        query = 'SELECT screening_time, screening_date, screening_screen FROM FilmScreenings WHERE film_name = ? AND cinema_name = ? ORDER BY screening_date, screening_time ASC'
        cur.execute(query, (filmName, cinemaName))
        screeningsInfo = cur.fetchall()
        print(screeningsInfo)
        return screeningsInfo

