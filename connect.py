
import libhitwa
import tkinter
import sys

from tkinter import messagebox


username = ''
password = ''

def main(argv):
    if len(argv) <= 1 or argv[1] != 'logout':
        result, message = libhitwa.do_login(username, password)
    else:
        result, message = libhitwa.do_logout()
    tk = tkinter.Tk()
    tk.withdraw()
    if result:
        messagebox.showinfo('HITWA: Connected', message)
    else:
        messagebox.showerror('HITWA: Failed to connect', message)
    return

if __name__ == '__main__':
    main(sys.argv)
