import unittest
from DatabaseAccess import *
from HorizonModel import *
from HorizonController import *
from HorizonController import LoginController

conn = getConn()
cur = getCursor()

class TestDatabase(unittest.TestCase):

    def test_connection(self):
        # Test that a connection to the database can be established
        self.assertTrue(conn)
    
    def test_insert(self):
        # Test that data can be inserted into the database
        cur.execute('''
        INSERT INTO users(email, password, user_type) 
        VALUES ('john@example.com', 'test', 1)
        ''')
        conn.commit
        
        # Test to select the data to ensure it was inserted successfully
        cur.execute("SELECT * FROM users WHERE email='john@example.com'")
        result = cur.fetchone()
        # self.assertEqual(result[1], '4')
        self.assertEqual(result[1], 'john@example.com')
        
    def test_update(self):
        # Test that a record can be updated in the database
        cur.execute("UPDATE users SET userID='20' WHERE email='john@example.com'")
        conn.commit
        
        # Retrieve the record to ensure it was updated successfully
        cur.execute("SELECT * FROM users WHERE email='john@example.com'")
        result = cur.fetchone()
        self.assertEqual(result[1], 'john@example.com')
        
    def test_delete(self):
        # Test that a record can be deleted from the database
        cur.execute("DELETE FROM users WHERE email='john@example.com'")
        conn.commit
        
        # Try to retrieve the deleted record to ensure it was deleted
        cur.execute("SELECT * FROM users WHERE email='john@example.com'")
        result = cur.fetchone()
        self.assertIsNone(result)
        
    def test_query(self):
        # Test that data can be queried from the database
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()
        self.assertGreater(len(results), 0)

class TestLogin(unittest.TestCase):

    def test_login(self):

        # Test for finding record of correct login - Imitating Logging In
        success = self.model = LoginModel.checkAccountInDB(self,'arthur@gmail.com', '12345')
        self.assertTrue(success)

        # Test for finding record with wrong email - Imitating Attempting to log in
        fail = self.model = LoginModel.checkAccountInDB(self,'test@gmail.com', '12345')
        self.assertFalse(fail)

        # Test for finding record with correct email but wrong password - Imitating Attempting to log in
        fail = self.model = LoginModel.checkAccountInDB(self,'arthur@gmail.com', '7')
        self.assertFalse(fail)

        # Test for getting user type of user
        success = self.model = LoginModel.getAccountUserType(self,'henry@gmail.com', 'hello')
        self.assertTrue(success)

        # Test for getting Cinema user is working at
        success = self.model = LoginModel.getAccountCinema(self, 'henry@gmail.com', 'hello')
        self.assertTrue(success)

class TestAppBookStaff(unittest.TestCase):
    
    def test_booking(self):

        # Create a booking
        success = self.model = CreateBookingModel.createBooking(self, '5394378565', '1', 'A2, A3, A4', '22', '3', '3')
        self.assertTrue(success)

        # Cancel a booking
        success = self.model = CancelBookingModel.removeBooking(self, '5394378565')
        self.assertTrue(success)

        # When cancel booking is made, check time of booking to see if it is allowed
        success = self.model = CancelBookingModel.checkCancelTime(self, '1')
        self.assertTrue(success)

        # Checking if there are dates of showings available
        success = self.model = CreateBookingModel.checkForDates(self, 'Avengers', 'Cabot Circus')
        self.assertTrue(success)
        
        # Test to see if any dates are returned for an incorrect film

        success = self.model = CreateBookingModel.getPrices(self, 'Cabot Circus')
        self.assertTrue(success)

    def test_films(self):
        
        #see details of a film
        success = self.model = ViewFilmModel.getFilmInfo(self, '1')
        self.assertTrue(success)

        #see what films are on at a cinema
        success = self.model = ViewFilmListingsModel.getFilms(self, 'Cabot Circus')

        #see screenings of a selected film
        success = self.model = ViewFilmListingsModel.returnScreeningsInfo(self, 'Avengers', 'Cabot Circus')
        self.assertTrue(success)

class TestAppAdmin(unittest.TestCase):

    def test_film(self):

        #Add film
        success = self.model = ViewFilmModel.addFilm(self, 'Shrek', 'Green guy', 'The Rock', 'Horror', '18', '10')
        self.assertTrue(success)
    
        #Delete film
        success = self.model = ViewFilmModel.deleteFilm(self, '3')
        self.assertTrue(success)

    def test_screenings(self):

        #Test for adding a screening
        success = self.model = ViewCinemaScreeningsModel.addScreening(self, '12:00', '19/01/2023', '2', 'West End', 'Aveners', '50', '70', '20')
        self.assertTrue(success)

        #Test for deleting a screening
        success = self.model = ViewCinemaScreeningsModel.deleteScreening(self, '4')
        self.assertTrue(success)

    def test_searches(self):
        
        #Test searching admin
        success = ViewAdminModel.searchForAccountByEmail(self, 'milner@gmail.com')
        self.assertTrue(success)

        #Test searching booking staff
        success = ViewBookingStaffModel.searchForAccountByEmail(self, 'arthur@gmail.com')
        self.assertTrue(success)

    def test_report(self):

        success = self.model = GenerateReportModel.returnReportInfo(self, '1' , 'Cabot Circus')
        self.assertTrue(success)

    def test_staff(self):
        
        #View Admin
        success = self.model = ViewAdminModel.searchForAccountByEmail(self, 'milner@gmail.com')
        self.assertTrue(success)

        #View Booking Staff
        success = self.model = ViewBookingStaffModel.searchForAccountByEmail(self, 'arthur@gmail.com')
        self.assertTrue(success)

class TestAppValidation(unittest.TestCase):

    def test_login_validation(self):

        # Test for email syntax (must include @, .com etc.)
        fail = self.model = LoginModel.validateEmailSyntax(self,'test')
        self.assertFalse(fail)

        # Test for if email syntax is partially correct
        fail = self.model = LoginModel.validateEmailSyntax(self, 'test@gmail')
        self.assertFalse(fail)

        # Test for if email syntax is fully correct
        success = self.model = LoginModel.validateEmailSyntax(self, 'test@gmail.com')
        self.assertTrue(success)

        # Test for password syntax (must be more than 4 characters)
        fail = self.model = LoginModel.validatePasswordSyntax(self, '0123')
        self.assertFalse(fail)

        # Test for password syntax correct
        success = self.model = LoginModel.validatePasswordSyntax(self, '01234')
        self.assertTrue(success)

    def test_film_validation(self):

        # Test for film name syntax
        fail = self.model = ViewFilmListingsModel.validateFilmNameSyntax(self, '123456789123456789123456789123456789123456789123456789')
        self.assertFalse(fail)

        # Test for cinema name syntax
        fail = self.model = ViewFilmListingsModel.validateCinemaNameSyntax(self, '12')
        self.assertFalse(fail)

        # Test for film age syntax
        fail = self.model = ViewFilmModel.validateFilmAgeSyntax(self, 'Twenty')
        self.assertFalse(fail)

        # Test for film name syntax
        fail = self.model = ViewFilmModel.validateFilmNameSyntax(self, '123456789123456789123456789123456789123456789123456789')
        self.assertFalse(fail)

    def test_bookingstaff_validation(self):

        # Test for email syntax
        fail = self.model = ViewBookingStaffModel.validateEmailSyntax(self, 'test')
        self.assertFalse(fail)

        # Test for password syntax
        fail = self.model = ViewBookingStaffModel.validatePasswordSyntax(self, '12')
        self.assertFalse(fail)

        # Test for cinema name syntax
        fail = self.model = ViewBookingStaffModel.validateCinemaNameSyntax(self, '12')
        self.assertFalse(fail)

    def test_report_validation(self):

        # Test for incorrect report type
        fail = self.model = GenerateReportModel.validateReportTypeSyntax(self, '10')
        self.assertFalse(fail)

        # Test for incorrect report parameter
        fail = self.model = GenerateReportModel.validateReportParameterSyntax(self, '3', '24')
        self.assertFalse(fail)


if __name__ == '__main__':
    unittest.main()