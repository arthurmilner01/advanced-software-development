from tkinter import *
from tkinter import ttk


class App(Tk):
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
        except TclError:
            print("Windows Only")


class BookingStaffLoginFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__createWidgets()

    def __createWidgets(self):
        username = StringVar()
        password = StringVar()
        login_title_label = ttk.Label(self, text="Login", font=('Helvetica bold', 26), foreground="white")
        login_title_label.grid(columnspan=3, row=0, padx=5, pady=5)
        username_label = ttk.Label(self, text="Username:")
        username_label.grid(column=0, row=1, padx=5, pady=5, sticky=E)
        username_entry = ttk.Entry(self, textvariable=username)
        username_entry.grid(column=1, row=1, padx=10, pady=10, sticky=W)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=0, row=2, padx=5, pady=5, sticky=E)
        password_entry = ttk.Entry(self, textvariable=password, show="*")
        password_entry.grid(column=1, row=2, padx=10, pady=10, sticky=W)
        login_button = ttk.Button(self, text="Login", command=lambda : self.validateLogin(username, password, username_entry, password_entry))
        login_button.grid(columnspan=2, row=3, padx=10, pady=10)
    
    def validateLogin(self, username, password, username_entry, password_entry):
        username_entry.configure(foreground="red")
        password_entry.configure(foreground="red")
        failed_login_label = ttk.Label(self, text="Forgotten your password? Please call over an admin to mediate this issue.", font=("Helvetica bold itallic", 8)).grid(columnspan=2, row=4, padx=10, pady=10)
        homeFrame.place(height=768, width=1366)

class HomeFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.__createWidgets()

    def __createWidgets(self):
        horizon_cinema_label = ttk.Label(self, text="Horizon Cinemas", font=('Helvetica bold', 15))
        horizon_cinema_label.grid(column=0,row=1)
        current_user_label = ttk.Label(self, text="Staff Name [Staff Type]", font=('Helvetica bold', 15))
        current_user_label.grid(column=0,row=2)
        listings_button = ttk.Button(self, text="View Film Listings")
        listings_button.grid(column=1, row=1, padx=10, pady=20, sticky=W)
        create_booking_button = ttk.Button(self, text="Create Booking")
        create_booking_button.grid(column=2, row=1, padx=10, pady=20)
        cancel_booking_button = ttk.Button(self, text="Cancel Booking")
        cancel_booking_button.grid(column=3, row=1, padx=10, pady=20)
        generate_report_button = ttk.Button(self, text="Generate Report")
        generate_report_button.grid(column=4, row=1, padx=10, pady=20, sticky=E)
        view_booking_staff_button = ttk.Button(self, text="View Booking Staff")
        view_booking_staff_button.grid(column=1, row=2, padx=10, pady=20, sticky=W)
        view_admin_button = ttk.Button(self, text="View Admin Staff")
        view_admin_button.grid(column=2, row=2, padx=10, pady=20)
        view_cinema_button = ttk.Button(self, text="View Cinemas")
        view_cinema_button.grid(column=3, row=2, padx=10, pady=20)
        view_film_button = ttk.Button(self, text="View Film")
        view_film_button.grid(column=4, row=2, padx=10, pady=20, sticky=E)

if __name__ == "__main__":
    app = App()
    bookingStaffLoginFrame = BookingStaffLoginFrame(app)
    homeFrame = HomeFrame(app)
    bookingStaffLoginFrame.place(height=768, width=1366)
    app.mainloop()