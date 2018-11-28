import pickle

#utility function to get input etc.
def invalid_input_string(): #a string that will be displayed if something is invalid
    print("Invalid Input. Please try again.", end='')

def get_valid_int(caption=""): #returns a valid integer
    while True:
        try:
            n = int(input(caption)) #keep asking for input
        except:
            invalid_input_string() #look at invalid_input_string() function above
        else:
            return n #until that particular input was a valid integer

def get_valid_boolchar(caption=""): #returns true if 'y' is input, false if 'n' is input (case insensitive)
    while True:
        n = input(caption).lower() #keep asking for input
        if n=='y' or n=='n': 
            return n #until it's either 'y' and 'n'

def check_out_of_index(container, index): #returns true if index is in container, false if not
    try:
        container[index] #check for index in container
        return True #if it is not out of bounds
    except:
        return False #if it is out of bounds

def save_data(): #saves account_list and location_flag to WOS_acc.dat and WOS_loc.dat respectively
    acc_data = open("WOS_acc.dat", "wb") #open file WOS_acc.dat in 'write-binary' form
    loc_data = open("WOS_loc.dat", "wb") #open file WOS_loc.dat in 'write-binary' form
    pickle.dump(account_list, acc_data) #store/write data in accouont_list to WOS_acc.dat
    pickle.dump(location_flag, loc_data) #store/write data in location_flag to WOS_loc.dat
    acc_data.close() #close 'stream' for file WOS_acc.dat
    loc_data.close() #close 'stream' for file WOS_loc.dat

def load_data(account_list, location_flag): #loads WOS_acc.dat and WOS_loc.dat and assign them to account_list and location_flag respectively
    try:
        acc_data = open("WOS_acc.dat", "rb") #open file WOS_acc.dat in 'read-binary' form.
        account_list = pickle.load(acc_data) #load WOS_acc.dat and store its content to account_list
        acc_data.close() #close 'stream' for file WOS_acc.dat
    except FileNotFoundError: #if WOS_acc.dat does not exist
        acc_data = open("WOS_acc.dat", "wb") #create that file by opening it in 'write-binary' form
        acc_data.close() #close 'stream' for file WOS_acc.dat
    except EOFError: #if file is empty
        pass #do nothing
    
    try:
        loc_data = open("WOS_loc.dat", "rb") #open file WOS_loc.dat in 'read-binary' form.
        location_flag = pickle.load(loc_data) #load WOS_loc.dat and store its content to llocation_flag
        loc_data.close() #close 'stream' for file WOS_loc.dat
    except FileNotFoundError: #if WOS_loc.dat does not exist
        loc_data = open("WOS_loc.dat", "wb") #create that file by opening it in 'write-binary' form
        loc_data.close() #close 'stream' for file WOS_loc.dat
    except EOFError: #if file is empty
        pass #do nothing
    
    return account_list, location_flag #return value of account_list and location_flag (will be assign to account_list(global variable) and location_flag(global variable) respectively)

def print_location_data(): #(debug only) used to print out all locations availability
    for i in range(100): #looping for 0 to 99
        print(location_flag[i], end=' ') #print location_flag by that index and adds a space
    print()

def print_all_account(): #prints all deatils about all accounts
    if len(account_list)==0: #if account_list is empty
        print("No account exists.")
    else: #if not empty
        for i in range(len(account_list)): #looping from 0 to size of account_list
            print(i+1, ">") #prints i+1 and adds a ">"
            account_list[i].to_string() #call to_string() function to account_list at index i

def choose_account(): #choose account and return its index
    print("[CHOOSE ACCOUNT]")
    print_all_account() #refer to print_all_account() function above
    idx = get_valid_int("Choose Account: ") - 1 #refer to get_valid_int() function above. this line gets a valid int and subtract that by 1
    while not check_out_of_index(account_list, idx): #refer to check_out_of_index() function above. looping while not in bounds
        invalid_input_string() #refer to invalid_input_string() function above
        print() #extra space
        idx = get_valid_int("Choose Account: ") - 1 #refer to get_valid_int() function above. this line gets a valid int and subtract that by 1
    return idx #return index
        

def find_item(item_key): #find a particular item based on its attributes, name and/or type.
    for acc in account_list: #looping all accounts in account_list
        for itm in acc.items: #looping all items in that account
            key = itm.__class__.__name__ + itm.name #key = (class name of item) + (name of item)
            if itm.__class__.__name__ == "Car": #if class of item is car
                key = key + itm.model + itm.color #combine string key above with car model and car color
            elif itm.__class__.__name__ == "Luggage": #if class of item is luggage
                key = key + itm.brand + itm.color #combine string key above with luggage brand and luggage color
            elif itm.__class__.__name__ == "Cargo": #if class of item is cargo
                for c_itm in itm.content: #looping all items in cargo
                    if c_itm.__class__.__name__ == "Car": #if class of cargo item is car
                        key = key + c_itm.model + c_itm.color #combine string key above with car model and car color
                    elif c_itm.__class__.__name__ == "Luggage": #if class of item is luggage
                        key = key + c_itm.brand + c_itm.color #combine string key above with luggage brand and luggage color
                    else: #if item is custom item
                        key = key + c_itm.name #combine string key above with item name

            if str(item_key).lower() in key.lower(): #if the word search is in the key combined above
                itm.to_string() #call to_string() function from item (this will differ based on what class that particular item is in)
                print("=======================================")
                print("Owned by: " + acc.name)
                print("Located at: " + itm.location)
    print()

#functions to alter/mutate account_list
def add_account(name=None, age=None, phone=None, email=None, address=None): #add account to account_list
    print("[CREATE ACCOUNT]")
    name = input("Name: ") if name==None else name #input name
    age = get_valid_int("Age: ") if age==None else age #input age
    phone = input("Phone Number: ") if phone==None else phone #input phone number
    email = input("Email: ") if email==None else email #input email
    address = input("Address: ") if address==None else address #input address
    account_list.append(Account(name, age, phone, email, address)) #add to account_list array
    print("[ACCOUNT CREATED]")
    save_data() #refer to save_data() function above

def delete_account(idx=None): #delete an account and automatically withdraw all items he/she possessed
    for acc in account_list: #looping all account in account_list
        acc_number = account_list.index(acc)+1 #acc_number will be (index of current looped account) + 1
        print(str(acc_number) + ">")
        acc.to_string() #call to_string() function to acc
    print("NOTE: All of deleted account's item will be withdrawn!")
    acc_index = get_valid_int("Delete Account (Input 0 to cancel): ") #get valid int for index
    if acc_index==0: return #if index is 0 cancel deletion
    while not check_out_of_index(account_list, acc_index-1):
        if acc_index==0: return #if index is 0 cancel deletion
        print("Account Number", acc_index, "does not exist. Please try again.")
        acc_index = get_valid_int("Delete Account (Input 0 to cancel): ") #get valid int for index
    for item in account_list[acc_index-1].items: #looping item in account_list[acc_index-1]'s item list
        item.location = item.location if len(item.location)==1 else item.location[1] 
        location_flag[int(item.location)-1] = True #set that item location to available or true
    del account_list[acc_index-1] #delete that account when we are done
    print("[ACCOUNT DELETED]")
    save_data() #refer to save_data() function above


#essential variables
account_list = [] #store all account
location_flag = [] #store all location availability
for i in range(100): #assign all locations to 'available' by default
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
    
    def to_string(self): #represents an account in a clear and detailed manner
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

    def deposit(self, select=None, name=None, model=None, color=None, brand=None, c_select=None): #deposits an item to an account
        if True not in location_flag: #if location_flag is all false or FULL
            print("WAREHOUSE FULL!")
            return
        location = str(location_flag.index(True)+1) #assign the first True value in location_flag to location variable
        print("[DEPOSIT NEW ITEM]")
        print("1. CAR")
        print("2. LUGGAGE")
        print("3. CARGO")
        print("4. CUSTOM ITEM")
        print("5. BACK")
        print("> ", end='')
        select = get_valid_int() if select==None else select #select menu
        if select==1:
            name = input("Car Name: ") if name==None else name #input car name
            model = input("Car Model: ") if model==None else model #input car model
            color = input("Car Color: ") if color==None else color #input car color
            self.items.append(Car(name, "#" + location, model, color)) #add car to account item list
            location_flag[int(location)-1] = False #flag that location (the one that was assigned to this item) to false (not available anymore)
            save_data() #refer to save_data() function above
        elif select==2:
            name = input("Luggage Name: ") if name==None else name #input luggage name
            brand = input("Luggage Brand: ") if brand==None else brand #input luggage brand
            color = input("Luggage Color: ") if color==None else color #input luggage color
            self.items.append(Luggage(name, "#" + location, brand, color)) #add luggage to account item list
            location_flag[int(location)-1] = False #flag that location (the one that was assigned to this item) to false (not available anymore)
            save_data() #refer to save_data() function above
        elif select==3:
            name = input("Cargo Name: ") if name==None else name #input cargo name
            new_cargo = Cargo(name, location) #create cargo object
            new_cargo.deposit() if c_select==None else new_cargo.deposit(c_select)
            self.items.append(new_cargo) #add cargo to account item list
            location_flag[int(location)-1] = False #flag that location (the one that was assigned to this item) to false (not available anymore)
            save_data() #refer to save_data() function above
        elif select==4:
            name = input("Item Name: ") if name==None else name #input custom item name
            self.items.append(Item(name, "#" + location)) #add custom item to account item list
            location_flag[int(location)-1] = False #flag that location (the one that was assigned to this item) to false (not available anymore)
            save_data() #refer to save_data() function above
        elif select==5:
            return
        else:
            invalid_input_string() #refer to invalid_input_string() function above
            print() #extra line
            self.deposit() #re-execute this function

    def withdraw(self, idx = None): #withdraw an item and clear its location
        for i in self.items: #looping item in item list
            item_number = self.items.index(i)+1
            print(str(item_number) + ">")
            i.to_string()
        print("[WITHDRAW ITEM]")
        item_index = get_valid_int("Withdraw item number (Input 0 to cancel): ") if idx==None else idx  #get valid int to item_index
        if item_index==0: return
        while not check_out_of_index(self.items, item_index-1): #looping while index is out of bounds
            print("Item Number", item_index, "does not exist. Please try again.")
            item_index = get_valid_int("Withdraw item number (Input 0 to cancel): ") #get valid int to item_index
        del self.items[item_index-1] #delete that item from item list
        print("[WITHDRAW SUCCESSFUL]")
        save_data() #refer to save_data() function above

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
            print("No account exists. Cannot Deposit")
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
