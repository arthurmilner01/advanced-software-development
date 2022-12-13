import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb


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

        for F in (LoginFrame, HomeFrame, ViewBookingStaffFrame, ViewAdminFrame, ViewFilmFrame, ViewCinemasFrame):
            frameName = F.__name__
            frame = F(self)
            self.frames[frameName] = frame

            #Placing each frame so that they are ready to be used with tkraise as appropriate
            frame.place(height=768, width=1366)

        self.showFrame("LoginFrame")

    # Function which will raise the given frame to the front of the GUI
    def showFrame(self, frameName):
        frame = self.frames[frameName]
        frame.tkraise()

class LoginFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__createWidgets()

    def __createWidgets(self):
        email = tk.StringVar()
        password = tk.StringVar()
        login_title_label = ttk.Label(self, text="Login", font=('Helvetica bold', 26), foreground="white")
        login_title_label.grid(columnspan=3, row=0, padx=5, pady=5)
        email_label = ttk.Label(self, text="Username:")
        email_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        email_entry = ttk.Entry(self, textvariable=email)
        email_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
        password_entry = ttk.Entry(self, textvariable=password, show="*")
        password_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
        login_button = ttk.Button(self, text="Login", command=lambda : self.validateLogin(email, password, email_entry, password_entry))
        login_button.grid(columnspan=2, row=3, padx=10, pady=10)
    
    def validateLogin(self, email, password, email_entry, password_entry):
        email_entry.configure(foreground="red")
        password_entry.configure(foreground="red")
        failed_login_label = ttk.Label(self, text="Forgotten your password? Please call over an admin to mediate this issue.", font=("Helvetica bold itallic", 8)).grid(columnspan=2, row=4, padx=10, pady=10)
        app.showFrame("HomeFrame")



class HomeFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.__createWidgets()

    def __createWidgets(self):
        horizon_cinema_label = ttk.Label(self, text="Horizon Cinemas", font=('Helvetica bold', 15))
        horizon_cinema_label.grid(column=0,row=1)
        current_user_label = ttk.Label(self, text="Staff Name [Staff Type]", font=('Helvetica bold', 15))
        current_user_label.grid(column=0,row=2)
        listings_button = ttk.Button(self, text="View Film Listings")
        listings_button.grid(column=1, row=1, padx=10, pady=20, sticky=tk.W)
        create_booking_button = ttk.Button(self, text="Create Booking")
        create_booking_button.grid(column=2, row=1, padx=10, pady=20)
        cancel_booking_button = ttk.Button(self, text="Cancel Booking")
        cancel_booking_button.grid(column=3, row=1, padx=10, pady=20)
        generate_report_button = ttk.Button(self, text="Generate Report")
        generate_report_button.grid(column=4, row=1, padx=10, pady=20, sticky=tk.E)
        view_booking_staff_button = ttk.Button(self, command=lambda : app.showFrame("ViewBookingStaffFrame"), text="View Booking Staff")
        view_booking_staff_button.grid(column=1, row=2, padx=10, pady=20, sticky=tk.W)
        view_admin_button = ttk.Button(self, command=lambda : app.showFrame("ViewAdminFrame"), text="View Admin Staff")
        view_admin_button.grid(column=2, row=2, padx=10, pady=20)
        view_cinema_button = ttk.Button(self, command=lambda : app.showFrame("ViewCinemasFrame"), text="View Cinemas")
        view_cinema_button.grid(column=3, row=2, padx=10, pady=20)
        view_film_button = ttk.Button(self, command=lambda : app.showFrame("ViewFilmFrame"), text="View Film")
        view_film_button.grid(column=4, row=2, padx=10, pady=20, sticky=tk.E)
        view_screenings_button = ttk.Button(self, text="View Cinema Screenings")
        view_screenings_button.grid(column=1, row=3, padx=10, pady=20, sticky=tk.W)
        generate_report_button = ttk.Button(self, text="Generate Report")
        generate_report_button.grid(column=2, row=3, padx=10, pady=20)
        logout_button = ttk.Button(self, command=lambda : app.showFrame("LoginFrame"), text="Logout")
        logout_button.grid(column=3, columnspan=2, row=3, padx=10, pady=20, sticky=tk.E)

class ViewBookingStaffFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Booking Staff", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)
        email = tk.StringVar()
        password = tk.StringVar()
        cinemaName = tk.StringVar()
        searchEmail = tk.StringVar()
        email_label = ttk.Label(content, text="Booking Staff Email:")
        email_label.grid(row=0, column=0, pady=20, padx=10)
        booking_staff_email_entry = ttk.Entry(content, textvariable=email)
        booking_staff_email_entry.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        password_label = ttk.Label(content, text="Booking Staff Password:")
        password_label.grid(row=1, column=0, pady=20, padx=10)
        booking_staff_password_entry = ttk.Entry(content, textvariable=password)
        booking_staff_password_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        cinema_name_label = ttk.Label(content, text="Booking Staff Cinema:")
        cinema_name_label.grid(row=2, column=0, pady=20, padx=10)
        booking_staff_cinema_name_entry = ttk.Entry(content, textvariable=cinemaName)
        booking_staff_cinema_name_entry.grid(row=2, column=1, columnspan=2, pady=20, padx=10)
        add_booking_staff_button = ttk.Button(content, text="Add Booking Staff")
        add_booking_staff_button.grid(row=4, column=0, pady=20, padx=10)
        edit_booking_staff_button = ttk.Button(content, text="Edit Booking Staff")
        edit_booking_staff_button.grid(row=4, column=1, pady=20, padx=10)
        remove_booking_staff_button = ttk.Button(content, text="Remove Booking Staff")
        remove_booking_staff_button.grid(row=4, column=2, pady=20, padx=10)
        horizontal_line_label = ttk.Label(content, text="-------------------------------------------------------------------------------------------")
        horizontal_line_label.grid(row=5, column=0, columnspan=3)
        search_label = ttk.Label(content, text="Search Details by Email:")
        search_label.grid(row=6, column=0, pady=30, padx=10)
        search_email_entry = ttk.Entry(content, textvariable=searchEmail)
        search_email_entry.grid(row=6, column=2, columnspan=2, pady=20, padx=10)
        search_email_button = ttk.Button(content, text="Search")
        search_email_button.grid(row=7, column=0, columnspan=3, pady=10, padx=10)

class ViewAdminFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Admin", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)
        email = tk.StringVar()
        password = tk.StringVar()
        searchEmail = tk.StringVar()
        email_label = ttk.Label(content, text="Admin Email:")
        email_label.grid(row=0, column=0, pady=20, padx=10)
        admin_email_entry = ttk.Entry(content, textvariable=email)
        admin_email_entry.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        password_label = ttk.Label(content, text="Admin Password:")
        password_label.grid(row=1, column=0, pady=20, padx=10)
        admin_password_entry = ttk.Entry(content, textvariable=password)
        admin_password_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        add_admin_button = ttk.Button(content, text="Add Admin")
        add_admin_button.grid(row=4, column=0, pady=20, padx=10)
        edit_admin_button = ttk.Button(content, text="Edit Admin")
        edit_admin_button.grid(row=4, column=1, pady=20, padx=10)
        remove_admin_button = ttk.Button(content, text="Remove Admin")
        remove_admin_button.grid(row=4, column=2, pady=20, padx=10)
        horizontal_line_label = ttk.Label(content, text="-------------------------------------------------------------------------------------------")
        horizontal_line_label.grid(row=5, column=0, columnspan=3)
        search_label = ttk.Label(content, text="Search Details by Email:")
        search_label.grid(row=6, column=0, pady=30, padx=10)
        search_email_entry = ttk.Entry(content, textvariable=searchEmail)
        search_email_entry.grid(row=6, column=2, columnspan=2, pady=20, padx=10)
        search_email_button = ttk.Button(content, text="Search")
        search_email_button.grid(row=7, column=0, columnspan=3, pady=10, padx=10)

class ViewFilmFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Film", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)
        filmID = tk.StringVar()
        filmName = tk.StringVar()
        filmDescription = tk.StringVar()
        filmActors = tk.StringVar()
        filmGenre = tk.StringVar()
        filmAge = tk.StringVar()
        filmRating = tk.StringVar()
        searchTitle = tk.StringVar()
        filmID_label = ttk.Label(content, text="Film ID:")
        filmID_label.grid(row=0, column=0, pady=10, padx=10)
        filmID_entry = ttk.Entry(content, textvariable=filmID)
        filmID_entry.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        film_title_label = ttk.Label(content, text="Film Title:")
        film_title_label.grid(row=1, column=0, pady=10, padx=10)
        film_title_entry = ttk.Entry(content, textvariable=filmName)
        film_title_entry.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        film_description_label = ttk.Label(content, text="Film Description:")
        film_description_label.grid(row=2, column=0, pady=10, padx=10)
        film_description_entry = ttk.Entry(content, textvariable=filmDescription)
        film_description_entry.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        film_actors_label = ttk.Label(content, text="Film Actors:")
        film_actors_label.grid(row=3, column=0, pady=10, padx=10)
        film_actors_entry = ttk.Entry(content, textvariable=filmActors)
        film_actors_entry.grid(row=3, column=1, columnspan=2, pady=10, padx=10)
        film_genre_label = ttk.Label(content, text="Film Genre:")
        film_genre_label.grid(row=4, column=0, pady=10, padx=10)
        film_genre_entry = ttk.Entry(content, textvariable=filmGenre)
        film_genre_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        film_age_label = ttk.Label(content, text="Film Age:")
        film_age_label.grid(row=5, column=0, pady=10, padx=10)
        film_age_entry = ttk.Entry(content, textvariable=filmAge)
        film_age_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        film_rating_label = ttk.Label(content, text="Film Rating:")
        film_rating_label.grid(row=6, column=0, pady=10, padx=10)
        film_age_entry = ttk.Entry(content, textvariable=filmRating)
        film_age_entry.grid(row=6, column=1, columnspan=2, pady=10, padx=10)

        add_film_button = ttk.Button(content, text="Add Film")
        add_film_button.grid(row=7, column=0, pady=20, padx=10)
        edit_film_button = ttk.Button(content, text="Edit Film")
        edit_film_button.grid(row=7, column=1, pady=20, padx=10)
        remove_film_button = ttk.Button(content, text="Remove Film")
        remove_film_button.grid(row=7, column=2, pady=20, padx=10)
        horizontal_line_label = ttk.Label(content, text="-------------------------------------------------------------------------------------------")
        horizontal_line_label.grid(row=8, column=0, columnspan=3)
        search_label = ttk.Label(content, text="Search Film Details by Title:")
        search_label.grid(row=9, column=0, pady=10, padx=10)
        search_title_entry = ttk.Entry(content, textvariable=searchTitle)
        search_title_entry.grid(row=9, column=2, columnspan=2, pady=20, padx=10)
        search_title_button = ttk.Button(content, text="Search")
        search_title_button.grid(row=10, column=0, columnspan=3, pady=10, padx=10)

class ViewCinemasFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        self.__createHeaderWithWidgets()
        self.__createContentWithWidgets()
        
    
    def __createHeaderWithWidgets(self):
        header = ttk.Frame(self)
        header.grid(row=0)
        current_page_label = ttk.Label(header, text="View Cinemas", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        menu_button = ttk.Button(header, command= lambda : app.showFrame("HomeFrame"), text="Menu")
        menu_button.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)

    def __createContentWithWidgets(self):
        content = ttk.Frame(self)
        content.grid(row=1)
        email = tk.StringVar()
        cinemaCity = tk.StringVar()
        cinemaName = tk.StringVar()
        addCityName = tk.StringVar()
        morningPrice = tk.StringVar()
        afternoonPrice = tk.StringVar()
        eveningPrice = tk.StringVar()
        cinema_city_label = ttk.Label(content, text="Cinema City:")
        cinema_city_label.grid(row=0, column=0, pady=20, padx=10)
        cinema_city_entry = ttk.Entry(content, textvariable=cinemaCity)
        cinema_city_entry.grid(row=0, column=1, columnspan=2, pady=20, padx=10)
        cinema_name_label = ttk.Label(content, text="Cinema Name:")
        cinema_name_label.grid(row=1, column=0, pady=20, padx=10)
        cinema_name_entry = ttk.Entry(content, textvariable=cinemaName)
        cinema_name_entry.grid(row=1, column=1, columnspan=2, pady=20, padx=10)
        add_cinema_button = ttk.Button(content, text="Add Cinema")
        add_cinema_button.grid(row=2, column=0, columnspan=3, pady=20, padx=10)
        horizontal_line_label = ttk.Label(content, text="-------------------------------------------------------------------------------------------")
        horizontal_line_label.grid(row=3, column=0, columnspan=3)
        city_label = ttk.Label(content, text="City Name:")
        city_label.grid(row=4, column=0, pady=20, padx=10)
        city_entry = ttk.Entry(content, textvariable=addCityName)
        city_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        city_morning_price_label = ttk.Label(content, text="Morning Price:")
        city_morning_price_label.grid(row=5, column=0, pady=10, padx=10)
        city_morning_price_entry = ttk.Entry(content, textvariable=morningPrice)
        city_morning_price_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        city_afternoon_price_label = ttk.Label(content, text="Afternoon Price:")
        city_afternoon_price_label.grid(row=6, column=0, pady=10, padx=10)
        city_afternoon_price_entry = ttk.Entry(content, textvariable=afternoonPrice)
        city_afternoon_price_entry.grid(row=6, column=1, columnspan=2, pady=10, padx=10)
        city_evening_price_label = ttk.Label(content, text="Evening Price:")
        city_evening_price_label.grid(row=7, column=0, pady=10, padx=10)
        city_evening_price_entry = ttk.Entry(content, textvariable=eveningPrice)
        city_evening_price_entry.grid(row=7, column=1, columnspan=2, pady=10, padx=10)
        add_city_button = ttk.Button(content, text="Add City")
        add_city_button.grid(row=8, column=0, columnspan=3, pady=10, padx=10)



if __name__ == "__main__":
    app = App()
    app.mainloop()