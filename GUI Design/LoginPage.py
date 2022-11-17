from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Login")
        self.resizable(0,0)
        self.configure(bg="#181818")
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica bold', 15), background="#181818", foreground="#b3b3b3")
        self.style.configure('TButton', font=("Helvetica bold", 10),foreground="#121212", height=40, width=25)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
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
        login_button = ttk.Button(self, text="Login", command=lambda : self.login(username, password, username_entry, password_entry))
        login_button.grid(columnspan=2, row=3, padx=10, pady=10)

    def login(self, username, password, username_entry, password_entry):
        username_entry.configure(foreground="red")
        password_entry.configure(foreground="red")
        failed_login_label = ttk.Label(self, text="Forgotten your password? Please call over an admin to mediate this issue. If you are an admin who has forgotten their password please contact a manager immediately.", font=("Helvetica bold itallic", 8)).grid(columnspan=2, row=4, padx=10, pady=10)





if __name__ == "__main__":
    app = App()    
    app.mainloop()