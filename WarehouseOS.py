import pickle

#utility function to get input etc.
def invalid_input_string():
    print("Invalid Input. Please try again.", end='')

def get_valid_int(caption=""):
    while True:
        try:
            n = int(input(caption))
        except:
            invalid_input_string()
        else:
            return n

def get_valid_boolchar(caption=""):
    while True:
        n = input(caption).lower()
        if n=='y' or n=='n':
            return n

def check_out_of_index(container, index):
    try:
        container[index]
        return True
    except:
        return False

def save_data():
    acc_data = open("WOS_acc.dat", "wb")
    loc_data = open("WOS_loc.dat", "wb")
    pickle.dump(account_list, acc_data)
    pickle.dump(location_flag, loc_data)
    acc_data.close()
    loc_data.close()

def load_data(account_list, location_flag):
    try:
        acc_data = open("WOS_acc.dat", "rb")
        account_list = pickle.load(acc_data)
        acc_data.close()
    except FileNotFoundError:
        acc_data = open("WOS_acc.dat", "wb")
        acc_data.close()
    except EOFError:
        pass
    
    try:
        loc_data = open("WOS_loc.dat", "rb")
        location_flag = pickle.load(loc_data)
        loc_data.close()
    except FileNotFoundError:
        loc_data = open("WOS_loc.dat", "wb")
        loc_data.close()
    except EOFError:
        pass
    
    return account_list, location_flag

def print_location_data():
    for i in range(100):
        print(location_flag[i], end=' ')
    print()

def print_all_account():
    if len(account_list)==0:
        print("No account exists.")
    else:
        for i in range(len(account_list)):
            print(i+1, ">")
            account_list[i].to_string()

def choose_account():
    print("[CHOOSE ACCOUNT]")
    print_all_account()
    idx = get_valid_int("Choose Account: ") - 1
    if check_out_of_index(account_list, idx):
        return idx
    else:
        invalid_input_string()
        print()
        choose_account()

def find_item(item_key):
    for acc in account_list:
        for itm in acc.items:
            key = itm.__class__.__name__ + itm.name
            if itm.__class__.__name__ == "Car":
                key = key + itm.model + itm.color
            elif itm.__class__.__name__ == "Luggage":
                key = key + itm.brand + itm.color
            elif itm.__class__.__name__ == "Cargo":
                for c_itm in itm.content:
                    if c_itm.__class__.__name__ == "Car":
                        key = key + c_itm.model + c_itm.color
                    elif c_itm.__class__.__name__ == "Luggage":
                        key = key + c_itm.brand + c_itm.color
                    else:
                        key = key + c_itm.name

            if str(item_key).lower() in key.lower():
                itm.to_string()
                print("=======================================")
                print("Owned by: " + acc.name)
                print("Located at: " + itm.location)
    print()

#functions to alter/mutate account_list
def add_account(name=None, age=None, phone=None, email=None, address=None):
    print("[CREATE ACCOUNT]")
    name = input("Name: ") if name==None else name
    age = get_valid_int("Age: ") if age==None else age
    phone = input("Phone Number: ") if phone==None else phone
    email = input("Email: ") if email==None else email
    address = input("Address: ") if address==None else address
    account_list.append(Account(name, age, phone, email, address))
    print("[ACCOUNT CREATED]")
    save_data()

def delete_account(idx=None):
    for acc in account_list:
        acc_number = account_list.index(acc)+1
        print(str(acc_number) + ">")
        acc.to_string()
    print("NOTE: All of deleted account's item will be withdrawn!")
    acc_index = get_valid_int("Delete Account (Input 0 to cancel): ")
    if acc_index==0: return
    while not check_out_of_index(account_list, acc_index-1):
        if acc_index==0: return
        print("Account Number", acc_index, "does not exist. Please try again.")
        acc_index = get_valid_int("Delete Account (Input 0 to cancel): ")
    for item in account_list[acc_index-1].items:
        item.location = item.location[1]
        location_flag[int(item.location)-1] = True
    del account_list[acc_index-1]
    print("[ACCOUNT DELETED]")
    save_data()


#essential variables
account_list = []
location_flag = []
for i in range(100):
    location_flag.append(True)

#classes
class Account:
    def __init__(self, name, age, phone, email, address):
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.address = address
        self.items = [] #Account has 0 item when first registering
    
    def to_string(self):
        print("[GENERAL INFORMATION]")
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Address: " + self.address)
        print("[CONTACT INFORMATION]")
        print("Phone: " + self.phone)
        print("Email: " + self.email)
        print("[POSSESSED ITEMS]")
        if len(self.items) == 0:
            print("No item exists.")
        else:
            for i in self.items:
                item_number = self.items.index(i)+1
                print(str(item_number) + ">")
                i.to_string()
        print('\n')

    def deposit(self, select=None, name=None, model=None, color=None, brand=None, c_select=None):
        if True not in location_flag:
            print("WAREHOUSE FULL!")
            return
        location = str(location_flag.index(True)+1)
        print("[DEPOSIT NEW ITEM]")
        print("1. CAR")
        print("2. LUGGAGE")
        print("3. CARGO")
        print("4. CUSTOM ITEM")
        print("5. BACK")
        print("> ", end='')
        select = get_valid_int() if select==None else select
        if select==1:
            name = input("Car Name: ") if name==None else name
            model = input("Car Model: ") if model==None else model
            color = input("Car Color: ") if color==None else color
            self.items.append(Car(name, "#" + location, model, color))
            location_flag[int(location)-1] = False
            save_data()
        elif select==2:
            name = input("Luggage Name: ") if name==None else name
            brand = input("Luggage Brand: ") if brand==None else brand
            color = input("Luggage Color: ") if color==None else color
            self.items.append(Luggage(name, "#" + location, brand, color))
            location_flag[int(location)-1] = False
            save_data()
        elif select==3:
            name = input("Cargo Name: ") if name==None else name
            new_cargo = Cargo(name, location)
            new_cargo.deposit() if c_select==None else new_cargo.deposit(c_select)
            self.items.append(new_cargo)
            location_flag[int(location)-1] = False
            save_data()
        elif select==4:
            name = input("Item Name: ") if name==None else name
            self.items.append(Item(name, "#" + location))
            location_flag[int(location)-1] = False
            save_data()
        elif select==5:
            return
        else:
            invalid_input_string()
            print() #extra line
            self.deposit()

    def withdraw(self, idx = None):
        for i in self.items:
            item_number = self.items.index(i)+1
            print(str(item_number) + ">")
            i.to_string()
        print("[WITHDRAW ITEM]")
        item_index = get_valid_int("Withdraw item number (Input 0 to cancel): ") if idx==None else idx
        if item_index==0: return
        while not check_out_of_index(self.items, item_index-1):
            print("Item Number", item_index, "does not exist. Please try again.")
            item_index = get_valid_int("Withdraw item number (Input 0 to cancel): ")
        del self.items[item_index-1]
        print("[WITHDRAW SUCCESSFUL]")
        save_data()

class Item:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def to_string(self):
        print("[GENERAL INFORMATION]")
        print("Type: " + self.__class__.__name__)
        print("Name: " + self.name)
        print("Location: " + self.location)

class Car(Item):
    def __init__(self, name, location, model, color):
        super().__init__(name, location)
        self.model = model
        self.color = color

    def to_string(self):
        super().to_string()
        print("[CAR INFORMATION]")
        print("Model: " + self.model)
        print("Color: " + self.color)


class Luggage(Item):
    def __init__(self, name, location, brand, color):
        super().__init__(name, location)
        self.brand = brand
        self.color = color

    def to_string(self):
        super().to_string()
        print("[LUGGAGE/BAG INFORMATION]")
        print("Brand: " + self.brand)
        print("Color: " + self.color)

class Cargo(Item):
    def __init__(self, name, location):
        super().__init__(name, location)
        self.content = []

    def deposit(self, select=None):
        print("[CARGO - DEPOSIT]")
        print("1. CAR")
        print("2. LUGGAGE")
        print("3. CUSTOM ITEM")
        print("4. BACK")
        print("> ", end='')
        select = get_valid_int() if select==None else select
        if select==1:
            name = input("Car Name: ")
            model = input("Car Model: ")
            color = input("Car Color: ")
            self.content.append(Car(name, "CARGO - LOCATION #" + self.location, model, color))
            more = get_valid_boolchar("Insert More Items? (Y/N) ")
            if more == 'y':
                self.deposit()
            else:
                return
        elif select==2:
            name = input("Luggage Name: ")
            brand = input("Luggage Brand: ")
            color = input("Luggage Color: ")
            self.content.append(Luggage(name, "CARGO - LOCATION #" + self.location, brand, color))
            more = get_valid_boolchar("Insert More Items? (Y/N) ")
            if more == 'y':
                self.deposit()
            else:
                return
        elif select==3:
            name = input("Item Name: ")
            self.content.append(Item(name, "CARGO - LOCATION #" + self.location))
            more = get_valid_boolchar("Insert More Items? (Y/N) ")
            if more == 'y':
                self.deposit()
            else:
                return
        elif select==4:
            return
        else:
            invalid_input_string()
            print() #extra line
            self.deposit()
    
    def to_string(self):
        super().to_string()
        print("[CARGO DETAILS - CONTENTS]")
        for i in self.content:
            i.to_string()

# Main Menu Starts Here
# ---------------------
# <Requirement>
# -> Create account
# -> Remove account
# -> Deposit items
# -> Withdraw items
# -> View all accounts
# -> Container/item location

if __name__ == "__main__":
    account_list, location_flag = load_data(account_list, location_flag)

while True:
    print("[MAIN MENU]                      ")
    print("1. Create Account                ")
    print("2. Remove Account                ")
    print("3. Deposit Items                 ")
    print("4. Withdraw Items                ")
    print("5. Display all Accounts          ")
    print("6. Find Item/Container Location  ")
    print("7. Exit Program                  ")
    print("> ", end='')
    select = get_valid_int()
    if select == 1: #create account
        add_account()
    elif select == 2: #remove account
        delete_account()
    elif select == 3: #deposit items
        if len(account_list)==0:
            print("No account exists. Cannot Withdraw")
            continue
        acc_idx = choose_account()
        acc = account_list[acc_idx]
        acc.deposit()
    elif select == 4: #withdraw items
        if len(account_list)==0:
            print("No account exists. Cannot Withdraw")
            continue
        acc_idx = choose_account()
        acc = account_list[acc_idx]
        acc.withdraw()
    elif select == 5: #display all accounts
        print_all_account()
    elif select == 6: #find item/container
        item_key = input("Search: ")
        find_item(item_key)
    elif select == 7:
        quit() #exit program
    else:
        invalid_input_string()
