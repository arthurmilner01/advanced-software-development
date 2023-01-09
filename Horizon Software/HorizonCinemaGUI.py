#Arthur Milner 21035478
#Joseph Cauvy-Foster 21031786
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from HorizonController import *
from DatabaseAccess import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horizon Cinema Booking System")
        self.geometry("1366x768")
        self.resizable(0,0)
        self.style = ttk.Style(self)
        self.configure(bg="#181818")
        self.style.configure('TLabel', font=('Helvetica bold', 15), background="#181818", foreground="#b3b3b3")
        self.style.configure('TButton', font=("Helvetica bold", 10),foreground="#121212", height=40, width=25)
        self.style.configure('TFrame', font=('Helvetica bold', 15), background="#181818", foreground="#b3b3b3")
        try:
            self.attributes('-toolwindow', True)
        except tk.TclError:
            print("Windows Only")

        # Creating all the frames, inserting them into a dictionary for access later
        self.frames = {}

        for F in (LoginFrame, HomeFrame, ViewBookingStaffFrame, ViewAdminFrame, ViewFilmFrame, AddCinemasFrame, GenerateReportFrame, ViewFilmListingsFrame, CreateBookingFrame, CancelBookingFrame, ViewCinemaScreeningsFrame):
            frameName = F.__name__
            frame = F(self)
            self.frames[frameName] = frame

            #Placing each frame at the same size so that they are ready to be used with tkraise as appropriate
            frame.place(height=768, width=1366)

        self.showFrame("LoginFrame")

    # Function which will raise the given frame to the front of the GUI
    def showFrame(self, frameName):
        frame = self.frames[frameName]
        frame.createWidgets()
        frame.tkraise()

    def getFrame(self, frameName):
        frame = self.frames[frameName]
        return frame
    

class LoginFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.model = LoginModel()
        self.view =  self
        self.controller = LoginController(self.model, self.view)
        

        # self.createWidgets()

    def createWidgets(self):
        self.__email = tk.StringVar()
        self.__password = tk.StringVar()

        self.login_title_label = ttk.Label(self, text="Login", font=('Helvetica bold', 26), foreground="white")
        self.login_title_label.grid(columnspan=3, row=0, padx=5, pady=5)

        self.email_label = ttk.Label(self, text="Username:")
        self.email_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(self, textvariable=self.__email)
        self.email_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self, textvariable=self.__password, show="*")
        self.password_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(columnspan=2, row=3, padx=10, pady=10)

        self.login_message = ttk.Label(self, text="               ")
        self.login_message.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    def getEmail(self):
        return self.__email

    def getPassword(self):
        return self.__password

    def loginSuccess(self, message, userType, accountCinema):
        #Resetting entry fields and email and password variables
        currentUser.setEmail(self.__email.get())
        currentUser.setAccountType(userType)
        if accountCinema != None:
            currentUser.setAccountCinema(accountCinema)
        print(currentUser.accountType)
        print(currentUser.accountCinema)
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.email_entry['foreground'] = 'black'
        self.password_entry['foreground'] = 'black'
        self.__email.set('')
        self.__password.set('')
        mb.showinfo(title="Logged In", message=message)
        app.showFrame("HomeFrame")
    
    def loginFailed(self, message):
        self.login_message['text'] = message
        self.login_message['foreground'] = 'red'
        self.email_entry['foreground'] = 'red'
        self.password_entry['foreground'] = 'red'
        self.login_message.after(3000, self.hideLoginMessage)

    def hideLoginMessage(self):
        self.login_message['text'] = ''

    def login(self):
        if self.controller:
            self.controller.login(self.__email.get(), self.__password.get())



class HomeFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.current_cinema_combobox_values = ["Select Current Cinema"]
        self.createWidgets()

        self.model = HomeModel()
        self.view =  self
        self.controller = HomeController(self.model, self.view)

    def createWidgets(self):
        self.__clearWidgets()
        if currentUser.accountType == 0 or currentUser.accountType == 1 or currentUser.accountType == 2:
            self.horizon_cinema_label = ttk.Label(self, text="Horizon Cinemas", font=('Helvetica bold', 15))
            self.horizon_cinema_label.grid(column=0,row=1)
            self.current_user_label = ttk.Label(self, text=currentUser.getEmail(), font=('Helvetica bold', 15))
            self.current_user_label.grid(column=0,row=2)
            self.listings_button = ttk.Button(self, command=lambda : app.showFrame("ViewFilmListingsFrame"), text="View Films/ Listings")
            self.listings_button.grid(column=1, row=1, padx=10, pady=20, sticky=tk.W)
            self.create_booking_button = ttk.Button(self, command=lambda : app.showFrame("CreateBookingFrame"), text="Create Booking")
            self.create_booking_button.grid(column=2, row=1, padx=10, pady=20)
            self.cancel_booking_button = ttk.Button(self, command=lambda : app.showFrame("CancelBookingFrame"), text="Cancel Booking")
            self.cancel_booking_button.grid(column=3, row=1, padx=10, pady=20)
            self.logout_button = ttk.Button(self, command=lambda : app.showFrame("LoginFrame"), text="Logout")
            self.logout_button.grid(column=3, columnspan=2, row=3, padx=10, pady=20, sticky=tk.E)
        if currentUser.accountType == 1 or currentUser.accountType == 2:
            self.generate_report_button = ttk.Button(self, command=lambda : app.showFrame("GenerateReportFrame"), text="Generate Report")
            self.generate_report_button.grid(column=4, row=1, padx=10, pady=20, sticky=tk.E)
            self.view_booking_staff_button = ttk.Button(self, command=lambda : app.showFrame("ViewBookingStaffFrame"), text="View Booking Staff")
            self.view_booking_staff_button.grid(column=1, row=2, padx=10, pady=20, sticky=tk.W)
            self.view_film_button = ttk.Button(self, command=lambda : app.showFrame("ViewFilmFrame"), text="View Film")
            self.view_film_button.grid(column=4, row=2, padx=10, pady=20, sticky=tk.E)
            self.view_cinema_screenings_button = ttk.Button(self, command= lambda:app.showFrame("ViewCinemaScreeningsFrame"), text="View Cinema Screenings")
            self.view_cinema_screenings_button.grid(column=1, row=3, padx=10, pady=10)
            self.current_cinema_combobox = ttk.Combobox(self, state="readonly")
            self.current_cinema_combobox['values'] = self.current_cinema_combobox_values
            self.current_cinema_combobox.bind("<Enter>", self.comboboxHoverFunction) #event <Enter> changes combobox when hovered over and not when selected
            self.current_cinema_combobox.bind("<<ComboboxSelected>>", self.selectComboboxFunction) #event <<ComboboxSelected>> does function when new value is selected
            self.current_cinema_combobox.current(0)
            self.current_cinema_combobox.grid(column=0, row=3, padx=10, pady=20)
        if currentUser.accountType == 2:
            self.view_admin_button = ttk.Button(self, command=lambda : app.showFrame("ViewAdminFrame"), text="View Admin Staff")
            self.view_admin_button.grid(column=2, row=2, padx=10, pady=20)
            self.view_cinema_button = ttk.Button(self, command=lambda : app.showFrame("AddCinemasFrame"), text="Add Cinemas/City")
            self.view_cinema_button.grid(column=3, row=2, padx=10, pady=20)

    def __clearWidgets(self):
        for widgets in self.winfo_children():
         widgets.destroy()

    def logout(self):
        currentUser.setEmail("default")
        currentUser.setAccountType(0)
        app.showFrame("LoginFrame")
    
    def cinemaSearchSuccess(self, cinemas):
        self.current_cinema_combobox_values = []
        for cinema in cinemas:
            self.current_cinema_combobox_values.append(cinema[0])

    def comboboxHoverFunction(self, cinema):
        if self.controller:
            self.controller.searchCinemas()
        self.current_cinema_combobox['values'] = self.current_cinema_combobox_values

    def selectComboboxFunction(self, cinema):
        currentUser.setAccountCinema(self.current_cinema_combobox.get())
        
        
      

class ViewBookingStaffFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self.model = ViewBookingStaffModel()
        self.view = self
        self.controller = ViewBookingStaffController(self.model, self.view)
        
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        self.header = ttk.Frame(self)
        self.header.grid(row=0)
        self.current_page_label = ttk.Label(self.header, text="View Booking Staff", font=('Helvetica bold', 20))
        self.current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        self.staff_name_label = ttk.Label(self.header, text="Staff Email:")
        self.staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        self.staff_cinema_label = ttk.Label(self.header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        self.staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        self.menu_button = ttk.Button(self.header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        self.menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)
        self.__email = tk.StringVar()
        self.__password = tk.StringVar()
        self.__cinemaName = tk.StringVar()
        self.__searchEmail = tk.StringVar()
        self.email_label = ttk.Label(self.content, text="Booking Staff Email:")
        self.email_label.grid(row=0, column=0, pady=20, padx=10)
        self.booking_staff_email_entry = ttk.Entry(self.content, textvariable=self.__email)
        self.booking_staff_email_entry.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        self.password_label = ttk.Label(self.content, text="Booking Staff Password:")
        self.password_label.grid(row=1, column=0, pady=20, padx=10)
        self.booking_staff_password_entry = ttk.Entry(self.content, show="*", textvariable=self.__password)
        self.booking_staff_password_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        self.cinema_name_label = ttk.Label(self.content, text="Booking Staff Cinema:")
        self.cinema_name_label.grid(row=2, column=0, pady=20, padx=10)
        self.booking_staff_cinema_name_entry = ttk.Entry(self.content, textvariable=self.__cinemaName)
        self.booking_staff_cinema_name_entry.grid(row=2, column=1, columnspan=2, pady=20, padx=10)
        self.add_booking_staff_button = ttk.Button(self.content, text="Add Booking Staff", command=self.addBookingStaff)
        self.add_booking_staff_button.grid(row=4, column=0, pady=20, padx=10)
        self.edit_booking_staff_button = ttk.Button(self.content, text="Edit Booking Staff", command=self.updateBookingStaff)
        self.edit_booking_staff_button.grid(row=4, column=1, pady=20, padx=10)
        self.remove_booking_staff_button = ttk.Button(self.content, text="Remove Booking Staff", command=self.deleteBookingStaff)
        self.remove_booking_staff_button.grid(row=4, column=2, pady=20, padx=10)
        self.horizontal_line_label = ttk.Label(self.content, text="-------------------------------------------------------------------------------------------")
        self.horizontal_line_label.grid(row=5, column=0, columnspan=3)
        self.search_label = ttk.Label(self.content, text="Search Details by Email:")
        self.search_label.grid(row=6, column=0, pady=30, padx=10)
        self.search_email_entry = ttk.Entry(self.content, textvariable=self.__searchEmail)
        self.search_email_entry.grid(row=6, column=2, columnspan=2, pady=20, padx=10)
        self.search_email_button = ttk.Button(self.content, text="Search", command=self.searchForBookingStaff)
        self.search_email_button.grid(row=7, column=0, columnspan=3, pady=10, padx=10)

    
    def searchFailed(self, message):
        mb.showerror(title="Error:", message=message)
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')
        self.__cinemaName.set('')


    def searchSuccess(self, message):
        mb.showinfo(title="Booking Staff Account Found:", message="Account Info:" + str(message))
        self.__email.set(message[0])
        self.__password.set(message[1])
        self.__cinemaName.set(message[2])
        self.__searchEmail.set('')
        print(message)

    def addSuccess(self, message):
        mb.showinfo(title="Added Booking Staff:", message="Account Info:" + str(message))
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')
    
    def updateSuccess(self, message):
        mb.showinfo(title="Booking Staff Updated:", message="Updated Info:" + str(message))
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')

    def deleteSuccess(self, message):
        mb.showinfo(title="Booking Staff Deleted:", message="Account with details "+ str(message) + " deleted.")
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')

    def searchForBookingStaff(self):
        if self.controller:
            self.controller.searchBookingStaff(self.__searchEmail.get())

    def addBookingStaff(self):
        if self.controller:
            self.controller.addBookingStaff(self.__email.get(), self.__password.get(), self.__cinemaName.get())

    def updateBookingStaff(self):
        if self.controller:
            self.controller.updateBookingStaff(self.__email.get(), self.__password.get(), self.__cinemaName.get())

    def deleteBookingStaff(self):
        if self.controller:
            self.controller.deleteBookingStaff(self.__email.get(), self.__password.get(), self.__cinemaName.get())

class ViewAdminFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        
        self.model = ViewAdminModel()
        self.view = self
        self.controller = ViewAdminController(self.model, self.view)
    
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()

    def __createHeaderWithWidgets(self):
        self.header = ttk.Frame(self)
        self.header.grid(row=0)
        self.current_page_label = ttk.Label(self.header, text="View Admin", font=('Helvetica bold', 20))
        self.current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        self.staff_name_label = ttk.Label(self.header, text="Staff Email:")
        self.staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        self.staff_cinema_label = ttk.Label(self.header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        self.staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        self.menu_button = ttk.Button(self.header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        self.menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)
        self.__email = tk.StringVar()
        self.__password = tk.StringVar()
        self.__searchEmail = tk.StringVar()
        self.email_label = ttk.Label(self.content, text="Admin Email:")
        self.email_label.grid(row=0, column=0, pady=20, padx=10)
        self.admin_email_entry = ttk.Entry(self.content, textvariable=self.__email)
        self.admin_email_entry.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        self.password_label = ttk.Label(self.content, text="Admin Password:")
        self.password_label.grid(row=1, column=0, pady=20, padx=10)
        self.admin_password_entry = ttk.Entry(self.content, show="*", textvariable=self.__password)
        self.admin_password_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        self.add_admin_button = ttk.Button(self.content, text="Add Admin", command=self.addAdmin)
        self.add_admin_button.grid(row=4, column=0, pady=20, padx=10)
        self.edit_admin_button = ttk.Button(self.content, text="Edit Admin", command=self.updateAdmin)
        self.edit_admin_button.grid(row=4, column=1, pady=20, padx=10)
        self.remove_admin_button = ttk.Button(self.content, text="Remove Admin", command=self.deleteAdmin)
        self.remove_admin_button.grid(row=4, column=2, pady=20, padx=10)
        self.horizontal_line_label = ttk.Label(self.content, text="-------------------------------------------------------------------------------------------")
        self.horizontal_line_label.grid(row=5, column=0, columnspan=3)
        self.search_label = ttk.Label(self.content, text="Search Details by Email:")
        self.search_label.grid(row=6, column=0, pady=30, padx=10)
        self.search_email_entry = ttk.Entry(self.content, textvariable=self.__searchEmail)
        self.search_email_entry.grid(row=6, column=2, columnspan=2, pady=20, padx=10)
        self.search_email_button = ttk.Button(self.content, text="Search", command=self.searchForAdmin)
        self.search_email_button.grid(row=7, column=0, columnspan=3, pady=10, padx=10)
        
    def searchSuccess(self, message):
        mb.showinfo(title="Admin Account Found:", message="Account Info:"+ str(message))
        self.__email.set(message[0])
        self.__password.set(message[1])
        self.__searchEmail.set('')
        print(message)
    
    def searchFailed(self, message):
        mb.showerror(title="Error:", message=message)
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')

    def addSuccess(self, message):
        mb.showinfo(title="Added Admin:", message="Account Info:" + str(message))
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')
    
    def updateSuccess(self, message):
        mb.showinfo(title="Admin Updated:", message="Updated Info:" + str(message))
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')

    def deleteSuccess(self, message):
        mb.showinfo(title="Admin Deleted:", message="Account with details "+ str(message) + " deleted.")
        self.__searchEmail.set('')
        self.__email.set('')
        self.__password.set('')

    def searchForAdmin(self):
        if self.controller:
            self.controller.searchForAdmin(self.__searchEmail.get())

    def addAdmin(self):
        if self.controller:
            self.controller.addAdmin(self.__email.get(), self.__password.get())

    def updateAdmin(self):
        if self.controller:
            self.controller.updateAdmin(self.__email.get(), self.__password.get())

    def deleteAdmin(self):
        if self.controller:
            self.controller.deleteAdmin(self.__email.get(), self.__password.get())



class ViewFilmFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.createWidgets()

        self.model = ViewFilmModel()
        self.view =  self
        self.controller = ViewFilmController(self.model, self.view)

    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Film", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Email:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)     
        self.filmID = tk.StringVar()
        self.filmName = tk.StringVar()
        self.filmDescription = tk.StringVar()
        self.filmActors = tk.StringVar()
        self.filmGenre = tk.StringVar()
        self.filmAge = tk.StringVar()
        self.filmRating = tk.StringVar()
        self.searchTitle = tk.StringVar()
        self.filmID_label = ttk.Label(self.content, text="Film ID:")
        self.filmID_label.grid(row=0, column=0, pady=10, padx=10)
        self.filmID_entry = ttk.Entry(self.content, textvariable=self.filmID)
        self.filmID_entry.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        self.film_title_label = ttk.Label(self.content, text="Film Title:")
        self.film_title_label.grid(row=1, column=0, pady=10, padx=10)
        self.film_title_entry = ttk.Entry(self.content, textvariable=self.filmName)
        self.film_title_entry.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        self.film_description_label = ttk.Label(self.content, text="Film Description:")
        self.film_description_label.grid(row=2, column=0, pady=10, padx=10)
        self.film_description_entry = ttk.Entry(self.content, textvariable=self.filmDescription)
        self.film_description_entry.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        self.film_actors_label = ttk.Label(self.content, text="Film Actors:")
        self.film_actors_label.grid(row=3, column=0, pady=10, padx=10)
        self.film_actors_entry = ttk.Entry(self.content, textvariable=self.filmActors)
        self.film_actors_entry.grid(row=3, column=1, columnspan=2, pady=10, padx=10)
        self.film_genre_label = ttk.Label(self.content, text="Film Genre:")
        self.film_genre_label.grid(row=4, column=0, pady=10, padx=10)
        self.film_genre_entry = ttk.Entry(self.content, textvariable=self.filmGenre)
        self.film_genre_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        self.film_age_label = ttk.Label(self.content, text="Film Age:")
        self.film_age_label.grid(row=5, column=0, pady=10, padx=10)
        self.film_age_entry = ttk.Entry(self.content, textvariable=self.filmAge)
        self.film_age_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        self.film_rating_label = ttk.Label(self.content, text="Film Rating:")
        self.film_rating_label.grid(row=6, column=0, pady=10, padx=10)
        self.film_rating_entry = ttk.Entry(self.content, textvariable=self.filmRating)
        self.film_rating_entry.grid(row=6, column=1, columnspan=2, pady=10, padx=10)

        self.add_film_button = ttk.Button(self.content, text="Add Film", command=self.addFilm)
        self.add_film_button.grid(row=7, column=0, pady=20, padx=10)
        self.edit_film_button = ttk.Button(self.content, text="Edit Film", command=self.editFilm)
        self.edit_film_button.grid(row=7, column=1, pady=20, padx=10)
        self.remove_film_button = ttk.Button(self.content, text="Remove Film", command=self.deleteFilm)
        self.remove_film_button.grid(row=7, column=2, pady=20, padx=10)
        self.horizontal_line_label = ttk.Label(self.content, text="-------------------------------------------------------------------------------------------")
        self.horizontal_line_label.grid(row=8, column=0, columnspan=3)
        self.search_label = ttk.Label(self.content, text="Search Film Details by Title:")
        self.search_label.grid(row=9, column=0, pady=10, padx=10)
        self.search_title_entry = ttk.Entry(self.content, textvariable=self.searchTitle)
        self.search_title_entry.grid(row=9, column=2, columnspan=2, pady=20, padx=10)
        self.search_title_button = ttk.Button(self.content, text="Search", command=self.searchFilmByTitle)
        self.search_title_button.grid(row=10, column=0, columnspan=3, pady=10, padx=10)
        self.text_fill_label = ttk.Label(self.content, text="""
        



        """)
        self.text_fill_label.grid(row=11, column=0, columnspan=3)


    def searchFailed(self, message):
        mb.showinfo(title="Film Edit Page Failure", message=message)
        print("Film Edit Page failure.")
    
    def addFilmSuccess(self, filmName):
        mb.showinfo(title="Film Added", message= "Film: "+str(filmName)+" Successfully Added To Database.")

    def addFilm(self):
        if self.controller:
            self.controller.addFilm(self.filmName.get(), self.filmDescription.get(), self.filmActors.get(), self.filmGenre.get(), self.filmAge.get(), self.filmRating.get())

    def deleteFilm(self):
        if self.controller:
            self.controller.deleteFilm(self.filmID.get())
        
    def removeFilmSuccess(self, filmID, filmName):
        mb.showinfo(title="Film Removed", message="Film With ID: "+str(filmID)+" Successfully Removed\nAswell As All Screenings With Film Name: "+str(filmName))

    def editFilm(self):
        if self.controller:
            listOfItems = []
            listOfItems.append(self.filmName.get())
            listOfItems.append(self.filmDescription.get())
            listOfItems.append(self.filmActors.get())
            listOfItems.append(self.filmGenre.get())
            listOfItems.append(self.filmAge.get())          
            listOfItems.append(self.filmRating.get())
            self.controller.editFilm(self.filmID.get(), listOfItems)

    def searchFilmByTitle(self):
        if self.controller:
            self.controller.searchFilmByTitle(self.searchTitle.get())

    def filmSearchSuccess(self, film, filmName):
        mb.showinfo(title="Film Found", message="Film Found With Name: "+str(filmName)+"\n"+str(film))
        self.filmID.set(film[0])
        self.filmName.set(film[1])
        self.filmDescription.set(film[2])
        self.filmActors.set(film[3])
        self.filmGenre.set(film[4])
        self.filmAge.set(film[5])
        self.filmRating.set(film[6])
    
    def editFilmSuccess(self, filmID, filmNameOld):
        mb.showinfo(title="Film Updated", message="Film Updated With ID: "+str(filmID)+" Successfully.")
        if self.filmName.get() != "":
            self.controller.updateScreenings(filmNameOld, self.filmName.get())


class AddCinemasFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.createWidgets()

        self.view = self
        self.model = AddCinemasModel()
        self.controller = AddCinemasController(self.model, self.view)
        
    def createWidgets(self):    
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()     
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="Add Cinema/City", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Email:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)
        self.cinemaCity = tk.StringVar()
        self.cinemaName = tk.StringVar()
        self.addCityName = tk.StringVar()
        self.morningPrice = tk.StringVar()
        self.afternoonPrice = tk.StringVar()
        self.eveningPrice = tk.StringVar()
        self.cities = ['select a city']
        self.cinema_city_label = ttk.Label(self.content, text="Cinema City:")
        self.cinema_city_label.grid(row=0, column=0, pady=20, padx=10)
        self.cinema_city_combobox = ttk.Combobox(self.content, textvariable=self.cinemaCity)
        self.cinema_city_combobox.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        self.cinema_city_combobox['values'] = self.cities
        self.cinema_city_combobox['state'] = 'readonly'
        self.cinema_city_combobox.bind("<Enter>", self.cityEnterFunction)
        self.cinema_city_combobox.current(0)
        self.cinema_name_label = ttk.Label(self.content, text="Cinema Name:")
        self.cinema_name_label.grid(row=1, column=0, pady=20, padx=10)
        self.cinema_name_entry = ttk.Entry(self.content, textvariable=self.cinemaName)
        self.cinema_name_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        self.add_cinema_button = ttk.Button(self.content, text="Add Cinema", command=self.addCinemaButton)
        self.add_cinema_button.grid(row=2, column=0, columnspan=3, pady=20, padx=10)
        self.horizontal_line_label = ttk.Label(self.content, text="-------------------------------------------------------------------------------------------")
        self.horizontal_line_label.grid(row=3, column=0, columnspan=3)
        self.city_label = ttk.Label(self.content, text="City Name:")
        self.city_label.grid(row=4, column=0, pady=20, padx=10)
        self.city_entry = ttk.Entry(self.content, textvariable=self.addCityName)
        self.city_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        self.city_morning_price_label = ttk.Label(self.content, text="Morning Price:")
        self.city_morning_price_label.grid(row=5, column=0, pady=10, padx=10)
        self.city_morning_price_entry = ttk.Entry(self.content, textvariable=self.morningPrice)
        self.city_morning_price_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        self.city_afternoon_price_label = ttk.Label(self.content, text="Afternoon Price:")
        self.city_afternoon_price_label.grid(row=6, column=0, pady=10, padx=10)
        self.city_afternoon_price_entry = ttk.Entry(self.content, textvariable=self.afternoonPrice)
        self.city_afternoon_price_entry.grid(row=6, column=1, columnspan=2, pady=10, padx=10)
        self.city_evening_price_label = ttk.Label(self.content, text="Evening Price:")
        self.city_evening_price_label.grid(row=7, column=0, pady=10, padx=10)
        self.city_evening_price_entry = ttk.Entry(self.content, textvariable=self.eveningPrice)
        self.city_evening_price_entry.grid(row=7, column=1, columnspan=2, pady=10, padx=10)
        self.add_city_button = ttk.Button(self.content, text="Add City", command=self.addCity)
        self.add_city_button.grid(row=8, column=0, columnspan=3, pady=10, padx=10)


    def cityEnterFunction(self, city):
        self.cities = []
        if self.controller:
            cities = self.controller.getCities()
            for city in cities:
               self.cities.append(city[1])
            self.cinema_city_combobox['values'] = self.cities

    def seacrhFailed(self, message):
        mb.showinfo(title="City/Cinema Page Error", message=message)

    def addCinemaButton(self):
        if self.controller:
            self.controller.addCinema(self.cinemaCity.get(), self.cinemaName.get())

    def addCinemaSuccess(self, cityName, cinemaName):
        message = "Cinema Successfully Added with name: "+str(cinemaName)+" in the city: "+str(cityName)
        self.cinema_name_entry.delete(0, 'end')
        mb.showinfo(title="Cinema Added Successfully", message=message)
    
    def addCity(self):
        if self.controller:
            self.controller.addCity(self.addCityName.get(), self.morningPrice.get(), self.afternoonPrice.get(), self.eveningPrice.get())

    def addCitySuccess(self, cityName, morningPrice, afternoonPrice, eveningPrice):
        message = "City Added Successfully Added with name: "+str(cityName)+"\nmorning price: £"+str(morningPrice)+"\nafternoon price: £"+str(afternoonPrice)+"\nevening price: £"+str(eveningPrice)
        self.city_entry.delete(0, 'end')
        self.city_morning_price_entry.delete(0, 'end')
        self.city_afternoon_price_entry.delete(0, 'end')
        self.city_evening_price_entry.delete(0, 'end')
        mb.showinfo(title="City Added Successfully", message=message)

    def searchFailed(self, messgae):
        mb.showinfo(title="City/Cinema Add Failed", message=messgae)

class GenerateReportFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self.model = GenerateReportModel()
        self.view = self
        self.controller = GenerateReportController(self.model, self.view)
    
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):

        self.header = ttk.Frame(self)
        self.header.grid(row=0)
        self.current_page_label = ttk.Label(self.header, text="Generate Report", font=('Helvetica bold', 20))
        self.current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        self.staff_name_label = ttk.Label(self.header, text="Staff Name:")
        self.staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        self.staff_cinema_label = ttk.Label(self.header, text=currentUser.getEmail())
        self.staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        self.menu_button = ttk.Button(self.header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        self.menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)
        self.__reportType = tk.StringVar()
        self.__reportParameter = tk.StringVar()
        self.filler_label = ttk.Label(self.content, text="""
        
        
        
        
        
        """)
        self.filler_label.grid(row=0, column=0)
        self.report_information_label = ttk.Label(self.content, text="""
        Report ID 1: List of Staff for a Given Cinema Name. (Parameter = Cinema Name)
        Report ID 2: Number of Bookings for a Screening. (Parameter: Screening ID)
        Report ID 3: Show films and the Number of Bookings. (Parameter: N/A)
        """, font=('Helvetica bold', 10))
        self.report_information_label.grid(row=1, column=0, columnspan=3, sticky=tk.N)
        self.generate_report_label = ttk.Label(self.content, text="Enter Report ID:")
        self.generate_report_label.grid(row=2, column=0, pady=10, padx=10)
        self.generate_report_entry = ttk.Entry(self.content, textvariable=self.__reportType)
        self.generate_report_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.report_parameter_label = ttk.Label(self.content, text="Enter Report Parameter:")
        self.report_parameter_label.grid(row=3, column=0, pady=10, padx=10)
        self.report_parameter_entry = ttk.Entry(self.content, textvariable=self.__reportParameter)
        self.report_parameter_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.generate_report_button = ttk.Button(self.content, text="Generate Report", command=self.generateReport)
        self.generate_report_button.grid(row=4, column=0, columnspan=3)
        self.report_listbox = tk.Listbox(self)
        self.report_listbox.place(height=250, width=450, x=500, y=100)

    def generateSuccess(self, message, reportInfo, reportType):
        self.report_listbox.delete(0, tk.END)
        mb.showinfo(title="Report Generating:", message=message)
        if reportType == "1":
            self.report1Title = "Report to Show the Staff for a Given Cinema Name."
            self.report1Headings = "Staff Email: Staff Cinema:"
            self.report_listbox.insert(tk.END, self.report1Title)
            self.report_listbox.insert(tk.END, self.report1Headings)
        elif reportType == "2":
            self.report2Title = "Report to Show the Number of Bookings for a Given Screening."
            self.report2Headings = "Screening ID: Number of Bookings:"
            self.report_listbox.insert(tk.END, self.report2Title)
            self.report_listbox.insert(tk.END, self.report2Headings)
        elif reportType == "3":
            self.report3Title = "Report to Show Films and the Number of Bookings."
            self.report3Headings = "Film Name: Number of Bookings:"
            self.report_listbox.insert(tk.END, self.report3Title)
            self.report_listbox.insert(tk.END, self.report3Headings)
        for row in reportInfo:
            self.report_listbox.insert(tk.END, row)

    def generateFailed(self, message):
        self.__reportType.set('')
        self.__reportParameter.set('')
        mb.showerror(title="Failed to Generate Report:", message=message)

    def generateReport(self,):
        if self.controller:
            self.controller.generateReport(self.__reportType.get(), self.__reportParameter.get())


        
class ViewFilmListingsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self.model = ViewFilmListingsModel()
        self.view =  self
        self.controller = ViewFilmListingsController(self.model, self.view)

        self.createWidgets()
      
        
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
    
    def __createHeaderWithWidgets(self):
        self.header = ttk.Frame(self)
        self.header.grid(row=0)
        self.current_page_label = ttk.Label(self.header, text="View Film Listings", font=('Helvetica bold', 20))
        self.current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        self.staff_name_label = ttk.Label(self.header, text="Staff Email:")
        self.staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        self.staff_cinema_label = ttk.Label(self.header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        self.staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        self.menu_button = ttk.Button(self.header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        self.menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)
        self.__filmName = tk.StringVar()
        self.__cinemaName = tk.StringVar()

        
        self.film_name_label = ttk.Label(self.content, text="Film Name:")
        self.film_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.film_name_entry = ttk.Entry(self.content, textvariable=self.__filmName)
        self.film_name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        self.cinema_name_label = ttk.Label(self.content, text="Cinema Name:")
        self.cinema_name_label.grid(row=1, column=0, padx=10, pady=10)
        self.cinema_name_entry = ttk.Entry(self.content, textvariable=self.__cinemaName)
        self.cinema_name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        self.show_listings_button = ttk.Button(self.content, text="Show Films/ Listings", command=self.searchListings)
        self.show_listings_button.grid(row=2, column=0, columnspan=3)
        self.text_fill_label = ttk.Label(self.content, text="""








        


        """)
        self.text_fill_label.grid(row=3, column=0, columnspan=3)
        self.listings_listbox = tk.Listbox(self)
        self.listings_listbox.place(height=300, width=200, x=583, y=400)
        self.listboxHeadings = "Time: Date: Screen:"
        self.listings_listbox.insert(0, self.listboxHeadings)

        if currentUser.getAccountType() == 0:
            self.__cinemaName.set(currentUser.getAccountCinema())
            self.cinema_name_entry.configure(state='disabled')  

    def searchSuccess(self, message, screeningInfo):
        self.listings_listbox.delete(1, tk.END)
        mb.showinfo(title="Search Success", message= message)
        for row in screeningInfo:
            self.listings_listbox.insert(tk.END, row)

    def searchFailed(self, message):
        self.__filmName.set('')
        if currentUser.getAccountType() != 0:
            self.__cinemaName.set('')
        mb.showerror(title="Search Failed", message=message)
    
    def filmListboxFunction(self, flim):
        film = self.listings_listbox.get(self.listings_listbox.curselection())
        self.film_name_entry.insert(0, film[0])

    def listingsListboxFunction(self, lsiting):
        listing = self.listings_listbox.get(self.listings_listbox.curselection())
        print(listing)

    def searchListings(self):
        if self.controller:
            if self.__filmName.get() == '':
                self.listings_listbox.delete(0, tk.END)
                self.listings_listbox.insert(tk.END, "films at "+str(self.__cinemaName.get()))
                self.controller.searchFilms(self.__cinemaName.get())
                self.listings_listbox.bind("<<ListboxSelect>>", self.filmListboxFunction)
            else:
                self.listings_listbox.delete(0, tk.END)
                self.listings_listbox.insert(tk.END, self.listboxHeadings)
                self.controller.searchListings(self.__filmName.get(), self.__cinemaName.get())
                self.listings_listbox.bind("<<ListboxSelect>>", self.listingsListboxFunction)

class CreateBookingFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self.model = CreateBookingModel()
        self.view =  self
        self.controller = CreateBookingController(self.model, self.view)
        self.createWidgets()

    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets() 
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="Create Booking", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Email:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)

        self.bookingDate = tk.StringVar()
        self.bookingFilm = tk.StringVar()
        self.bookingShowing = tk.StringVar()
        self.bookingSeatType = tk.IntVar()
        self.bookingNumOfTickets = tk.IntVar()
        self.bookingCustomerName = tk.StringVar()
        self.bookingCustomerPhone = tk.StringVar()
        self.bookingCustomerEmail = tk.StringVar()
        self.bookingCardNum = tk.IntVar()
        self.bookingExpiry = tk.StringVar()
        self.bookingCVV = tk.IntVar()
        self.cinemaName = tk.StringVar()
        self.price = tk.IntVar()


        
        self.films = ['select movie', 'select cinema on home page']
        self.select_film_label = ttk.Label(content, text="Select Film:")
        self.select_film_label.grid(row=0, column=0, padx=10, pady=(0, 40))
        self.select_film_combobox = ttk.Combobox(content, textvariable=self.bookingFilm)
        self.select_film_combobox.grid(row=0, column=1, padx=5, pady=(0, 40))
        self.select_film_combobox['values'] = self.films
        self.select_film_combobox['state'] = 'readonly'
        self.select_film_combobox.bind("<Enter>", self.comboboxHoverFunction) #new event <Enter> changes combobox when hovered over and not when selected
        self.select_film_combobox.bind("<<ComboboxSelected>>", self.filmComboboxFunction)
        self.select_film_combobox.current(0)

        self.dates = ('select movie') 
        self.select_date_label = ttk.Label(content, text="Select Date:")
        self.select_date_label.grid(row=0, column=2, padx=5, pady=(0, 40))
        self.select_date_combobox = ttk.Combobox(content, textvariable=self.bookingDate)
        self.select_date_combobox.grid(row=0, column=3, padx=5, pady=(0, 40))
        self.select_date_combobox['values'] = self.dates
        self.select_date_combobox['state'] = 'readonly'  
        self.select_date_combobox.bind("<<ComboboxSelected>>", self.dateComboboxFunction) 
        self.select_date_combobox.current(0) 

        self.showings = ('select date')
        self.select_showing_label = ttk.Label(content, text="Select Showing:")
        self.select_showing_label.grid(row=0, column=4, padx=10, pady=(0, 40))
        self.select_showing_combobox = ttk.Combobox(content, textvariable=self.bookingShowing)
        self.select_showing_combobox.grid(row=0, column=5, padx=5, pady=(0, 40))
        self.select_showing_combobox['values'] = self.showings
        self.select_showing_combobox['state'] = 'readonly'
        self.select_showing_combobox.current(0)

        self.select_ticket_type_label = ttk.Label(content, text="Select Ticket Type:")
        self.select_ticket_type_label.grid(row=1, column=0, padx=5, pady=(0, 40))
        self.lower_hall_ticket_radio_button = ttk.Radiobutton(content, text="Lower Hall", value=1, variable=self.bookingSeatType)
        self.lower_hall_ticket_radio_button.grid(row=1, column=1, padx=5, pady=(0, 40))
        self.upper_hall_ticket_radio_button = ttk.Radiobutton(content, text="Upper Hall", value=2, variable=self.bookingSeatType)
        self.upper_hall_ticket_radio_button.grid(row=1, column=2, padx=5, pady=(0, 40))
        self.VIP_ticket_radio_button = ttk.Radiobutton(content, text="VIP", value=3, variable=self.bookingSeatType)
        self.VIP_ticket_radio_button.grid(row=1, column=3, padx=5, pady=(0, 40))

        self.booking_num_of_tickets_label = ttk.Label(content, text="Number of Tickets:")
        self.booking_num_of_tickets_label.grid(row=1, column=4, padx=5, pady=(0, 40))
        self.booking_num_of_ticekts_entry = ttk.Entry(content, textvariable=self.bookingNumOfTickets)
        self.booking_num_of_ticekts_entry.grid(row=1, column=5, padx=5, pady=(0, 40))

        self.check_availability_price_button = ttk.Button(content, text="Check Availability/Price", command=self.checkAvailabilityAndPrice)
        self.check_availability_price_button.grid(row=2, column=0, columnspan=6, padx=5, pady=(0, 80))

        customer_name_label = ttk.Label(content, text="Customer Name:")
        customer_name_label.grid(row=3, column=0,padx=5, pady=(0, 40))
        customer_name_entry = ttk.Entry(content, textvariable=self.bookingCustomerName)
        customer_name_entry.grid(row=3, column=1, padx=5, pady=(0, 40))

        customer_phone_label = ttk.Label(content, text="Customer Phone:")
        customer_phone_label.grid(row=3, column=2,padx=5, pady=(0, 40))
        customer_phone_entry = ttk.Entry(content, textvariable=self.bookingCustomerPhone)
        customer_phone_entry.grid(row=3, column=3, padx=5, pady=(0, 40))

        customer_email_label = ttk.Label(content, text="Customer Email:")
        customer_email_label.grid(row=3, column=4, padx=5, pady=(0, 40))
        customer_email_entry = ttk.Entry(content, textvariable=self.bookingCustomerEmail)
        customer_email_entry.grid(row=3, column=5, padx=5, pady=(0, 40))

        card_num_label = ttk.Label(content, text="Card #:")
        card_num_label.grid(row=4, column=0, padx=5, pady=(0, 40))
        card_num_entry = ttk.Entry(content, textvariable=self.bookingCardNum)
        card_num_entry.grid(row=4, column=1, padx=5, pady=(0, 40))

        card_exp_label = ttk.Label(content, text="Card Expiry:")
        card_exp_label.grid(row=5, column=0, padx=5, pady=(0, 40))
        card_exp_entry = ttk.Entry(content, textvariable=self.bookingExpiry)
        card_exp_entry.grid(row=5, column=1, padx=5, pady=(0, 40))

        cvv_label = ttk.Label(content, text="CVV:")
        cvv_label.grid(row=5, column=2, padx=5, pady=(0, 40))
        cvv_entry = ttk.Entry(content, textvariable=self.bookingCVV)
        cvv_entry.grid(row=5, column=3, padx=5, pady=(0, 40))

        self.create_booking_button = ttk.Button(content, text="Create Booking/Get Receipt", command=self.createBooking)
        self.create_booking_button.grid(row=6, column=0, columnspan=6, padx=5, pady=(0, 80))

        if currentUser.getAccountType() == 0:
            self.cinemaName.set(currentUser.getAccountCinema())

    def filmSearchSuccess(self, message, films):
        #resets list so doesnt show 'click me'
        self.films = []
        #adds fetched films to combobox list
        for film in films:
            self.films.append(film[0])
            
    def searchFailed(self, message):
        self.bookingFilm.set('')
        if currentUser.getAccountType() != 0:
            self.cinemaName.set('')
        mb.showerror(title="Search Failed", message=message)
    
    def searchFilms(self):
        if self.controller:
            self.controller.searchFilm(currentUser.getAccountCinema())

    #function with joins 2 functions together so both happen on <Enter> (when hovered over) event   
    def comboboxHoverFunction(self, film):
        self.searchFilms()
        self.select_film_combobox['values'] = self.films

    def dateSearchSuccess(self, message, dates):
        self.dates = []
        for date in dates:
            self.dates.append(date[0])

    def searchDates(self):
        if self.controller:
            self.controller.searchDates(self.bookingFilm.get(), currentUser.getAccountCinema())
    
    def updateDateCombobox(self):
        self.select_date_combobox['values'] = self.dates

    #function for <<ComboboxSelected>> event on the film combobox
    def filmComboboxFunction(self, film):
        self.searchDates()
        self.updateDateCombobox()
    
    def showingSearchSuccess(self, message, showings):
        self.showings = []
        for show in showings:
            self.showings.append(show[0])
    
    def searchShowings(self):
        if self.controller:
            self.controller.searchShowings(self.bookingDate.get(), self.bookingFilm.get(), currentUser.getAccountCinema())

    def updateShowingsCombobox(self):
        self.select_showing_combobox['values'] = self.showings

    #function for <<ComboboxSelected>> event on the dates combobox
    def dateComboboxFunction(self, film):
        self.searchShowings()
        self.updateShowingsCombobox()
    
    def priceSuccess(self, message, price):
        self.price = price
        message = message + "\nTotal price: " + str(price)
        mb.showinfo(title="Availability and Price", message =message)

    def checkPrice(self, message):
        if self.controller:
            self.controller.checkPrice(self.bookingNumOfTickets.get(), self.bookingSeatType.get(), self.bookingShowing.get(), self.bookingDate.get(), self.bookingFilm.get(), currentUser.getAccountCinema(), message)

    def availabilityFailed(self, message, tickets):
        message = message + "\nlower tickets available: " + str(tickets[0][0]) + "\nupper ticekts available: " + str(tickets[0][1]) + "\nVIP tickets available: " + str(tickets[0][2])
        mb.showinfo(title="Availability Failure", message= message)

    def checkAvailability(self):
        if self.controller:
            self.controller.checkAvailability(self.bookingNumOfTickets.get(), self.bookingSeatType.get(), self.bookingShowing.get(), self.bookingDate.get(), self.bookingFilm.get(), currentUser.getAccountCinema())

    def checkAvailabilityAndPrice(self):
        self.checkAvailability()
    
    def createBooking(self):
        if self.controller:
            self.controller.createBooking(self.bookingSeatType.get(), self.price, self.bookingNumOfTickets.get(), self.bookingShowing.get(), self.bookingDate.get(), self.bookingFilm.get(), currentUser.getAccountCinema())
        
    def showBooking(self, bookingID, ticketSeats, price, numOfTickets, time, date, film, cinema, screeningScreen):
        message = '''
        -------------------BOOKING RECIEPT-------------------\n
        BookingID = '''+str(bookingID)+'''     \n 
        Film Name = '''+str(film)+'''       \n
        Screening Date = '''+str(date)+'''   \n
        Screening Time = '''+str(time)+''' \n
        Cinema = '''+str(cinema)+'''\n
        Screen = '''+str(screeningScreen)+'''              \n
        Number of Tickets = '''+str(numOfTickets)+''' \n
        Seat Numbers = '''+str(ticketSeats)+''' \n
        Cost = £'''+str(price)+''' \n
        '''
        mb.showinfo(title="Booking Reciept", message=message)
        print("booking function")
        app.showFrame("HomeFrame")
        



class CancelBookingFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.createWidgets()

        self.model = CancelBookingModel()
        self.view =  self
        self.controller = CancelBookingController(self.model, self.view)
        
    
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()

    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="Cancel Booking", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Email:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)

        self.bookingID = tk.StringVar()

        self.booking_id_label = ttk.Label(content, text="Booking ID:")
        self.booking_id_label.grid(row=0, column=0, padx=5, pady=(0, 100))
        self.booking_id_entry = ttk.Entry(content, textvariable=self.bookingID)
        self.booking_id_entry.grid(row=0, column=1, padx=5, pady=(0, 100))

        self.cancel_booking_button = ttk.Button(content, text="Cancel Booking", command=self.cancelBooking)
        self.cancel_booking_button.grid(row=1, column=0, columnspan=2)

    def cancelBooking(self):
        if self.controller:
            self.controller.cancelBooking(self.bookingID.get())
        
    def cancelSuccess(self, message):
        mb.showinfo(title="Booking Cancelled", message=message)
        print("Booking Cancelled.")
        app.showFrame("HomeFrame")
    
    def searchFailed(self, message):
        mb.showinfo(title="Booking Cancellation Failure", message=message)
        print("booking cancellation failure")


class ViewCinemaScreeningsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.createWidgets()

        self.model = ViewCinemaScreeningsModel()
        self.view =  self
        self.controller = ViewCinemaScreeningsController(self.model, self.view)
    
    def createWidgets(self):
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()       
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Screenings", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Email:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text= currentUser.getEmail() + " [" + currentUser.getAccountCinema()+"]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1)     
        self.screeningID = tk.StringVar()
        self.screeningTime = tk.StringVar()
        self.screeningDate = tk.StringVar()
        self.screeningScreen = tk.StringVar()
        self.cinemaName = tk.StringVar()
        self.filmName = tk.StringVar()
        self.LHTickets = tk.StringVar()
        self.UHTickets = tk.StringVar()
        self.VIPTickets = tk.StringVar()
        self.searchID = tk.StringVar()
        self.screeningID_label = ttk.Label(self.content, text="Screening ID:")
        self.screeningID_label.grid(row=0, column=0, pady=10, padx=10)
        self.screeningID_entry = ttk.Entry(self.content, textvariable=self.screeningID)
        self.screeningID_entry.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        self.screening_time_label = ttk.Label(self.content, text="Time:")
        self.screening_time_label.grid(row=1, column=0, pady=10, padx=10)
        self.screening_time_entry = ttk.Entry(self.content, textvariable=self.screeningTime)
        self.screening_time_entry.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        self.screening_date_label = ttk.Label(self.content, text="Date:")
        self.screening_date_label.grid(row=2, column=0, pady=10, padx=10)
        self.screening_date_entry = ttk.Entry(self.content, textvariable=self.screeningDate)
        self.screening_date_entry.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        self.screening_screen_label = ttk.Label(self.content, text="Screen:")
        self.screening_screen_label.grid(row=3, column=0, pady=10, padx=10)
        self.screening_screen_entry = ttk.Entry(self.content, textvariable=self.screeningScreen)
        self.screening_screen_entry.grid(row=3, column=1, columnspan=2, pady=10, padx=10)
        self.cinema_name_label = ttk.Label(self.content, text="Cinema Name:")
        self.cinema_name_label.grid(row=4, column=0, pady=10, padx=10)
        self.cinema_name_entry = ttk.Entry(self.content, textvariable=self.cinemaName)
        self.cinema_name_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        self.film_name_label = ttk.Label(self.content, text="Film Name:")
        self.film_name_label.grid(row=5, column=0, pady=10, padx=10)
        self.film_name_entry = ttk.Entry(self.content, textvariable=self.filmName)
        self.film_name_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        self.LH_tickets_label = ttk.Label(self.content, text="Lower Hall Tickets:")
        self.LH_tickets_label.grid(row=6, column=0, pady=10, padx=10)
        self.LH_tickets_entry = ttk.Entry(self.content, textvariable=self.LHTickets)
        self.LH_tickets_entry.grid(row=6, column=1, columnspan=2, pady=10, padx=10)
        self.UH_tickets_label = ttk.Label(self.content, text="Upper Hall Tickets:")
        self.UH_tickets_label.grid(row=7, column=0, pady=10, padx=10)
        self.UH_tickets_entry = ttk.Entry(self.content, textvariable=self.LHTickets)
        self.UH_tickets_entry.grid(row=7, column=1, columnspan=2, pady=10, padx=10)
        self.VIP_tickets_label = ttk.Label(self.content, text="VIP Tickets:")
        self.VIP_tickets_label.grid(row=8, column=0, pady=10, padx=10)
        self.VIP_tickets_entry = ttk.Entry(self.content, textvariable=self.LHTickets)
        self.VIP_tickets_entry.grid(row=8, column=1, columnspan=2, pady=10, padx=10)

        self.add_screening_button = ttk.Button(self.content, text="Add Screening", command=self.addScreening)
        self.add_screening_button.grid(row=9, column=0, pady=20, padx=10)
        self.edit_screening_button = ttk.Button(self.content, text="Edit Screening", command=self.editScreening)
        self.edit_screening_button.grid(row=9, column=1, pady=20, padx=10)
        self.remove_screening_button = ttk.Button(self.content, text="Remove Screening", command=self.deleteScreening)
        self.remove_screening_button.grid(row=9, column=2, pady=20, padx=10)
        self.horizontal_line_label = ttk.Label(self.content, text="-------------------------------------------------------------------------------------------")
        self.horizontal_line_label.grid(row=10, column=0, columnspan=3)
        self.search_label = ttk.Label(self.content, text="Search Screening by ID:")
        self.search_label.grid(row=11, column=0, pady=10, padx=10)
        self.search_ID_entry = ttk.Entry(self.content, textvariable=self.searchID)
        self.search_ID_entry.grid(row=11, column=1, pady=20, padx=10)
        self.search_ID_button = ttk.Button(self.content, text="Search", command=self.searchScreeningByID)
        self.search_ID_button.grid(row=11, column=2, columnspan=2, pady=10, padx=10)
        self.text_fill_label = ttk.Label(self.content, text="""
        



        """)
        self.text_fill_label.grid(row=11, column=0, columnspan=3)


    def searchFailed(self, message):
        mb.showinfo(title="Screening Edit Page Failure", message=message)
        print("Screening Edit Page failure.")
    
    def addScreeningSuccess(self, filmName, time, date):
        mb.showinfo(title="Screening Added", message= "Screening Added For Film: "+str(filmName)+" At Time: "+str(time)+" On: "+str(date)+" Successfully Added To Database.")

    def addScreening(self):
        if self.controller:
            self.controller.addScreening(self.screeningTime.get(), self.screeningDate.get(), self.screeningScreen.get(), self.cinemaName.get(), self.filmName.get(), self.LHTickets.get(), self.UHTickets.get(), self.VIPTickets.get())

    def deleteScreening(self):
        if self.controller:
            self.controller.deleteScreening(self.screeningID.get())
        
    def removeScreeningSuccess(self, screeningID):
        mb.showinfo(title="Screening Removed", message="Screening With ID: "+str(screeningID)+" Successfully Removed")

    def editScreening(self):
        if self.controller:
            listOfItems = []
            listOfItems.append(self.screeningTime.get())
            listOfItems.append(self.screeningDate.get())
            listOfItems.append(self.screeningScreen.get())
            listOfItems.append(self.cinemaName.get())
            listOfItems.append(self.filmName.get())
            listOfItems.append(self.LHTickets.get())
            listOfItems.append(self.UHTickets.get())          
            listOfItems.append(self.VIPTickets.get())
            self.controller.editScreening(self.screeningID.get(), listOfItems)

    def searchScreeningByID(self):
        if self.controller:
            self.controller.searchScreeningByID(self.searchID.get())

    def screeningSearchSuccess(self, screening, screeningID):
        mb.showinfo(title="Screening Found", message="Screening Found With ID: "+str(screeningID)+"\n"+str(screening))
        self.screeningID.set(screening[0])
        self.screeningTime.set(screening[1])
        self.screeningDate.set(screening[2])
        self.screeningScreen.set(screening[3])
        self.cinemaName.set(screening[4])
        self.filmName.set(screening[5])
        self.LHTickets.set(screening[6])
        self.UHTickets.set(screening[7])
        self.VIPTickets.set(screening[8])
    
    def editScreeningSuccess(self, screeningID):
        mb.showinfo(title="Screening Updated", message="Screening Updated With ID: "+str(screeningID)+" Successfully.")

class CurrentUser:
    def __init__(self, email, accountType, accountCinema = None):
        self.email = email
        self.accountType = accountType
        if accountCinema is not None:
            self.accountCinema = accountCinema

    def getEmail(self):
        return self.email
    
    def getAccountType(self):
        return self.accountType

    def getAccountCinema(self):
        return self.accountCinema

    def setEmail(self, email):
        self.email = email

    def setAccountType(self, accountType):
        self.accountType = accountType

    def setAccountCinema(self, accountCinema):
        self.accountCinema = accountCinema


if __name__ == "__main__":
    currentUser = CurrentUser("default", 0, "default")
    app = App()
    app.mainloop()