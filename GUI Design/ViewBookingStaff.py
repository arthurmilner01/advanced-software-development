import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Home Page")
        self.resizable(0,0)
        self.configure(bg="#181818")
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica bold', 15), background="#F0F0F0", foreground="black")
        self.style.configure('TButton', font=("Helvetica bold", 10), foreground="#121212", height=40, width=25)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self)
        content = ttk.Frame(self)
        # Header widgets
        header.grid(row=0)
        content.grid(row=1)

        current_page_label = ttk.Label(header, text="View Booking Staff")
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        horizon_cinema_label = ttk.Label(header, text="Horizon Cinemas")
        horizon_cinema_label.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)
        # Content widgets
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

        




if __name__ == "__main__":
    app = App()    
    app.mainloop()