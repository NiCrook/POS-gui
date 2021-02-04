import tkinter as tk
from tkinter import IntVar, StringVar
import mysql.connector as mysql
from mysql.connector import errorcode

### SQL Database Handling ###

sql_db = mysql.connect(
    host="localhost",
    user="root",
    password="password"
)

#   ESTABLISH CURSOR
cursor = sql_db.cursor(buffered=True)

TABLES_USERS = {}
TABLES_SALES = {}

#   DEFINE EACH DESIGNATED TABLE
TABLES_USERS['user profiles'] = (
    "CREATE TABLE `user profiles` ("
    "   `username` varchar(16),"
    "   `password` varchar(16)"
    ")  ENGINE=InnoDB")

TABLES_SALES['sales log'] = (
    "CREATE TABLE `sales log` ("
    "   `sale ID` int(11) NOT NULL AUTO_INCREMENT,"
    "   `sale date` date NOT NULL,"
    "   `item log` varchar(225),"
    "   `item number` int(3) NOT NULL,"
    "   `sale value` int(8) NOT NULL,"
    "   PRIMARY KEY (`sale ID`), KEY `sale_id` (`sale ID`)"
    ")  ENGINE=InnoDB")

DB_LIST = ['users', 'sales']
TABLE_LIST = [TABLES_USERS, TABLES_SALES]

DB_TABLE_DICT = {}

#   PAIR EACH DATABASE WITH ITS DESIGNATED LIST OF TABLES
for k, db in enumerate(DB_LIST):
    DB_TABLE_DICT[db] = TABLE_LIST[int(k)]


def create_database(cursor, db_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.Error as err:
        print("Failed to create database: {}.\n".format(err))
        exit(1)


#   CREATE DATABASES
for db in DB_LIST:
    try:
        cursor.execute("USE {}".format(db))
        print("DB: {} exists.".format(db))
    except mysql.Error as err:
        print("Database {} does not exist.".format(db))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, db)
            print("Database {} created.".format(db))
        else:
            print(err)
            exit(1)

#   CREATE TABLES FOR EACH DATABASE
for db, table in DB_TABLE_DICT.items():
    cursor.execute("USE {}".format(db))
    for table_name in table:
        table_data = table[table_name]
        try:
            print("Creating table: {}.".format(table_name), end='')
            cursor.execute(table_data)
        except mysql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("\nTable {} already exists.".format(table_name))
            else:
                print(err.msg)
        else:
            print("\nOkay!")

#   CHECK FOR ADMIN PROFILE, CREATE IF DOESN'T EXIST
INSERT_USER = "INSERT INTO `user profiles` (username, password) VALUES (%s, %s)"
ADMIN = ("username", "password")
ADMIN_CHECK_SQL = "SELECT * FROM `user profiles` WHERE username='username' AND password='password'"

try:
    cursor.execute("USE users")
    print("Using database: 'users'")

    cursor.execute(ADMIN_CHECK_SQL)
    admin_result = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        print("Admin profile does not exist.\nCreating admin profile now...\n")
        cursor.execute(INSERT_USER, ADMIN)
        sql_db.commit()
    else:
        print("Admin profile exists.\n")
except Exception as e:
    print("Something went wrong: {}".format(e))


### FRAMES ###

# CONTAINER FRAME
class ContainerFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.title("Point-of-Sales Demo v2.01")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frame_list = [StartFrame, LoginFrame, MenuFrame]
        self.frames = {}

        for F in self.frame_list:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
            frame = self.frames[page_name]
            frame.grid()

    def create_frame(self, frame_name):
        self.frames[frame_name] = frame_name(parent=self.container, controller=self)
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")


# START FRAME
class StartFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
        app_name_label = tk.Label(self, text="Cash Register System v2.01")
        start_button = tk.Button(self, text="Start", command=self.start_button_push)

        #   LAYOUT
        app_name_label.grid(row=1, column=0, columnspan=3)
        start_button.grid(row=2, column=1)

    #   METHODS
    def start_button_push(self):
        self.controller.show_frame("LoginFrame")


# LOGIN FRAME
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
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

        #   LAYOUT
        self.login_labels["login label"].grid(row=1, column=0)
        self.login_labels["username label"].grid(row=2, column=0)
        self.login_entries["username entry"].grid(row=2, column=1)
        self.login_labels["password label"].grid(row=3, column=0)
        self.login_entries["password entry"].grid(row=3, column=1)

        login_button.grid(row=4, column=1)

    #   METHODS
    def login_push(self):
        empty_list = []
        user_login = self.login_entries["username entry"].get()
        pass_login = self.login_entries["password entry"].get()
        login_info = (user_login, pass_login)
        user_check_sql = "SELECT * FROM `user profiles` WHERE username=%s AND password=%s"

        cursor.execute("USE `users`")
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


# MENU FRAME
class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
        hello_label = tk.Label(self, text='Hello! Select an item below.')

        self.menu_buttons = {
            "admin button": tk.Button(self, text="Admin", command=self.admin_push),
            "POS button": tk.Button(self, text="POS", command=self.POS_push),
            "logout button": tk.Button(self, text="Logout", command=self.logout_push)
        }

        #   LAYOUT
        hello_label.grid(row=1, column=0, columnspan=3)

        self.menu_buttons["admin button"].grid(row=2, column=0)
        self.menu_buttons["POS button"].grid(row=2, column=1)
        self.menu_buttons["logout button"].grid(row=2, column=2)

    #   METHODS
    def admin_push(self):
        self.controller.create_frame(AdminFrame)
        self.controller.show_frame(AdminFrame)

    def POS_push(self):
        self.controller.create_frame(POSFrame)
        self.controller.show_frame(POSFrame)

    def logout_push(self):
        self.controller.show_frame("LoginFrame")


# ADMIN FRAME
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
        admin_label = tk.Label(self, text="Admin Screen")

        self.admin_buttons = {
            "user list": tk.Button(self, text="User List", command=self.user_list_push),
            "add user": tk.Button(self, text="Add User", command=self.add_user_push),
            "change password": tk.Button(self, text="Change Password", command=self.change_password_push),
            "return": tk.Button(self, text="Return", command=self.return_push)
        }

        #   LAYOUT
        admin_label.grid(row=1, column=1, columnspan=2)

        self.admin_buttons["user list"].grid(row=2, column=0, columnspan=1)
        self.admin_buttons["add user"].grid(row=2, column=1, columnspan=1)
        self.admin_buttons["change password"].grid(row=2, column=2, columnspan=1)
        self.admin_buttons["return"].grid(row=2, column=3, columnspan=1)

    #   METHODS
    def user_list_push(self):
        self.controller.create_frame(UserListFrame)
        self.controller.show_frame(UserListFrame)

    def add_user_push(self):
        self.controller.create_frame(AddUserFrame)
        self.controller.show_frame(AddUserFrame)

    def change_password_push(self):
        self.controller.create_frame(ChangePasswordFrame)
        self.controller.show_frame(ChangePasswordFrame)

    def return_push(self):
        self.controller.show_frame("MenuFrame")
        # self.destroy()


# POINT OF SALES FRAME
class POSFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
        pos_label = tk.Label(self, text="POS Menu")

        pos_buttons = {
            "start of day": tk.Button(self, text="Start of Day", command=self.day_start_push),
            "new sale": tk.Button(self, text="New Sale"),
            "daily sales": tk.Button(self, text="Daily Sales"),
            "cash drop": tk.Button(self, text="Add/Drop Cash"),
            "end of day": tk.Button(self, text="End of Day"),
            "return": tk.Button(self, text="Return", command=self.return_push)
        }

        # LAYOUT
        pos_label.grid(row=0, column=0)

        pos_buttons["start of day"].grid(row=1, column=0)
        pos_buttons["new sale"].grid(row=1, column=1)
        pos_buttons["daily sales"].grid(row=1, column=2)
        pos_buttons["cash drop"].grid(row=2, column=0)
        pos_buttons["end of day"].grid(row=2, column=1)
        pos_buttons["return"].grid(row=2, column=2)

    def day_start_push(self):
        self.controller.create_frame(DayStartFrame)
        self.controller.show_frame(DayStartFrame)

    def return_push(self):
        self.controller.show_frame("MenuFrame")


# USER LIST FRAME
class UserListFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   VARIABLES
        cursor.execute("USE `users`")
        print("Using 'users'.")
        user_list_sql = "SELECT * FROM `user profiles`"
        cursor.execute(user_list_sql)
        user_list_dict = {}
        for user in cursor:
            user_list_dict[user[0]] = user[1]

        #   WIDGETS
        user_list_label = tk.Label(self, text="User List")

        self.user_list_box = tk.Listbox(self)
        for user in user_list_dict.keys():
            self.user_list_box.insert(tk.END, user)

        user_list_buttons = {
            "remove user": tk.Button(self, text="Remove", command=self.remove_user),
            "return": tk.Button(self, text="Return", command=self.frame_return)
        }

        #   LAYOUT
        user_list_label.grid(row=1, column=0)
        self.user_list_box.grid(row=2, column=0, columnspan=2)
        user_list_buttons["remove user"].grid(row=3, column=0)
        user_list_buttons["return"].grid(row=3, column=1)

    #   METHODS
    def remove_user(self):
        user_delete_sql = "DELETE FROM `user profiles` WHERE username=%s"
        removed_user = str(self.user_list_box.get(tk.ANCHOR))

        cursor.execute(user_delete_sql, (removed_user,))
        sql_db.commit()
        self.user_list_box.delete(tk.ANCHOR)

    def frame_return(self):
        self.controller.show_frame(AdminFrame)
        # self.destroy()


# ADD USER FRAME
class AddUserFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #    WIDGETS
        self.add_user_labels = {
            "add user title": tk.Label(self, text="Add User/Change Password"),
            "username": tk.Label(self, text="username:"),
            "password": tk.Label(self, text="password:"),
            "re password": tk.Label(self, text="re-enter password:"),
            "old password": tk.Label(self, text="old password:"),
            "user added": tk.Label(self, text="User added!"),
            "password changed": tk.Label(self, text="Password changed!"),
            "wrong match": tk.Label(self, text="Sorry, but you have entered an incorrect match... Try again."),
            "username already exists": tk.Label(self,
                                                text="Sorry, but the username you have chosen already exists. Try again")
        }

        self.add_user_entries = {
            "username": tk.Entry(self),
            "password": tk.Entry(self, show="*"),
            "re-enter password": tk.Entry(self, show="*"),
            "old password": tk.Entry(self, show="*")
        }

        add_user_buttons = {
            "create user": tk.Button(self, text="Create User",
                                     command=self.create_user),
            "return": tk.Button(self, text="Return", command=self.return_frame)
        }

        #   LAYOUT
        self.add_user_labels["add user title"].grid(row=0, column=0, columnspan=2)
        self.add_user_labels["username"].grid(row=1, column=0, columnspan=1)
        self.add_user_labels["password"].grid(row=2, column=0, columnspan=1)
        self.add_user_labels["re password"].grid(row=3, column=0, columnspan=1)

        self.add_user_entries["username"].grid(row=1, column=1, columnspan=2)
        self.add_user_entries["password"].grid(row=2, column=1, columnspan=2)
        self.add_user_entries["re-enter password"].grid(row=3, column=1, columnspan=2)

        add_user_buttons["create user"].grid(row=5, column=0, columnspan=1)
        add_user_buttons["return"].grid(row=5, column=2, columnspan=1)

    #   METHODS
    def create_user(self):
        self.add_user_labels["wrong match"].grid_forget()
        self.add_user_labels["username already exists"].grid_forget()
        self.add_user_labels["user added"].grid_forget()

        username_get = self.add_user_entries["username"].get()
        new_password = self.add_user_entries["password"].get()
        new_second_password = self.add_user_entries["re-enter password"].get()

        username_sql = "SELECT username FROM `user profiles` WHERE username=%s"
        insert_user_sql = "INSERT INTO `user profiles` (username, password) VALUES (%s, %s)"

        cursor.execute("USE `users`")
        print("Using 'users'.")
        cursor.execute(username_sql, (username_get,))

        if new_password != new_second_password:
            self.add_user_labels["wrong match"].grid(row=6, column=0, columnspan=3)
        elif cursor.rowcount != 0:
            self.add_user_labels["username already exists"].grid(row=6, column=0, columnspan=3)
        elif cursor.rowcount == 0:
            try:
                cursor.execute(insert_user_sql, (username_get, new_password))
                sql_db.commit()
            except Exception:
                print("Something went wrong!")
            self.add_user_labels["user added"].grid(row=6, column=0, columnspan=3)

    def return_frame(self):
        self.controller.show_frame(AdminFrame)


class ChangePasswordFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #   WIDGETS
        self.change_password_labels = {
            "change password": tk.Label(self, text="Change Password"),
            "username": tk.Label(self, text="username:"),
            "old password": tk.Label(self, text="old password:"),
            "new password": tk.Label(self, text="new password:"),
            "new password two": tk.Label(self, text="re-enter new password"),
            "password changed": tk.Label(self, text="Password changed!"),
            "wrong match": tk.Label(self, text="Sorry, but you have entered an incorrect match... Try again."),
        }

        self.change_password_entries = {
            "username": tk.Entry(self),
            "old password": tk.Entry(self, show="*"),
            "new password": tk.Entry(self, show="*"),
            "new password two": tk.Entry(self, show="*")
        }

        change_password_buttons = {
            "change password": tk.Button(self, text="change password",
                                         command=self.change_password),
            "return": tk.Button(self, text="return", command=self.return_frame)
        }

        #   LAYOUT
        self.change_password_labels["change password"].grid(row=0, column=0, columnspan=2)
        self.change_password_labels["username"].grid(row=1, column=0, columnspan=1)
        self.change_password_labels["old password"].grid(row=2, column=0, columnspan=1)
        self.change_password_labels["new password"].grid(row=3, column=0, columnspan=1)
        self.change_password_labels["new password two"].grid(row=4, column=0, columnspan=1)

        self.change_password_entries["username"].grid(row=1, column=1, columnspan=1)
        self.change_password_entries["old password"].grid(row=2, column=1, columnspan=1)
        self.change_password_entries["new password"].grid(row=3, column=1, columnspan=1)
        self.change_password_entries["new password two"].grid(row=4, column=1, columnspan=1)

        change_password_buttons["change password"].grid(row=5, column=0)
        change_password_buttons["return"].grid(row=5, column=1)

    def change_password(self):
        self.change_password_labels["wrong match"].grid_forget()
        self.change_password_labels["password changed"].grid_forget()

        change_pass_userget = self.change_password_entries["username"].get()
        change_pass_passget = self.change_password_entries["old password"].get()
        change_pass_newget = self.change_password_entries["new password"].get()
        change_pass_secondget = self.change_password_entries["new password two"].get()

        old_password_sql = "SELECT password FROM `user profiles` WHERE username=%s"
        change_password_sql = "UPDATE `user profiles` SET password=%s WHERE username=%s"

        cursor.execute("USE `users`")
        print("Using 'users'.")
        cursor.execute(old_password_sql, (change_pass_userget,))
        list_result = cursor.fetchall()[0]
        tuple_result = list_result[0]

        if change_pass_newget != change_pass_secondget:
            self.change_password_labels["wrong match"].grid(row=6, column=0, columnspan=3)
        if change_pass_passget != tuple_result:
            self.change_password_labels["wrong match"].grid(row=6, column=0, columnspan=3)
        else:
            self.change_password_labels["password changed"].grid(row=6, column=0, columnspan=3)
            cursor.execute(change_password_sql, (change_pass_newget, change_pass_userget))
            sql_db.commit()

    def return_frame(self):
        self.controller.show_frame(AdminFrame)


class DayStartFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        CURRENCY_LIST = ['$100', '$50', '$20', '$10', '$5', '$1', '$0.25', '$0.10', '$0.05', '$0.01']

        REGISTER_OFF_AMOUNT = 0
        self.OFF_AMOUNT_TYPE = IntVar()
        self.OFF_AMOUNT_TYPE.set(REGISTER_OFF_AMOUNT)

        #   WIDGETS
        #   LABELS
        ds_labels = {
            "start of day": tk.Label(self, text="Start of Day"),
            "opening reg count": tk.Label(self, text='Opening Count: '),
            "opening cur count": tk.Label(self, text='Currency Count: '),
            "count off": tk.Label(self, text='Your register count if off by: '),
            "off amount": tk.Label(self, textvariable=self.OFF_AMOUNT_TYPE)
        }

        for cur in CURRENCY_LIST:
            ds_labels[cur] = tk.Label(self, text="{}: ".format(cur))

        #   ENTRIES
        ds_entries = {
            "opening reg entry": tk.Entry(self),
        }

        for cur in CURRENCY_LIST:
            ds_entries[cur] = tk.Entry(self)

        #   BUTTONS
        ds_buttons = {
            "check count": tk.Button(self, text='Check Count'),
            "confirm count": tk.Button(self, text='Confirm Count'),
            "return": tk.Button(self, text='Return')
        }

        #   LAYOUT
        #   LABELS
        ds_labels["start of day"].grid(row=0, column=0, columnspan=1)
        ds_labels["opening reg count"].grid(row=1, column=0, sticky=tk.W)
        ds_labels["opening cur count"].grid(row=2, column=0, sticky=tk.W)

        label_row_place = 3
        for k, v in list(ds_labels.items())[5:]:
            ds_labels[k].grid(row=label_row_place, column=0, sticky=tk.E)
            label_row_place += 1

        ds_labels["count off"].grid(row=14, column=0, columnspan=1, sticky=tk.W)
        # ds_labels["off amount"].grid(row=14, column=4)

        # ENTRIES
        ds_entries["opening reg entry"].grid(row=1, column=1)
        entry_row_place = 3
        for k, v in list(ds_entries.items())[1:]:
            ds_entries[k].grid(row=entry_row_place, column=1)
            entry_row_place += 1

        #   BUTTONS
        ds_buttons["check count"].grid(row=13, column=0)
        ds_buttons["confirm count"].grid(row=13, column=1)
        ds_buttons["return"].grid(row=15, column=0)


### MAIN OPERATION ###

def main():
    # user_lst_directory()
    # user_admin_check()
    root = ContainerFrame()
    root.mainloop()


if __name__ == '__main__':
    main()
