import unittest
from WarehouseOS import *

class WarehouseOS_Test(unittest.TestCase):

    # //----------------------------------------------
    # // Utility Function Tests
    # //----------------------------------------------
    def test_check_out_of_index(self):
        test_list = []
        check_out_of_index(test_list, 999) #testing out of bounds
        check_out_of_index(test_list, -1200) #testing out of bounds
        test_list = [1, 2, 3]
        check_out_of_index(test_list, 0)
        check_out_of_index(test_list, 1)
        check_out_of_index(test_list, 2)

    # //----------------------------------------------
    # // Basic Account Creation Function Tests
    # //----------------------------------------------
    def test_add_account(self):
        add_account("Testing", 999, "999-89531", "test_email@emailhost.com", "Test Addr. 2nd Avenue, Testown")
        added_account = account_list[len(account_list)-1]
        self.assertIn(added_account, account_list) #assert whether or not the account has been created

    def test_delete_account(self):
        #deconstructed function for assert purposes
        for acc in account_list:
            acc_number = account_list.index(acc)+1
            print(str(acc_number) + ">")
            acc.to_string()
        print("NOTE: All of deleted account's item will be withdrawn!")
        acc_index = 1 #existing account deleted
        if acc_index==0: return
        while not check_out_of_index(account_list, acc_index-1):
            if acc_index==0: return
            print("Account Number", acc_index, "does not exist. Please try again.")
            acc_index = get_valid_int("Delete Account (Input 0 to cancel): ")
        for item in account_list[acc_index-1].items:
            location_flag[int(item.location)-1] = True
            self.assertTrue(location_flag[int(item.location)-1]) #assert whether or not that item slot has been freed
        deleted_account = account_list[acc_index-1]
        del account_list[acc_index-1]
        print("[ACCOUNT DELETED]")
        self.assertNotIn(deleted_account, account_list) #assert whether or not the account has been deleted

    # //----------------------------------------------
    # // Basic Item Creation Function Tests
    # //----------------------------------------------
    def test_deposit(self):
        acc = Account("Testing", 999, "999-89531", "test_email@emailhost.com", "Test Addr. 2nd Avenue, Testown")
        acc.deposit(1, "Porsche", "911", "Meteorite Gray")
        car = acc.items[len(acc.items)-1]
        acc.deposit(2, "Carry Bag", None, "Brown", "Louis Vuitton")
        bag = acc.items[len(acc.items)-1]
        acc.deposit(3, "Anne's Present")
        cargo = acc.items[len(acc.items)-1]
        acc.deposit(4, "Golden Apple")
        custom_item = acc.items[len(acc.items)-1]
        self.assertIn(car, acc.items)
        self.assertIn(bag, acc.items)
        self.assertIn(cargo, acc.items)
        self.assertIn(custom_item, acc.items)
    
    def test_withdraw(self):
        acc = Account("Testing", 999, "999-89531", "test_email@emailhost.com", "Test Addr. 2nd Avenue, Testown")
        acc.deposit(1, "Porsche", "911", "Meteorite Gray")
        acc.withdraw(0)

suite = unittest.TestLoader().loadTestsFromTestCase(WarehouseOS_Test)
unittest.TextTestRunner(verbosity=2).run(suite)