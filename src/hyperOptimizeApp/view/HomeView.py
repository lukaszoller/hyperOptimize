import tkinter as tk


class HomeView(tk.Frame):

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="yellow")
        self.place(relx=0, rely=0, height=height, width=width)