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
        self.style.configure('TLabel', font=('Helvetica bold', 15), background="#181818", foreground="#b3b3b3")
        self.style.configure('TButton', font=("Helvetica bold", 10), foreground="#121212", height=40, width=25)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)
        header = ttk.Frame(self)
        content = ttk.Frame(self)
        # Header widgets
        header.grid(row=0)
        content.grid(row=1)
        current_page_label = ttk.Label(header, text="Current Page Title", font=('Helvetica bold', 20))
        current_page_label.grid(row=0, column= 0, padx=50, pady=20)
        staff_name_label = ttk.Label(header, text="Staff Name:")
        staff_name_label.grid(row=0, column=1, padx=0, pady=20)
        staff_cinema_label = ttk.Label(header, text=" Staff Name [Staff Cinema]")
        staff_cinema_label.grid(row=0, column=2, padx=10, pady=20)
        horizon_cinema_label = ttk.Label(header, text="Horizon Cinemas")
        horizon_cinema_label.grid(row=0, column=3, padx=50, pady=20, sticky=tk.E)
        # Content widgets