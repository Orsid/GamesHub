"""
This file handles the login and signup UI and functionality
"""
from client import client_logic
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

login_window = None
signupWin = None


# Signup
def signup():
    # Make a regular expression
    # for validating an Email address
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    global signupWin
    first_name = signupWin.first_name.get()
    last_name = signupWin.last_name.get()
    user_name = signupWin.user_name.get()
    email = signupWin.email.get()
    password = signupWin.password.get()
    very_pass = signupWin.very_pass.get()

    if first_name == "" or last_name == "" or user_name == "" or email == "" or password == "" or very_pass == "":
        messagebox.showerror("Error", "All Fields Are Required", parent=signupWin)
    elif password != very_pass:
        messagebox.showerror("Error", "Password & Confirm Password Should Be Same", parent=signupWin)
    elif re.search(regex, email) is None:
        messagebox.showerror("Error", "Please type a valid email address", parent=signupWin)
    else:
        try:
            user_data = first_name + "##" + last_name + "##" + user_name + "##" + email + "##" + password
            client_logic.bl_signup(user_data)

        except Exception as es:
            messagebox.showerror("Error", f"Error Dui to : {str(es)}", parent=signupWin)


# start signup window
def open_signup_ui():
    global signupWin
    signupWin = Toplevel()
    signupWin.title("GameHub - Register")
    signupWin.maxsize(width=430, height=360)
    signupWin.minsize(width=430, height=360)

    bg_color = "DeepSkyBlue2"
    signupWin.configure(background=bg_color)

    # heading label
    heading = Label(signupWin, text="Register", font='Verdana 20 bold', bg=bg_color)
    heading.place(x=40, y=25)

    # form data label
    first_name = Label(signupWin, text="First Name :", font='Verdana 10 bold', bg=bg_color)
    first_name.place(x=40, y=70)

    last_name = Label(signupWin, text="Last Name :", font='Verdana 10 bold', bg=bg_color)
    last_name.place(x=40, y=110)

    user_name = Label(signupWin, text="User Name :", font='Verdana 10 bold', bg=bg_color)
    user_name.place(x=40, y=150)

    user_name = Label(signupWin, text="Email :", font='Verdana 10 bold', bg=bg_color)
    user_name.place(x=40, y=190)

    password = Label(signupWin, text="Password :", font='Verdana 10 bold', bg=bg_color)
    password.place(x=40, y=230)

    very_pass = Label(signupWin, text="Verify Password:", font='Verdana 10 bold', bg=bg_color)
    very_pass.place(x=40, y=270)

    # Entry Box ------------------------------------------------------------------
    first_name = StringVar()
    last_name = StringVar()
    user_name = StringVar()
    email = StringVar()
    password = StringVar()
    very_pass = StringVar()

    signupWin.first_name = Entry(signupWin, width=30, textvariable=first_name)
    signupWin.first_name.focus()
    signupWin.first_name.place(x=190, y=70)

    signupWin.last_name = Entry(signupWin, width=30, textvariable=last_name)
    signupWin.last_name.place(x=190, y=110)

    signupWin.user_name = Entry(signupWin, width=30, textvariable=user_name)
    signupWin.user_name.place(x=190, y=150)

    signupWin.email = Entry(signupWin, width=30, textvariable=email)
    signupWin.email.place(x=190, y=190)

    signupWin.password = Entry(signupWin, width=30, show="*", textvariable=password)
    signupWin.password.place(x=190, y=230)

    signupWin.very_pass = Entry(signupWin, width=30, show="*", textvariable=very_pass)
    signupWin.very_pass.place(x=190, y=270)

    # button register and login
    btn_signup = Button(signupWin, text="Register", font='Verdana 10 bold', command=signup)
    btn_signup.place(x=240, y=310)

    btn_login = Button(signupWin, text="Close", font='Verdana 10 bold', command=signupWin.destroy)
    btn_login.place(x=320, y=310)

    #    signupWin.bind('<Return>', signup)

    signupWin.mainloop()


def close_signup_ui():
    global signupWin
    messagebox.showinfo("Success", "Signup successfully!", parent=signupWin)
    if signupWin is not None:
        signupWin.destroy()


def show_signup_msg_info(msg):
    global signupWin
    messagebox.showinfo("Error", msg, parent=signupWin)


# login window

def login():
    global login_window

    username = login_window.userentry.get()
    password = login_window.passentry.get()
    if username == "" or password == "":
        messagebox.showerror("Error", "Enter User Name And Password")
    else:
        user_data = username + "##" + password
        client_logic.bl_login(user_data)
        return "login", username, password


def open_login_ui():
    global login_window

    login_window = Tk()

    login_window.title("GameHub - Login")

    bg_color = "DeepSkyBlue2"
    login_window.configure(background=bg_color)

    # window size
    login_window.maxsize(width=430, height=380)
    login_window.minsize(width=430, height=380)

    photo = ImageTk.PhotoImage(Image.open("../res/c4_cover_small.jpeg"))
    Label(login_window, image=photo).grid(rowspan=3, columnspan=5, row=0, column=0)

    username = Label(login_window, text="User Name :", font='Verdana 10 bold', bg=bg_color)
    username.place(x=60, y=260)

    userpass = Label(login_window, text="Password :", font='Verdana 10 bold', bg=bg_color)
    userpass.place(x=60, y=300)

    # Entry Boxes
    user_name = StringVar()
    password = StringVar()

    login_window.userentry = Entry(login_window, width=35, textvariable=user_name)
    login_window.userentry.focus()
    login_window.userentry.place(x=170, y=260)

    login_window.passentry = Entry(login_window, width=35, show="*", textvariable=password)
    login_window.passentry.place(x=170, y=300)

    # button login
    btn_login = Button(login_window, text="Login", font='Verdana 10 bold', command=login)
    btn_login.place(x=260, y=340)

    # signup button
    sign_up_btn = Button(login_window, text="Signup", font='Verdana 10 bold', command=open_signup_ui)
    sign_up_btn.place(x=320, y=340)

    login_window.mainloop()


def close_login_ui():
    global login_window
    if login_window is not None:
        login_window.withdraw()


def show_login_msg_info(msg):
    global login_window
    messagebox.showinfo("Error", msg, parent=login_window)


# a message box for messages
def show_message_box(title, message):
    messagebox.showerror(title, message)


# a yes/no message box for messages
def show_yes_no_message_box(title, message):
    return messagebox.askquestion(title, message)