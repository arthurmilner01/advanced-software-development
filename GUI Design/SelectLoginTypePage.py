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
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        title_label = ttk.Label(self, text="Please Select User Type:", font=('Helvetica bold', 15))
        title_label.grid(column=1,row=1)
        booking_staff_login_button = ttk.Button(self, text="Booking Staff")
        booking_staff_login_button.grid(column=1, row=2, padx=10, pady=20)
        admin_login_button = ttk.Button(self, text="Admin")
        admin_login_button.grid(column=1, row=3, padx=10, pady=20)
        manager_login_button = ttk.Button(self, text="Manager")
        manager_login_button.grid(column=1, row=4, padx=10, pady=20)
        quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(column=1, row=5, padx=10, pady=80, sticky=S)




if __name__ == "__main__":
    app = App()    
    app.mainloop()