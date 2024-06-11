"""
util.py

Contains a number of "utility" functions to lighten the code in general
"""

import tkinter as tk
from tkinter import messagebox


def show_info_message(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    messagebox.showinfo(title, message)
    root.destroy()  # This closes the Tkinter instance


def show_warning_message(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    messagebox.showwarning(title, message)
    root.destroy()  # This closes the Tkinter instance


def show_error_message(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    messagebox.showerror(title, message)
    root.destroy()  # This closes the Tkinter instance


def ask_question(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    response = messagebox.askquestion(title, message)
    root.destroy()  # This closes the Tkinter instance
    return response


def ask_yes_no(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    response = messagebox.askyesno(title, message)
    root.destroy()  # This closes the Tkinter instance
    return response


def ask_ok_cancel(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    response = messagebox.askokcancel(title, message)
    root.destroy()  # This closes the Tkinter instance
    return response


def ask_retry_cancel(title, message):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    response = messagebox.askretrycancel(title, message)
    root.destroy()  # This closes the Tkinter instance
    return response


def escape_json_for_javascript(json_string: str):
    """
    Prepares a JSON string to be sent through pywebview's api without errors
    """
    monitor_data_json = json_string.replace('"', '\\"')
    return monitor_data_json
