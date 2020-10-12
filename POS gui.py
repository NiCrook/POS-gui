import tkinter as tk
from tkinter import IntVar, StringVar
import mysql.connector as mysql

### SQL Database Handling ###

# establish sql connection
sql_db = mysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydatabase"
)

# assign sql cursor to variable for convenience
cursor = sql_db.cursor(buffered=True)

# create SQL Table named 'users'
# if it exists, print message handling error
try:
    cursor.execute("CREATE TABLE users (username VARCHAR(225), password VARCHAR(225))")
    print("User table does not exist.\nCreating user table now...\n")
except Exception as e:
    print("Exception occurred:{}".format(e))

# assign variables for creating and checking admin profile in users table
insert_user = "INSERT INTO users (username, password) VALUES (%s, %s)"
admin = ("username", "password")
admin_check_sql = "SELECT * FROM users WHERE username='username' AND password='password'"

# checks to see if Table 'users' has any rows
# if zero rows, then admin profile can't exist
# creates admin profile if zero rows
try:
    cursor.execute(admin_check_sql)
    admin_result = cursor.fetchall()
    row_count = cursor.rowcount
    print("number of counted rows: {}".format(row_count))
    if row_count == 0:
        print("Admin profile does not exist.\nCreating admin profile now...\n")
        cursor.execute(insert_user, admin)
        sql_db.commit()  # commits changes to the table
        cursor.execute(admin_check_sql)
        second_result = cursor.fetchall()
        second_count = cursor.rowcount
        if second_count == 0:
            print("You're still doing it wrong.")
        else:
            for row in second_result:
                print(row)
            print("Yay! You did it!")
    else:
        print("Admin profile exists.\n")
except Exception as e:
    print("Something went wrong:{}".format(e))

### FRAMES ###

# create the underlying container frame which holds StartFrames, LoginFrame, and MenuFrame
class ContainerFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # assigns container variable as a frame
        # give container frame dimensions
        self.container = tk.Frame(self)
        self.title("Point-of-Sales Demo v2.01")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frame_list = [StartFrame, LoginFrame, MenuFrame]
        self.frames = {}

        # loop that assigns each item in frame_list to a frame
        # place each frame into container frame, on top of each other
        for F in self.frame_list:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    # method that removes grid placement for frames not shown
    # reduces size of frames not shown, giving shown frame proper size
    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
            frame = self.frames[page_name]
            frame.grid()

    def create_frame(self, frame_name):
        self.frames[frame_name] = frame_name(parent=self.container, controller=self)
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")


class StartFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # WIDGETS
        app_name_label = tk.Label(self, text="Cash Register System v2.01")
        start_button = tk.Button(self, text="Start", command=self.start_button_push)

        # LAYOUT
        app_name_label.grid(row=1, column=0, columnspan=3)
        start_button.grid(row=2, column=1)

    def start_button_push(self):
        self.controller.show_frame("LoginFrame")


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # WIDGETS
        self.login_labels = {
            "login label": tk.Label(self, text="Login"),
            "username label": tk.Label(self, text="Username:"),
            "password label": tk.Label(self, text="Password:"),
            'wrong entry label': tk.Label(self, text='You have entered a wrong username/password. Try again')
        }

        self.login_entries = {
            'username entry': tk.Entry(self),
            'password entry': tk.Entry(self, show='*')
        }

        login_button = tk.Button(self, text="Login", command=self.login_push)

        # LAYOUT
        self.login_labels["login label"].grid(row=1, column=0)
        self.login_labels["username label"].grid(row=2, column=0)
        self.login_entries["username entry"].grid(row=2, column=1)
        self.login_labels["password label"].grid(row=3, column=0)
        self.login_entries["password entry"].grid(row=3, column=1)
        login_button.grid(row=4, column=1)

    # method which grabs each entry field contents
    # checks contents against items in user_dict
    # if any match, shows next frame while destroying loginframe
    # if none match, shows message giving unmatch error, prompts the user to try again
    def login_push(self):
        empty_list = []
        user_login = self.login_entries["username entry"].get()
        pass_login = self.login_entries["password entry"].get()
        login_info = (user_login, pass_login)
        print(login_info)
        user_check_sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(user_check_sql, login_info)
        if cursor.fetchall() == empty_list:
            self.login_labels["wrong entry label"].grid(row=5, column=0, columnspan=3)
        else:
            self.controller.show_frame("MenuFrame")
            self.login_entries["username entry"].delete(0, tk.END)
            self.login_entries["password entry"].delete(0, tk.END)
            if self.login_labels["wrong entry label"]:
                self.login_labels["wrong entry label"].grid_remove()
        cursor.execute(user_check_sql, login_info)


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        hello_label = tk.Label(self, text='Hello! Select an item below.')

        self.menu_buttons = {
            "admin button": tk.Button(self, text="Admin", command=self.admin_push),
            "POS button": tk.Button(self, text="POS", command=self.POS_push),
            "logout button": tk.Button(self, text="Logout", command=self.logout_push)
        }

        hello_label.grid(row=1, column=0, columnspan=3)
        self.menu_buttons["admin button"].grid(row=2, column=0)
        self.menu_buttons["POS button"].grid(row=2, column=1)
        self.menu_buttons["logout button"].grid(row=2, column=2)

    def admin_push(self):
        self.controller.create_frame(AdminFrame)
        self.controller.show_frame(AdminFrame)

    def POS_push(self):
        self.controller.create_frame(POSFrame)
        self.controller.show_frame(POSFrame)

    def logout_push(self):
        self.controller.show_frame("LoginFrame")


class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        admin_label = tk.Label(self, text="Admin Screen")

        self.admin_buttons = {
            "user list": tk.Button(self, text="User List", command=self.user_list_push),
            "add user": tk.Button(self, text="Add User"),
            "change password": tk.Button(self, text="Change Password"),
            "return": tk.Button(self, text="Return", command=self.return_push)
        }

        admin_label.grid(row=1, column=1, columnspan=2)
        self.admin_buttons["user list"].grid(row=2, column=0, columnspan=1)
        self.admin_buttons["add user"].grid(row=2, column=1, columnspan=1)
        self.admin_buttons["change password"].grid(row=2, column=2, columnspan=1)
        self.admin_buttons["return"].grid(row=2, column=3, columnspan=1)

    def user_list_push(self):
        self.controller.create_frame(UserListFrame)
        self.controller.show_frame(UserListFrame)

    def add_user_push(self):
        pass

    def change_password_push(self):
        pass

    def return_push(self):
        self.controller.show_frame("MenuFrame")
        # self.destroy()


class POSFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        pos_label = tk.Label(self, text="POS Menu")

        pos_buttons = {
            "start of day": tk.Button(self, text="Start of Day"),
            "new sale": tk.Button(self, text="New Sale"),
            "daily sales": tk.Button(self, text="Daily Sales"),
            "cash drop": tk.Button(self, text="Add/Drop Cash"),
            "end of day": tk.Button(self, text="End of Day"),
            "return": tk.Button(self, text="Return")
        }

        pos_buttons["start of day"].grid(row=1, column=0)
        pos_buttons["new sale"].grid(row=1, column=1)
        pos_buttons["daily sales"].grid(row=1, column=2)
        pos_buttons["cash drop"].grid(row=2, column=0)
        pos_buttons["end of day"].grid(row=2, column=1)
        pos_buttons["return"].grid(row=2, column=2)


class UserListFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        user_list_sql = "SELECT * FROM users"
        cursor.execute(user_list_sql)
        user_list_dict = {}
        for user in cursor:
            user_list_dict[user[0]] = user[1]

        user_list_label = tk.Label(self, text="User List")

        self.user_list_box = tk.Listbox(self)
        for user in user_list_dict.keys():
            self.user_list_box.insert(tk.END, user)

        user_list_buttons = {
            "remove user": tk.Button(self, text="Remove", command=self.remove_user),
            "return": tk.Button(self, text="Return", command=self.frame_return)
        }

        user_list_label.grid(row=1, column=0)
        self.user_list_box.grid(row=2, column=0, columnspan=2)
        user_list_buttons["remove user"].grid(row=3, column=0)
        user_list_buttons["return"].grid(row=3, column=1)

    def remove_user(self):
        user_delete_sql = "DELETE FROM users WHERE username=%s"
        removed_user = str(self.user_list_box.get(tk.ANCHOR))

        cursor.execute(user_delete_sql, (removed_user,))
        sql_db.commit()
        self.user_list_box.delete(tk.ANCHOR)

    def frame_return(self):
        self.controller.show_frame(AdminFrame)
        # self.destroy()


#     CURRENCY_LIST = ['$100', '$50', '$20', '$10', '$5', '$1', '$0.25', '$0.10', '$0.05', '$0.01']

### MAIN OPERATION ###

def main():
    # user_lst_directory()
    # user_admin_check()
    root = ContainerFrame()
    root.mainloop()


if __name__ == '__main__':
    main()
