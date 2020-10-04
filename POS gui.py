import tkinter as tk
from tkinter import IntVar, StringVar
import os


def user_lst_directory():
    if not os.path.exists("user_list.txt"):
        print("file does not exist.\nCreating new file...")
        file = open("user_list.txt", "w")
        file.write("username:password,")
        file.close()
    else:
        print("File exists.")


class ContainerFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        self.title("Point-of-Sales Demo v2.01")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame_list = [StartFrame, LoginFrame, MenuFrame]
        self.frames = {}

        for F in frame_list:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
            frame = self.frames[page_name]
            frame.grid()

    # def create_admin_frame(self):
    #     self.frames["AdminFrame"] = AdminFrame(parent=self.container, controller=self)
    #     self.frames["AdminFrame"].grid(row=0, column=0, sticky="nsew")


class StartFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        app_name_label = tk.Label(self, text="Cash Register System v2.01")
        start_button = tk.Button(self, text="Start", command=self.start_button_push)

        app_name_label.grid(row=1, column=0, columnspan=3)
        start_button.grid(row=2, column=1)

    def start_button_push(self):
        self.controller.show_frame("LoginFrame")


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        user_list = open("user_list.txt", "r")
        users = user_list.readlines()
        self.user_dict = {}
        for line in users:
            delimer = str(":")
            delimer_index = line.find(delimer)
            username = line[0:delimer_index]
            password = line[(delimer_index + 1):-1]
            self.user_dict[username] = password

        self.login_labels = {
            "login label": tk.Label(self, text="Login"),
            "username label": tk.Label(self, text="Username:"),
            "password label": tk.Label(self, text="Password:"),
            'wrong_user/pass_label': tk.Label(self, text='You have entered a wrong username/password. Try again')
        }

        self.login_entries = {
            'username entry': tk.Entry(self),
            'password entry': tk.Entry(self, show='*')
        }

        login_button = tk.Button(self, text="Login", command=self.login_push)

        self.login_labels["login label"].grid(row=1, column=0)
        self.login_labels["username label"].grid(row=2, column=0)
        self.login_entries["username entry"].grid(row=2, column=1)
        self.login_labels["password label"].grid(row=3, column=0)
        self.login_entries["password entry"].grid(row=3, column=1)
        login_button.grid(row=4, column=1)

    def login_push(self):
        user_login = self.login_entries["username entry"].get()
        pass_login = self.login_entries["password entry"].get()
        try:
            for username, password in self.user_dict.items():
                if user_login == username:
                    if pass_login == password:
                        self.controller.show_frame("MenuFrame")
        except:
            print("You have entered a wrong username/password! Try again!\n")


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        hello_label = tk.Label(self, text='Hello! Select an item below.')

        self.menu_buttons = {
            "admin button": tk.Button(self, text="Admin"),
            "POS button": tk.Button(self, text="POS"),
            "logout button": tk.Button(self, text="Logout")
        }

        hello_label.grid(row=1, column=0, columnspan=3)
        self.menu_buttons["admin button"].grid(row=2, column=0)
        self.menu_buttons["POS button"].grid(row=2, column=1)
        self.menu_buttons["logout button"].grid(row=2, column=2)

    # def admin_push(self):
    #     self.controller.create_admin_frame()
    #     # ContainerFrame.create_admin_frame(ContainerFrame.parent)
    #     self.controller.show_frame("AdminFrame")

    def POS_push(self):
        pass

    def logout_push(self):
        pass


class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        admin_label = tk.Label(self, text="Admin Screen")

        self.admin_buttons = {
            "user list": tk.Button(self, text="User List"),
            "add user": tk.Button(self, text="Add User"),
            "change password": tk.Button(self, text="Change Password"),
            "return": tk.Button(self, text="Return")
        }

        admin_label.grid(row=1, column=1, columnspan=2)
        self.admin_buttons["user list"].grid(row=2, column=0, columnspan=1)
        self.admin_buttons["add user"].grid(row=2, column=1, columnspan=1)
        self.admin_buttons["change password"].grid(row=2, column=2, columnspan=1)
        self.admin_buttons["return"].grid(row=2, column=3, columnspan=1)

    def user_list_push(self):
        pass

    def add_user_push(self):
        pass

    def change_password_push(self):
        pass

    def return_push(self):
        pass


def main():
    user_lst_directory()
    root = ContainerFrame()
    root.mainloop()


if __name__ == '__main__':
    main()
