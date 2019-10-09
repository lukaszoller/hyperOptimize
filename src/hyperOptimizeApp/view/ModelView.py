import tkinter as tk


class ModelView(tk.Frame):

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="green")
        self.place(relx=0, rely=0, height=height, width=width)