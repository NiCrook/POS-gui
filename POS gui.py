import tkinter as tk
from tkinter import IntVar, StringVar


class POSGui:

    CURRENCY_LIST = ['$100', '$50', '$20', '$10', '$5', '$1', '$0.25', '$0.10', '$0.05', '$0.01']

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame()
        self.frame.grid()

        # VARIABLES
        self.user_name = None
        self.register_incorrect = 0
        self.transaction_total = 0
        self.cash_due = 0

        self.user_name_text = StringVar()
        self.register_incorrect_text = IntVar()
        self.transaction_total_text = IntVar()
        self.cash_due_text = IntVar()

        self.user_name_text.set(self.user_name)
        self.register_incorrect_text.set(self.register_incorrect)
        self.transaction_total_text.set(self.transaction_total)
        self.cash_due_text.set(self.cash_due)

        # WIDGETS
        for cur in POSGui.CURRENCY_LIST:
            cur = IntVar()
            self.currency_labels = {
                cur: tk.Label(self.frame, text=cur)
            }
            self.currency_buttons = {
                cur: tk.Button(self.frame, text=cur)
            }
            self.currency_entries = {
                cur: tk.Entry(self.frame)
            }

        self.labels = {
            'program_name_label': tk.Label(self.frame, text='Cash Register System v1.0'),
            'welcome_label': tk.Label(self.frame, text='Welcome!'),
            'username_label': tk.Label(self.frame, text='Username:'),
            'password_label': tk.Label(self.frame, text='Password:'),
            're_password_label': tk.Label(self.frame, text='Re-enter Password:'),
            'wrong_user/pass_label': tk.Label(self.frame, text='You have entered a wrong username/password. Try again'),
            'hello_user_label': tk.Label(self.frame, text='Hello! Select an item below.'),
            'admin_label': tk.Label(self.frame, text='Admin Screen'),
            'pos_label': tk.Label(self.frame, text='Point Of Sales'),
            'opening_register_label': tk.Label(self.frame, text='Opening register count:'),
            'opening_currency_label': tk.Label(self.frame, text='Opening currency count:'),
            'closing_register_label': tk.Label(self.frame, text='Closing register count:'),
            'closing_currency_label': tk.Label(self.frame, text='Closing currency count:'),
            'register_wrong_label': tk.Label(self.frame, text='Your register count is off...'),
            'register_wrong_amount_label': tk.Label(self.frame, textvariable=self.register_incorrect_text),
            'enter_UPC_label': tk.Label(self.frame, text='Enter UPC:'),
            'count_label': tk.Label(self.frame, text='Count:'),
            'total_label': tk.Label(self.frame, text='Total:'),
            'cash_received_label': tk.Label(self.frame, text='Cash received:'),
            'cash_due_label': tk.Label(self.frame, text='Cash due:'),
            'current_register_count_label': tk.Label(self.frame, text='Register count:')
        }

        self.buttons = {
            'start_button': tk.Button(self.frame, text='Start', command=self.welcome_button_push),
            # 'login_button': tk.Button(self.frame, text='login', command=self.login_button_push),
            # 'admin_button': tk.Button(self.frame, text='Admin', command=pass),
            # 'POS_button': tk.Button(self.frame, text='POS', command=pass),
            # 'admin_user_list_button': tk.Button(self.frame, text='User List', command=pass),
            # 'remove_user_button': tk.Button(self.frame, text='Remove User', command=pass),
            # 'admin_add_user_button': tk.Button(self.frame, text='Add User', command=pass),
            # 'create_user_button': tk.Button(self.frame, text='Create User', command=pass),
            # 'admin_change_password_button': tk.Button(self.frame, text='Change Pass', command=pass),
            # 'change_password_button': tk.Button(self.frame, text='Change Pass', command=pass),
            # 'start_day_button': tk.Button(self.frame, text='Start of Day', command=pass),
            # 'pos_new_sale_button': tk.Button(self.frame, text='New Sale', command=pass),
            # 'today_sales_button': tk.Button(self.frame, text="Today's Sales", command=pass),
            # 'add_drop_cash_button': tk.Button(self.frame, text='Add/Drop Cash', command=pass),
            # 'end_day_button': tk.Button(self.frame, text='End of Day', command=pass),
            # 'recount_button': tk.Button(self.frame, text='Recount', command=pass),
            # 'accept_count_button': tk.Button(self.frame, text='Accept', command=pass),
            # 'add_product_button': tk.Button(self.frame, text='Add', command=pass),
            # 'remove_product_button': tk.Button(self.frame, text='Remove', command=pass),
            # 'confirm_transaction_button': tk.Button(self.frame, text='Confirm', command=pass),
            # 'sale_new_sale_button': tk.Button(self.frame, text='New Sale', command=pass),
            # 'add_cash_button': tk.Button(self.frame, text='Add', command=pass),
            # 'drop_cash_button': tk.Button(self.frame, text='Drop', command=pass),
            # 'return_frame_button': tk.Button(self.frame, text='Return', command=pass)
        }

        self.entries = {
            'username_entry': tk.Entry(self.frame),
            'password_entry': tk.Entry(self.frame, show='*'),
            're_password_entry': tk.Entry(self.frame, show='*'),
            'open_reg_count_entry': tk.Entry(self.frame),
            'enter_upc_entry': tk.Entry(self.frame),
            'upc_count_entry': tk.Entry(self.frame),
            'cash_received_entry': tk.Entry(self.frame)
        }

        self.listboxes = {
            'user_list_box': tk.Listbox(self.frame),
            'cart_items_box': tk.Listbox(self.frame)
        }

        self.welcome_frame()

    def welcome_frame(self):
        self.labels['program_name_label'].grid(row=0, column=0)
        self.labels['welcome_label'].grid(row=1, column=0)
        self.buttons['start_button'].grid(row=2, column=0)

    def welcome_button_push(self):
        self.labels['program_name_label'].grid_forget()
        self.labels['welcome_label'].grid_forget()
        self.buttons['start_button'].grid_forget()
        self.labels['username_label'].grid(row=0, column=0)
        self.labels['password_label'].grid(row=1, column=0)


def main():
    root = tk.Tk()
    POS_gui = POSGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
