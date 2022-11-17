from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Home Page")
        self.resizable(0,0)
        self.configure(bg="#181818")
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica bold', 15), background="#181818", foreground="#b3b3b3")
        self.style.configure('TButton', font=("Helvetica bold", 10), foreground="#121212", height=40, width=25)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        horizon_cinema_label = ttk.Label(self, text="Horizon", font=('Helvetica bold', 15))
        horizon_cinema_label.grid(column=0,row=1)
        current_user_label = ttk.Label(self, text="Cinemas", font=('Helvetica bold', 15))
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
        quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(column=4, row=3, padx=10, pady=20, sticky=E)




if __name__ == "__main__":
    app = App()    
    app.mainloop()