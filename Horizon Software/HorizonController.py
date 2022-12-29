from HorizonModel import *
import datetime
import random

class HomeController:
    def __init__(self,model, view):
        self.model = model
        self.view = view

    def searchCinemas(self):
        try:
            cinemas = self.model.getCinemas()
            self.view.cinemaSearchSuccess(cinemas)
        except ValueError as error:
            pass
    


class LoginController:
    def __init__(self, model, view):
        self.model = model 
        self.view = view

    def login(self, email, password):
        try:
            if self.model.validateEmailSyntax(email):
                if self.model.validatePasswordSyntax(password):
                    if self.model.checkAccountInDB(email, password):
                        print("Account found.")
                        userType = self.model.getAccountUserType(email, password)
                        accountCinema = self.model.getAccountCinema(email, password)
                        self.view.loginSuccess(f'Logged in as {email}.', userType, accountCinema)
                    else:
                        print("Could not find account.")
                        self.view.loginFailed('Could not find account.')
                else:
                    print("Password syntax incorrect.")
                    self.view.loginFailed('Password syntax incorrect.')
            else:
                print("Email syntax incorrect.")
                self.view.loginFailed('Email syntax incorrect.')
        except ValueError as error:
            self.view.loginFailed(error)

class ViewFilmListingsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def searchListings(self, filmName, cinemaName):
        try:
            if self.model.validateFilmNameSyntax(filmName):
                if self.model.validateCinemaNameSyntax(cinemaName):
                    if self.model.checkForScreenings(filmName, cinemaName):
                        screeningInfo = self.model.returnScreeningsInfo(filmName, cinemaName)
                        self.view.searchSuccess('Displaying Screenings for ' + str(filmName) + ' at ' + str(cinemaName) + '.', screeningInfo)
                    else:
                        self.view.searchFailed('No screenings found.')
                else:
                    self.view.searchFailed('Cinema name syntax incorrect.')
            else:
                print("Film name syntax incorrect.")
                self.view.searchFailed('Film name syntax incorrect.')
        except ValueError as error:
            self.view.searchFailed(error)
        
    def searchFilms(self, cinemaName):
        try:
            if self.model.validateCinemaNameSyntax(cinemaName):
                filmNames = self.model.getFilms(cinemaName)
                self.view.searchSuccess('Showing films in ' + str(cinemaName)+".", filmNames)
            else:
                self.view.searchFailed('Cinema name syntax incorrect.')
        except ValueError as error:
            self.view.searchFailed(error)


class CreateBookingController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    #function to fetch films to show in combobox
    def searchFilm(self, cinemaName):
        try:
            if self.model.validateCinemaNameSyntax(cinemaName):
                if self.model.checkForFilms(cinemaName):
                    films = self.model.returnFilms(cinemaName)
                    self.view.filmSearchSuccess('Displaying films at ' + str(cinemaName) + '.', films)
                else:
                    #self.view.searchFailed('No films found.')
                    print("no films")
            else:
                self.view.searchFailed('Cinema name syntax incorrect.')
        except ValueError as error:
            pass
    
    #function to update other comboboxes when film is selected
    def searchDates(self, filmName, cinemaName):
        try:
            if self.model.checkForDates(filmName, cinemaName):
                dates = self.model.returnDates(filmName, cinemaName)
                self.view.dateSearchSuccess('Found dates for film '+str(filmName)+'.', dates)
            else:
                self.view.searchFailed('no dates found.')
        except ValueError as error:
            pass
    
    def searchShowings(self, filmDate, filmName, cinemaName):
        try:
            if self.model.checkForShowings(filmDate, filmName, cinemaName):
                showings = self.model.returnShowings(filmDate, filmName, cinemaName)
                self.view.showingSearchSuccess('Found Showings for film ' + str(filmName) + " on " + str(filmDate) +".", showings)
            else:
                self.view.searchFailed('no showings found.')
        except ValueError as error:
            pass
    
    def checkAvailability(self, numOfTickets, seatType, showing, date, film, cinema):
        try:
            if self.model.checkForTickets(showing, date, film, cinema):
                amountOfTickets = self.model.returnTickets(showing, date, film, cinema)
                if numOfTickets <= amountOfTickets[0][seatType-1]:
                    self.view.checkPrice('Available tickets for film ' + str(film))
                else:
                    self.view.availabilityFailed('not enough tickets', amountOfTickets)
            else:
                self.view.searchFailed('No tickets.')
        except ValueError as error:
            pass
    
    def checkPrice(self, numOfTickets, seatType, showing, date, film, cinema, message):
        try:
            #get prices of different part fo the day 
            prices = self.model.getPrices(cinema)
            #check what time showing is at 
            print(showing)
            time = datetime.datetime.strptime(showing, "%H:%M")
            morning = datetime.datetime.strptime("09:00", "%H:%M")
            noon = datetime.datetime.strptime("12:00", "%H:%M")
            afternoon = datetime.datetime.strptime("17:00", "%H:%M")
            if time>=morning and time < noon:
                price = prices[0]
            elif time>=noon and time<afternoon:
                price = prices[1]
            elif time>=afternoon:
                price = prices[2]
            else:
                ValueError
            #CALCULATE PRICE
            #calculate price of 1 ticket 
            if seatType == 2:
                price = price *1.20
            if seatType == 3:
                price = (price *1.20)*1.20
            print("price of 1 ticket = " + str(price))
            #calculate total 
            price = price * numOfTickets
            print("total price = "+str(price))
            self.view.priceSuccess(message, price)
            
        except ValueError as error:
            pass
    
    def createBooking(self, seatType, price, numOfTickets, time, date, film, cinema):
        try:
            screeningID = self.model.getScreeningID(time, date, film, cinema)
            alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            letter = alphabet[random.randint(0, 24)]
            number = random.randint(0,15)
            ticketSeats = ""
            for ticket in range(numOfTickets):
                ticketSeats = ticketSeats+"[" + str(letter)+str(number)+"]"
                number+= 1
            bookingID = ""
            for i in range(10):
                bookingID = bookingID + str(random.randint(0,9))
            if self.model.createBooking(int(bookingID), seatType, ticketSeats, price, numOfTickets, screeningID):
                screeningScreen = self.model.getScreeningScreen(screeningID)
                self.view.showBooking(bookingID, ticketSeats, price, numOfTickets, time, date, film, cinema, screeningScreen)
            else:
                self.view.searchFailed("Booking unsuccessful")
        except ValueError as error:
            pass


class GenerateReportController:
    def __init__(self, model, view):
        self.model = model
        self.view=view

    def generateReport(self, reportType, reportParameter):
        try:
            if self.model.validateReportTypeSyntax(reportType):
                if self.model.validateReportParameterSyntax(reportType, reportParameter):
                    if self.model.checkReportReturnsInfo(reportType, reportParameter):
                        reportInfo = self.model.returnReportInfo(reportType, reportParameter)
                        self.view.generateSuccess('Generating report', reportInfo)
                    else:
                        self.view.generateFailed('Report did not return any results.')
                else:
                    self.view.generateFailed('Report parameter syntax incorrect.')
            else:
                self.view.generateFailed('Report type syntax incorrect.')
        except ValueError as error:
            self.view.generateFailed(error)
                        


class CancelBookingController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def cancelBooking(self, bookingID):
        try:
            if len(bookingID) == 10:
                if self.model.checkBookingID(bookingID):
                    bookingInfo = self.model.getBooking(bookingID)
                    if self.model.checkCancelTime(bookingInfo[5]):                        
                        if self.model.removeBooking(bookingID):
                            if self.model.updateTickets(bookingInfo[4], bookingInfo[1], bookingInfo[5]):
                                self.view.cancelSuccess("Cancel success for booking ID: "+str(bookingID)+".")
                            else:
                                self.view.searchFailed("Screening tickets remaining couldnt be updated.")
                        else:
                            self.view.searchFailed("Booking could not be removed from database.")
                    else:
                        self.view.searchFailed("Booking can't be canceled less that a day before showing.")
                else:
                    self.view.searchFailed("No booking connected to that booking ID.")
            else:
                self.view.searchFailed("Booking ID not correct.")
        except ValueError as error:
            pass



class ViewFilmController:
    def __init__(self, model, view):
        self.view = view
        self.model = model
    
    def addFilm(self, filmName, filmDescription, filmActors, filmGenre, filmAge, filmRating):
        try:
            if self.model.validateFilmNameSyntax(filmName):
                if self.model.validateFilmNameSyntax(filmDescription):
                    if self.model.validateFilmNameSyntax(filmActors):
                        if self.model.validateFilmNameSyntax(filmGenre):
                            if self.model.validateFilmAgeSyntax(filmAge):
                                if self.model.validateFilmRatingSyntax(filmRating):
                                    if self.model.addFilm(filmName, filmDescription, filmActors, filmGenre, filmAge, filmRating):
                                        self.view.addFilmSuccess(filmName)
                                    else:
                                        self.view.searchFailed("Cannot Add Film To Database.")
                                else:
                                    self.view.searchFailed("Invalid Rating Syntax.")
                            else:
                                self.view.searchFailed("Invalid Film Age Syntax.")
                        else:
                            self.view.searchFailed("Invalid Film Genre Syntax.")
                    else:
                        self.view.searchFailed("Invalid Film Actors Syntax.")
                else:
                    self.view.searchFailed("Invalid Film Description Syntax.")
            else:
                self.view.searchFailed("Invalid Film Name Syntax.")
        except ValueError as error:
            self.view.searchFailed(error)

