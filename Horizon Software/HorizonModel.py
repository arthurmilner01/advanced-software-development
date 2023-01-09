#Arthur Milner 21035478
#Joseph Cauvy-Foster 21031786
import re
from DatabaseAccess import *
from datetime import *
from datetime import datetime
import time

conn = getConn()
cur = getCursor()

class HomeModel:
    def __init__(self):
        pass

    def getCinemas(self):
        cur.execute("SELECT cinema_name FROM Cinemas")
        cinemas = cur.fetchall()
        return cinemas


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
        
    def getFilms(self, cinemaName):
        query = 'SELECT DISTINCT film_name FROM FilmScreenings WHERE cinema_name = ?'
        cur.execute(query, (cinemaName,))
        films = cur.fetchall()
        print(films)
        return films

    def returnScreeningsInfo(self, filmName, cinemaName):
        query = 'SELECT screening_time, screening_date, screening_screen FROM FilmScreenings WHERE film_name = ? AND cinema_name = ? ORDER BY screening_date, screening_time ASC'
        cur.execute(query, (filmName, cinemaName))
        screeningsInfo = cur.fetchall()
        print(screeningsInfo)
        return screeningsInfo

class CreateBookingModel:
    def __init__(self):
        self.__seatType = ""
        self.__seatNumbers = ""
        self.__customerName = ""
        self.__cinemaName = ""
    
    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            print("yes")
            pattern = r'[A-Za-z ]{0,50}' #Letters and up to 50 char
            if re.fullmatch(pattern, cinemaName):
                return 1
            else:
                return 0
        else:
            return 0
    
    def validateFilmNameSyntax(self, filmName):
        if len(filmName) > 0:
            pattern = r'[A-Za-z0-9 ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, filmName):
                return 1
            else:
                return 0
        else:
            return 0
   
    def checkForFilms(self, cinemaName):
        query = 'SELECT DISTINCT film_name FROM FilmScreenings WHERE cinema_name = ?'
        cur.execute(query, (cinemaName,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Films found.")
            return 1
        else:
            print("Films not found.")
            return 0

    #function to return a fetch of all films in a given cinema to be put in combobox   
    def returnFilms(self, cinemaName):
        query = 'SELECT DISTINCT film_name FROM FilmScreenings WHERE cinema_name = ?'
        cur.execute(query, (cinemaName,)) #NOTE: have to have the execute layed out like this when only using 1 parameter
        films = cur.fetchall()            # very wierd but have to have (cinemaName, ) and not just cinemaName
        return films
    
    def checkForDates(self, filmName, cinemaName):
        query = 'SELECT screening_date FROM FilmScreenings WHERE film_name = ? AND cinema_name = ?'
        cur.execute(query, (filmName,cinemaName))
        record = cur.fetchall()
        if len(record) > 0:
            print('Dates found.')
            return 1
        else:
            print('No dates found.')
            return 0
        
    def returnDates(self, filmName, cinemaName):
        query = 'SELECT DISTINCT screening_date FROM FilmScreenings WHERE film_name = ? AND cinema_name = ?'
        cur.execute(query, (filmName,cinemaName)) 
        dates = cur.fetchall()
        return dates
    
    def checkForShowings(self, filmDate, filmName, cinemaName):
        query = 'SELECT screening_time FROM FilmScreenings WHERE film_name = ? AND cinema_name = ? AND screening_date = ?'
        cur.execute(query, (filmName, cinemaName, filmDate))
        records = cur.fetchall()
        if len(records) > 0:
            print('Showings found.')
            return 1
        else:
            print('No showings found')
            return 0
    
    def returnShowings(self, filmDate, filmName, cinemaName):
        query = 'SELECT DISTINCT screening_time FROM FilmScreenings WHERE film_name = ? AND cinema_name = ? AND screening_date = ?'
        cur.execute(query, (filmName, cinemaName, filmDate))
        showings = cur.fetchall()
        return showings

    def checkForTickets(self, showing, filmDate, filmName, cinemaName):
        query = 'SELECT lower_hall_tickets_left, upper_hall_tickets_left, VIP_tickets_left FROM FilmScreenings WHERE screening_time = ? AND film_name = ? AND cinema_name = ? AND screening_date = ?'
        cur.execute(query, (showing, filmName, cinemaName, filmDate))
        records = cur.fetchall()
        if len(records) > 0:
            print('Tickets found.')
            return 1
        else:
            print('No tickets found.')
            return 0
        
    def returnTickets(self, showing, filmDate, filmName, cinemaName):
        query = 'SELECT lower_hall_tickets_left, upper_hall_tickets_left, VIP_tickets_left FROM FilmScreenings WHERE screening_time = ? AND film_name = ? AND cinema_name = ? AND screening_date = ?'
        cur.execute(query, (showing, filmName, cinemaName, filmDate))
        tickets = cur.fetchall()
        return tickets
    
    def getPrices(self, cinemaName):
        query = 'SELECT city_name FROM Cinemas WHERE cinema_name = ?'
        cur.execute(query, (cinemaName, ))
        city = cur.fetchone()
        query = 'SELECT morning_price, afternoon_price, evening_price FROM Cities WHERE city_name = ?'
        cur.execute(query, (city[0], ))
        prices = cur.fetchone()
        return prices

    def getScreeningID(self, time, date, name, cinema):
        query = 'SELECT screeningID FROM FilmScreenings WHERE screening_time = ? AND screening_date = ? AND film_name = ? AND cinema_name = ?'
        cur.execute(query, (time, date, name, cinema))
        screeningID = cur.fetchone()
        return screeningID[0]

    def createBooking(self, bookingID, seatType, seatNums, price, numOfTickets, screeningID):
        cur.execute("SELECT bookingID FROM Bookings")
        bookings = cur.fetchall()
        query = '''INSERT INTO Bookings (bookingID, seat_type, seat_numbers, price, number_of_tickets, screeningID)
        VALUES (?, ?, ? ,?, ?, ?)'''
        cur.execute(query, (bookingID, seatType, seatNums, price, numOfTickets, screeningID))
        cur.execute("SELECT bookingID FROM Bookings")
        bookings1 = cur.fetchall()
        if len(bookings1) - len(bookings) == 1:
            print("booking added to database")
            #removing seats booked from database
            if seatType == 1:
                query = "SELECT lower_hall_tickets_left FROM FilmScreenings WHERE screeningID = ?"
                cur.execute(query, (screeningID,))
                tickets = cur.fetchone()
                ticketsRemaining = tickets[0] - numOfTickets
                query = "UPDATE FilmScreenings SET lower_hall_tickets_left = ? WHERE screeningID = ? "
                cur.execute(query, (ticketsRemaining, screeningID))
                conn.commit()
            if seatType == 2:
                query = "SELECT upper_hall_tickets_left FROM FilmScreenings WHERE screeningID = ?"
                cur.execute(query, (screeningID,))
                tickets = cur.fetchone()
                ticketsRemaining = tickets[0] - numOfTickets
                query = "UPDATE FilmScreenings SET upper_hall_tickets_left = ? WHERE screeningID = ? "
                cur.execute(query, (ticketsRemaining, screeningID))
                conn.commit()
            if seatType == 3:
                query = "SELECT VIP_tickets_left FROM FilmScreenings WHERE screeningID = ?"
                cur.execute(query, (screeningID,))
                tickets = cur.fetchone()
                ticketsRemaining = tickets[0] - numOfTickets
                query = "UPDATE FilmScreenings SET VIP_tickets_left = ? WHERE screeningID = ? "
                cur.execute(query, (ticketsRemaining, screeningID))
                conn.commit()
            return 1
        else:
            return 0
        
    def getScreeningScreen(self, screeningID):
        query = "SELECT screening_screen FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        screeningScreen = cur.fetchone()
        return screeningScreen[0]

    def getBookingIDs(self):
        cur.execute("SELECT bookingID FROM Bookings")
        bookingIDs = cur.fetchall()
        return bookingIDs

class GenerateReportModel:
    def __init__(self):
        self.__reportType = ""
        self.__reportParameter = ""

    def validateReportTypeSyntax(self, reportType):
        if len(reportType) > 0:
            pattern = r'[1-3]' #Numbers, up to 3, increase if you wish to have more reports
            if re.fullmatch(pattern, reportType):
                return 1
            else:
                return 0
        else:
            return 0

    def validateReportParameterSyntax(self, reportType, reportParameter):
        if reportType == "3" and len(reportParameter) == 0:
            return 1
        if len(reportParameter) > 0 and reportType != "3":
            if reportType == "1":
                query = "SELECT * FROM Cinemas WHERE cinema_name = ?"
                cur.execute(query, (reportParameter,))
                result = cur.fetchall()
                if len(result) > 0:
                    return 1
                else:
                    return 0
            if reportType == "2":
                query = "SELECT * FROM FilmScreenings WHERE screeningID = ?"
                cur.execute(query, (reportParameter,))
                result = cur.fetchall()
                if len(result) > 0:
                    return 1
                else:
                    return 0
        else:
            return 0

    def checkReportReturnsInfo(self, reportType, reportParameter):
        if reportType == "1":
            print("Report type 1")
            query = "SELECT * FROM Users WHERE user_cinema = ?"
            cur.execute(query, (reportParameter, ))
            result = cur.fetchall()
            print(result)
            if len(result) > 0:
                print("Results found.")
                return 1
            else:
                return 0
        if reportType == "2":
            #Getting all bookings for given screening ID to check if any bookings have been made
            print("Report type 2")
            query = "SELECT * FROM Bookings WHERE screeningID = ?"
            cur.execute(query, (reportParameter, ))
            result = cur.fetchall()
            print(result)
            if len(result) > 0:
                print("Found results.")
                return 1
            else:
                return 0
        if reportType == "3":
            print("Report type 3")
            query = "SELECT * FROM Bookings"
            cur.execute(query)
            result = cur.fetchall()
            if len(result) > 0:
                print("Found results.")
                return 1
            else:
                return 0
    
    def returnReportInfo(self, reportType, reportParameter):
        if reportType == "1":
            #Get the staff email for all staff under a given cinema name
            query = "SELECT email, user_cinema FROM Users WHERE user_cinema = ?"
            cur.execute(query, (reportParameter, ))
            reportInfo = cur.fetchall()
            return reportInfo
        if reportType == "2":
            #Getting the count of bookings under a given screening ID
            query = "SELECT screeningID, COUNT(*) FROM Bookings WHERE screeningID = ?"
            cur.execute(query, (reportParameter, ))
            reportInfo = cur.fetchall()
            return reportInfo
        if reportType == "3":
            #Get the number of bookings for films
            query = """SELECT FilmScreenings.film_name, COUNT(Bookings.screeningID)
                        FROM FilmScreenings INNER JOIN Bookings ON Bookings.screeningID = FilmScreenings.screeningID"""
            cur.execute(query)
            reportInfo = cur.fetchall()
            return reportInfo




class CancelBookingModel():
    def checkBookingID(self, bookingID):
        query = "SELECT * FROM Bookings WHERE bookingID = ?"
        cur.execute(query, (bookingID,))
        records = cur.fetchall()
        if len(records) > 0:
            return 1
        else: 
            return 0

    def checkCancelTime(self, screeningID):
        query = "SELECT screening_date FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        dates = cur.fetchone()
        holder = date.today()
        today = holder.strftime("%d/%m/%Y")
        today = datetime.strptime(today, "%d/%m/%Y")
        bookingDate = datetime.strptime(dates[0], "%d/%m/%Y")
        difference = bookingDate - today
        if int(difference.days) >= 1:
            return 1
        else:
            return 0
    
    def getBooking(self, bookingID):
        query = "SELECT * FROM Bookings WHERE bookingID = ?"
        cur.execute(query, (bookingID,))
        bookingInfo = cur.fetchone()
        return bookingInfo

    def removeBooking(self, bookingID):
        query = "SELECT * FROM Bookings WHERE bookingID = ?"
        cur.execute(query, (bookingID,))
        bookingsBefore = cur.fetchall()
        query = "DELETE FROM Bookings WHERE bookingID = ?"
        cur.execute(query, (bookingID,))
        conn.commit()
        query = "SELECT * FROM Bookings WHERE bookingID = ?"
        cur.execute(query, (bookingID,))
        bookingsAfter = cur.fetchall()
        if  len(bookingsBefore) - len(bookingsAfter) == 1:
            return 1
        else: 
            return 0

    def updateTickets(self, numOfTickets, seatType, screeningID):
        if seatType == "1":
            query = "SELECT lower_hall_tickets_left FROM FilmScreenings WHERE screeningID = ?"
            cur.execute(query, (screeningID,))
            tickets = cur.fetchone()
            ticketsRemaining = tickets[0] + numOfTickets
            query = "UPDATE FilmScreenings SET lower_hall_tickets_left = ? WHERE screeningID = ? "
            cur.execute(query, (ticketsRemaining, screeningID))
            conn.commit()
            return 1
        elif seatType == "2":
            query = "SELECT upper_hall_tickets_left FROM FilmScreenings WHERE screeningID = ?"
            cur.execute(query, (screeningID,))
            tickets = cur.fetchone()
            ticketsRemaining = tickets[0] + numOfTickets
            query = "UPDATE FilmScreenings SET upper_hall_tickets_left = ? WHERE screeningID = ? "
            cur.execute(query, (ticketsRemaining, screeningID))
            conn.commit()
            return 1
        elif seatType == "3":
            query = "SELECT VIP_tickets_left FROM FilmScreenings WHERE screeningID = ?"
            cur.execute(query, (screeningID,))
            tickets = cur.fetchone()
            ticketsRemaining = tickets[0] + numOfTickets
            query = "UPDATE FilmScreenings SET VIP_tickets_left = ? WHERE screeningID = ? "
            cur.execute(query, (ticketsRemaining, screeningID))
            conn.commit()
            return 1
        else:
            return 0


class ViewFilmModel:
    def __init__(self):
        pass

    def validateFilmNameSyntax(self, filmName):
        if len(filmName) > 0:
            pattern = r'[A-Za-z0-9,.\& ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, filmName):
                return 1
            else:
                return 0
        else:
            return 0
        
    def validateFilmAgeSyntax(self, filmAge):
        if len(filmAge) > 0 and len(filmAge) <= 2:
            pattern = r'[0-9 ]{0,2}' #numbers and up to 2 char
            if re.fullmatch(pattern, filmAge):
                return 1
            else:
                return 0
        else:
            return 0
        
    def validateFilmRatingSyntax(self, filmName):
        if len(filmName) > 0:
            pattern = r'-?\d+(?:\.\d+)?' #floating point 
            if re.fullmatch(pattern, filmName):
                return 1
            else:
                return 0
        else:
            return 0
        
    def addFilm(self, filmName, filmDescription, filmActors, filmGenre, filmAge, filmRating):
        cur.execute("SELECT * FROM Films")
        filmsBefore = cur.fetchall()
        query = "INSERT INTO Films(film_name, film_description, film_actors, film_genre, film_age, film_rating) VALUES (?,?,?,?,?,?)"
        cur.execute(query, (filmName, filmDescription, filmActors, filmGenre, filmAge, filmRating))
        conn.commit()
        cur.execute("SELECT * FROM Films")
        filmsAfter = cur.fetchall()
        print(filmsAfter)
        if len(filmsAfter) - len(filmsBefore) == 1:
            return 1
        else:
            return 0

    def checkFilmID(self, filmID):
        query = "SELECT * FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        records = cur.fetchall()
        if len(records) > 0:
            return 1
        else:
            return 0
    def getFilmName(self, filmID):
        query = "SELECT film_name FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        filmName = cur.fetchone()
        return filmName[0]

    def deleteFilm(self, filmID):
        query = "SELECT * FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        filmsBefore = cur.fetchall()
        query = "DELETE FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        conn.commit()
        query = "SELECT * FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        filmsAfter = cur.fetchall()
        if len(filmsBefore) - len(filmsAfter) > 0:
            return 1
        else:
            return 0
        
    def deleteShowings(self, filmName):
        query = "SELECT * FROM FilmScreenings WHERE film_name = ?"
        cur.execute(query, (filmName,))
        showingsBefore = cur.fetchall()
        query = "DELETE FROM FilmScreenings WHERE film_name = ?"
        cur.execute(query, (filmName,))
        conn.commit()
        query = "SELECT * FROM FilmScreenings WHERE film_name = ?"
        cur.execute(query, (filmName,))
        showingsAfter = cur.fetchall()
        if len(showingsBefore) == 0:
            return 1
        if len(showingsBefore) - len(showingsAfter) > 0:
            return 1
        else:
            return 0
        
    def checkFilmName(self, filmName):
        query = 'SELECT * FROM Films WHERE film_name = ?'
        cur.execute(query, (filmName,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Film found.")
            return 1
        else:
            print("Film not found.")
            return 0
        
    def getFilm(self, filmName):
        query = 'SELECT * FROM Films WHERE film_name = ?'
        cur.execute(query, (filmName,))
        film = cur.fetchone()
        return film
    
    def getFilmInfo(self, filmID):
        query = 'SELECT film_name, film_description, film_actors, film_genre, film_age, film_rating FROM Films WHERE filmID = ?'
        cur.execute(query, (filmID,))
        film = cur.fetchone()
        return film
    
    def updateFilm(self, filmID, updateList):
        query = 'UPDATE Films SET film_name = ?, film_description = ?, film_actors = ?, film_genre = ?, film_age = ?, film_rating = ? WHERE filmID = ?'
        cur.execute(query, (updateList[0], updateList[1], updateList[2], updateList[3], updateList[4], updateList[5], filmID))
        conn.commit()
        query = "SELECT * FROM Films WHERE filmID = ?"
        cur.execute(query, (filmID,))
        film = cur.fetchone()
        print("film: "+str(film))
    
    def updateScreenings(self, filmName, oldFilmName):
        query = 'UPDATE FilmScreenings SET film_name = ? WHERE film_name = ?'
        cur.execute(query, (filmName, oldFilmName))
        print(filmName, oldFilmName)
        conn.commit()


class ViewBookingStaffModel:
    def __init__(self):
        pass

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

    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            pattern = r'[A-Za-z ]{3,}' #Check letters only at least 3 in length
            if re.fullmatch(pattern, cinemaName):
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

    def checkAccountNotExist(self, email):
        query = 'SELECT * FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account exists.")
            return 0
        else:
            print("Account does not exist.")
            return 1

    def getUserAccountType(self, email):
        query = 'SELECT user_type FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchone()
        userType = int(''.join(map(str, record)))
        if userType == 0:
            return 1
        else:
            return 0

    def searchForAccountByEmail(self, email):
        query = 'SELECT * FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account found")
            return 1
        else:
            print("Account not found")
            return 0

    def retrieveAccountInfo(self, email):
        query = 'SELECT email, password, user_cinema FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        account = cur.fetchone()
        print(account[0])
        return account
    
    def checkCinemaNameInDB(self, cinemaName):
        query = 'SELECT * FROM Cinemas WHERE cinema_name = ?'
        cur.execute(query, (cinemaName, ))
        record = cur.fetchall()
        if len(record) > 0:
            return 1
        else:
            return 0

    def addBookingStaff(self, email, password, cinemaName):
        userType = 0
        query = '''
        INSERT INTO Users(email, password, user_type, user_cinema)
        VALUES (?, ?, ?, ?)
        '''
        cur.execute(query, (email, password, userType, cinemaName))
        conn.commit()
        print("Booking Staff added.")

    def updateBookingStaff(self, email, password, cinemaName):
        query = '''
        UPDATE Users
        SET email = ?,
        password = ?,
        user_cinema = ?
        WHERE email = ?
        '''
        cur.execute(query, (email, password, cinemaName, email))
        conn.commit()
        print("Booking Staff updated.")
    
    def deleteBookingStaff(self, email):
        query = '''
        DELETE FROM Users WHERE email = ?
        '''
        cur.execute(query, (email,))
        conn.commit()
        print("Booking staff deleted.")

class ViewAdminModel:
    def __init__(self):
        pass

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

    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            pattern = r'[A-Za-z ]{3,}' #Check letters only at least 3 in length
            if re.fullmatch(pattern, cinemaName):
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

    def checkAccountNotExist(self, email):
        query = 'SELECT * FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account exists.")
            return 0
        else:
            print("Account does not exist.")
            return 1

    def getUserAccountType(self, email):
        query = 'SELECT user_type FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchone()
        userType = int(''.join(map(str, record)))
        if userType == 1:
            return 1
        else:
            return 0

    def searchForAccountByEmail(self, email):
        query = 'SELECT * FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account found")
            return 1
        else:
            print("Account not found")
            return 0

    def retrieveAccountInfo(self, email):
        query = 'SELECT email, password, user_cinema FROM Users WHERE email = ?'
        cur.execute(query, (email,))
        account = cur.fetchone()
        print(account[0])
        return account

    def addAdmin(self, email, password):
        userType = 1
        query = '''
        INSERT INTO Users(email, password, user_type)
        VALUES (?, ?, ?)
        '''
        cur.execute(query, (email, password, userType))
        conn.commit()
        print("Admin added.")

    def updateAdmin(self, email, password):
        query = '''
        UPDATE Users
        SET email = ?,
        password = ?
        WHERE email = ?
        '''
        cur.execute(query, (email, password, email))
        conn.commit()
        print("Admin updated.")
    
    def deleteAdmin(self, email):
        query = '''
        DELETE FROM Users WHERE email = ?
        '''
        cur.execute(query, (email,))
        conn.commit()
        print("Admin deleted.")
    

    
class AddCinemasModel:
    def checkCities(self):
        cur.execute("SELECT * FROM cities")
        cities = cur.fetchall()
        if len(cities) == 0:
            return 0
        else:
            return 1

    def getCities(self):
        cur.execute("SELECT * FROM cities")
        cities = cur.fetchall()
        return cities
    
    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            pattern = r'[A-Za-z0-9 ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, cinemaName):
                return 1
            else:
                return 0
        else:
            return 0
        
    def checkCinemaName(self, cityName, cinemaName):
        query = "SELECT cinema_name FROM Cinemas WHERE city_name = ?"
        cur.execute(query, (cityName,))
        cinemas = cur.fetchall()
        for cinema in cinemas:
            if cinema[0] == cinemaName:
                return 0
        return 1
    
    def addCinema(self, cityName, cinemaName):
        query = "SELECT * FROM Cinemas WHERE city_name = ?"
        cur.execute(query, (cityName,))
        cinemasBefore = cur.fetchall()
        query = "INSERT INTO Cinemas(city_name, cinema_name) VALUES (?,?)"
        cur.execute(query, (cityName, cinemaName))
        query = """INSERT INTO CinemaScreens(cinema_name)
                    VALUES (?),
                    (?),
                    (?),
                    (?),
                    (?),
                    (?)"""
        cur.execute(query, (cinemaName, cinemaName, cinemaName, cinemaName, cinemaName, cinemaName))
        conn.commit()
        query = "SELECT * FROM Cinemas WHERE city_name = ?"
        cur.execute(query, (cityName,))
        cinemasAfter = cur.fetchall()
        if len(cinemasAfter) > len(cinemasBefore):
            return 1
        else: 
            return 0
        
    def validateCityNameSyntax(self, cityName):
        if len(cityName) > 0:
            pattern = r'[A-Za-z ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, cityName):
                return 1
            else:
                return 0
        else:
            return 0
        
    def checkCityName(self, cityName):
        query = "SELECT * FROM Cities WHERE city_name = ?"
        cur.execute(query, (cityName,))
        cities = cur.fetchall()
        if len(cities) > 0:
            return 0
        else:
            return 1
    
    def validatePriceSyntax(self, price):
        if len(price) > 0:
            pattern = r'^\d+(.\d{2})?$' #price regex
            if re.fullmatch(pattern, price):
                return 1
            else:
                return 0
        else:
            return 0 

    def addCity(self, cityName, morningPrice, afternoonPrice, eveningPrice):
        cur.execute("SELECT * FROM Cities")
        citiesBefore = cur.fetchall()
        query = "INSERT INTO Cities(city_name, morning_price, afternoon_price, evening_price) VALUES (?,?,?,?)"
        cur.execute(query, (cityName, morningPrice, afternoonPrice, eveningPrice))
        conn.commit()
        cur.execute("SELECT * FROM Cities")
        citiesAfter = cur.fetchall()
        if len(citiesAfter) > len(citiesBefore):
            return 1
        else:
            return 0


class ViewCinemaScreeningsModel:
    def __init__(self):
        pass

    def validateTimeSyntax(self, inputTime):
        try:
            time.strptime(inputTime, '%H:%M')
            return 1
        except ValueError:
            return 0
        
    def validateDateSyntax(self, inputDate):
        try:
            datetime.strptime(inputDate,'%d/%m/%Y').date()
            return 1
        except ValueError:
            return 0

    def validateCinemaNameSyntax(self, cinemaName):
        if len(cinemaName) > 0:
            pattern = r'[A-Za-z0-9 ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, cinemaName):
                return 1
            else:
                return 0
        else:
            return 0   

    def validateScreensSyntax(self, screen):
        if len(screen) > 0:
            pattern = r'[0-9]{0,3}'
            if re.fullmatch(pattern, screen):
                return 1
            else:
                return 0
        else:
            return 0
    
    def checkScreen(self, screen, cinemaName):
        query = "SELECT * FROM CinemaScreens WHERE cinema_screenID = ? AND cinema_name = ?"
        cur.execute(query, (screen, cinemaName))
        screens = cur.fetchall()
        if len(screens) > 0:
            return 1
        else:
            return 0
    
    def checkTimeDate(self, screen, cinemaName, time, date):
        query = "SELECT * FROM FilmScreenings WHERE screening_screen = ? AND cinema_name = ? AND screening_time = ? AND screening_date = ?"
        cur.execute(query, (screen, cinemaName, time, date))
        screenings = cur.fetchall()
        if len(screenings) > 0:
            return 0
        else:
            return 1
    
    def validateFilmNameSyntax(self, filmName):
        if len(filmName) > 0:
            pattern = r'[A-Za-z0-9,.\& ]{0,50}' #Letters/numbers and up to 50 char
            if re.fullmatch(pattern, filmName):
                return 1
            else:
                return 0
        else:
            return 0
        
    def addScreening(self, time, date, screen, cinemaName, filmName, LHTickets, UHTickets, VIPTickets):
        cur.execute("SELECT * FROM FilmScreenings")
        screeningsBefore = cur.fetchall()
        query = "INSERT INTO FilmScreenings(screening_time, screening_date, screening_screen, cinema_name, film_name, lower_hall_tickets_left, upper_hall_tickets_left, VIP_tickets_left) VALUES (?,?,?,?,?,?,?,?)"
        cur.execute(query, (time, date, screen, cinemaName, filmName, LHTickets, UHTickets, VIPTickets))
        conn.commit()
        cur.execute("SELECT * FROM FilmScreenings")
        screeningsAfter = cur.fetchall()
        if len(screeningsAfter) > len(screeningsBefore):
            return 1
        else:
            return 0
        
    def checkScreeningID(self, screeningID):
        query = "SELECT * FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        screenings = cur.fetchall()
        if len(screenings) > 0:
            return 1
        else:
            return 0
        
    def deleteScreening(self, screeningID):
        cur.execute("SELECT * FROM FilmScreenings")
        screeningsBefore = cur.fetchall()
        query = "DELETE FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        conn.commit()
        cur.execute("SELECT * FROM FilmScreenings")
        screeningsAfter = cur.fetchall()
        if len(screeningsBefore) > len(screeningsAfter):
            return 1
        else:
            return 0
    
    def getScreening(self, screeningID):
        query = "SELECT * FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        screening = cur.fetchone()
        return screening
    
    def getScreeningInfo(self, screeningID):
        query = "SELECT lower_hall_tickets_left, upper_hall_tickets_left, VIP_tickets_left FROM FilmScreenings WHERE screeningID = ?"
        cur.execute(query, (screeningID,))
        screeningInfo = cur.fetchone()
        return screeningInfo
    
    def updateScreening(self, screeningID, updateList):
        query = "UPDATE FilmScreenings SET screening_time = ?, screening_date = ?, screening_screen = ?, cinema_name = ?, film_name = ?, lower_hall_tickets_left = ?, upper_hall_tickets_left = ?, VIP_tickets_left = ? WHERE screeningID = ?"
        cur.execute(query, (updateList[0], updateList[1], updateList[2], updateList[3], updateList[4], updateList[5], updateList[6], updateList[7], screeningID))
        conn.commit()
