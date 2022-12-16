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
        query = 'SELECT email, password FROM BookingStaff WHERE email = ? AND password = ?'
        cur.execute(query, (email, password))
        record = cur.fetchall()
        if len(record) > 0:
            print("Account found")
            return 1
        else:
            print("Account not found")
            return 0

