import display, os

# Global Variables

user_list = []
bill_list = []
error_message = []

# Utility Functions

def update_display():
    os.system('cls')
    print(display.banner)
    if len(user_list) > 0:
        print('Users:')
        count = 1
        for i in user_list:
            print(str(count) + '. ' + i.name + ' - $' + str(i.amount_paid))
            count += 1
    print('\n')
    if len(bill_list) > 0:
        print('Bills:')
        count = 1
        for i in bill_list:
            print(str(count) + '. ' + i.name + ' - $' + str(i.cost))
            count += 1
        print('\n')
        print('Total Cost: $' + str(calculate_total()))
        print('\n')
    if len(error_message) > 0:
        print(error_message[0])
        error_message.pop()

def add_user(name):
    user_list.append(User(name))

def remove_user(user_index):
    user_list.pop(user_index)

def add_bill(name, cost, user_index):
    bill_list.append(Bill(name, cost, user_index))
    user_list[user_index].add_money(cost)

def remove_bill(bill_index):
    bill = bill_list[bill_index]
    removed_from = bill.get_user()
    user = user_list[removed_from]
    user.remove_money(bill.get_cost())
    bill_list.pop(bill_index)

def reassign_bill(bill_index, user_index):
    bill = bill_list[bill_index]
    old_user = user_list[bill.get_user()]
    new_user = user_list[user_index]
    if old_user != new_user:
        old_user.remove_money(bill.get_cost())
        new_user.add_money(bill.get_cost())
        bill.set_user(user_index)
    else:
        pin_msg(old_user.get_name() + " is already paying for " + bill.get_name() + "!\n")

def pin_msg(message):
    if len(error_message) != 0:
        error_message.pop()
    error_message.append(message)

# Menu Functions

def main_menu():
    update_display()
    if len(user_list) == 0:
        print("Welcome to my first Python app! Please start by entering 2 users!")
        user = input("Name 1: ").upper()
        add_user(user)
        update_display()
        user = input("Name 2: ").upper()
        add_user(user)
        main_menu()
    else:
        print("What would you like to do?")
        response = input("1 - Manage Users\n2 - Manage Bills\n3 - Finalize Results\nAnswer: ")
        if response == "1":
            manage_users()
        elif response == "2":
            manage_bills()
        elif response == "3":
            if len(bill_list) == 0:
                main_menu()
            else:
                confirm_results()
        else:
            print("Please try again.")
            main_menu()

def manage_users():
    update_display()
    print("What would you like to do?")
    response = input("1 - Add New User\n2 - Remove User\n3 - Go Back\nAnswer: ")
    if response == "1":
        add_user_prompt()
    elif response == "2":
        if len(user_list) == 0:
            print("Number of users cannot be less than 2!")
            manage_users()
        remove_user_prompt()
    elif response == "3":
        main_menu()
    else:
        manage_users()

def manage_bills():
    update_display()
    print("What would you like to do?")
    response = input("1 - Add Bill\n2 - Remove Bill\n3 - Reassign Bill\n4 - Go Back\nAnswer: ")
    if response == "1":
        add_bill_prompt()
    elif response == "2":
        if len(bill_list) == 0:
            manage_bills()
        elif len(bill_list) == 1:
            remove_bill(0)
            manage_bills()
        else:
            remove_bill_prompt()
    elif response == "3":
        if len(bill_list) == 0:
            print("No bills available to reassign!")
            manage_bills()
        else:
            reassign_bill_prompt()
    elif response == "4":
        main_menu()
    else:
        print("Please try again.")
        manage_bills()

def confirm_results():
    update_display()
    print("Are you sure you want to finalize the results?")
    response = input("1 - Yes\n2 - No\nAnswer: ")
    if response == "1":
        print_results()
    elif response == "2":
        main_menu()
    else:
        print("Please try again.")
        confirm_results()

# Prompt Functions

def add_user_prompt():
    name = input("Enter name: ").upper()
    add_user(name)
    pin_msg(name + " has been added!\n")
    manage_users()

def remove_user_prompt():
    if len(user_list) <= 2:
        pin_msg("Cannot have less than 2 users!\n")
        manage_users()
    else:
        try: 
            user_index_to_remove = int(input("Which # user would you like to remove? (1-"+str(len(user_list))+")\nAnswer: ")) - 1
        except ValueError:
            pin_msg("Invalid input, please try again.\n")
            manage_users()
        if user_index_to_remove >= 0 and user_index_to_remove < len(user_list):
            if user_list[user_index_to_remove].get_money() != 0:
                pin_msg("Please reassign bills before removing this user!\n")
                manage_users()
            else:
                pin_msg(user_list[user_index_to_remove].get_name() + " has been removed!\n")
                remove_user(user_index_to_remove)
                manage_users()
        else:
            pin_msg("Invalid input, please try again.\n")
            remove_user_prompt()

def add_bill_prompt():
    name = input("Enter name: ").upper()
    try:
        cost = round(float(input("How much does "+ name +" cost per month?\nAnswer: $")), 2)
    except ValueError:
        pin_msg("Invalid input, please try again.\n")
        add_bill_prompt()
    try:
        user_index = int(input("Which user is paying for " + name + "? (1-"+str(len(user_list))+")\nAnswer: ")) - 1
    except ValueError:
        pin_msg("Invalid input, please try again.\n")
        add_bill_prompt()
    pin_msg(name + " has been added!\n")
    add_bill(name, cost, user_index)
    manage_bills()

def remove_bill_prompt():
    try:
        bill_index = int(input("Which # bill would you like to remove? (1-"+str(len(bill_list))+"): ")) - 1
    except ValueError:
        pin_msg("Invalid input, please try again.\n")
        manage_bills()
    if bill_index >= 0 and bill_index < len(bill_list):
        pin_msg(bill_list[bill_index].get_name() + " has been removed!\n")
        remove_bill(bill_index)
        manage_bills()
    else:
        pin_msg("Invalid input, please try again.\n")
        manage_bills()

def reassign_bill_prompt():
    if len(bill_list) == 0:
        pin_msg("No bills to reassign!")
        manage_bills()
    elif len(bill_list) == 1:
        try:
            user_index = int(input("Which # user is paying for "+bill_list[0].get_name()+"? (1-"+str(len(user_list))+")\nAnswer: ")) - 1
            if user_index >= 0 and user_index < len(user_list):
                reassign_bill(0, user_index)
                manage_bills()
            else:
                pin_msg("Invalid input, please try again.\n")
                manage_bills()
        except ValueError:
            pin_msg("Invalid input, please try again.\n")
            manage_bills()
    else:
        try:
            bill_index = int(input("Which # bill would you like to reassign? (1-"+str(len(bill_list))+")\nAnswer: ")) - 1
        except ValueError:
            pin_msg("Invalid input, please try again.\n")
            manage_bills()
        if bill_index >= 0 and bill_index < len(bill_list):
            try:
                user_index = int(input("Which # user is paying for "+bill_list[bill_index].get_name()+"? (1-"+str(len(user_list))+"):\nAnswer: ")) - 1
            except ValueError:
                pin_msg("Invalid input, please try again.\n")
                manage_bills()
        else:
            pin_msg("Invalid input, please try again.\n")
            manage_bills()
        if user_index >= 0 and user_index < len(user_list):
            pin_msg(bill_list[bill_index].get_name() + " has been reassigned to " + user_list[user_index].get_name() + "!\n")
            reassign_bill(bill_index, user_index)
            manage_bills()
        else:
            pin_msg("Invalid input, please try again.\n")
            manage_bills()
    
# Global Functions

def calculate_total():
    total = []
    for i in user_list:
        total.append(i.get_money())
    return sum(total)

def print_results():
    each_share = round(calculate_total() / len(user_list), 2)
    for i in user_list:
        i.calculate_difference(each_share)
    winner_name = return_winner()[0]
    winner_index = return_winner()[1]
    for i in user_list:
        if i.difference <= 0:
            print(i.get_name() + " owes " + winner_name + ": $" + str(abs(i.calculate_difference()))+"\n")
    input("Press Enter to restart.\n")
    restart()

def restart():
    while len(user_list) > 0:
        user_list.pop()
    while len(bill_list) > 0:
        bill_list.pop()
    main_menu()

def return_winner():
    max_range = len(user_list) - 1
    i = 0
    winner = -1
    while i in range(0, max_range) and winner < 0:
        if user_list[i].calculate_difference() > 0:
            winner = i
        i += 1
    return [user_list[winner].get_name(), winner]

# Classes

class User():
    def __init__(self, name):
        self.name = name
        self.amount_paid = 0
        self.difference = 0

    def add_money(self, cost):
        self.amount_paid += float(cost)

    def remove_money(self, cost):
        self.amount_paid -= float(cost)

    def get_name(self):
        return self.name

    def get_money(self):
        return self.amount_paid
    
    def calculate_difference(self, amount=0):
        if amount != 0:
            self.difference = self.amount_paid - amount
        return self.difference

class Bill():
    def __init__(self, name, cost, user):
        self.name = name
        self.cost = float(cost)
        self.user_index = user

    def get_name(self):
        return self.name
    
    def get_cost(self):
        return self.cost

    def get_user(self):
        return self.user_index
    
    def set_user(self, user):
        self.user_index = int(user)
    
main_menu()