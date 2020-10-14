#!/usr/bin/env python3
"""
This module contains the Driver class and serves as the entry point
for the Family Appointed Moderator application.
"""
from menu import Menu
from transaction import TransactionManager, Transaction
from budget import BudgetManager, Budget
from user import User

USER_TEST_DATA = {
    "name": "Edwin Pau",
    "age": "31",
    "user_type": "1",
    "bank_account_number": "A01074676",
    "bank_name": "TD Bank",
    "bank_balance": "5000",
    "budget_games_and_entertainment": "200",
    "budget_clothing_and_accessories": "200",
    "budget_eating_out": "500",
    "budget_miscellaneous": "100"
}
"""
Modifiable global variable which is used for registering a test user
for the load_test_data method in the Driver class.
"""


class Driver:
    """
    An object of type Driver is responsible for running the Lab 2 Card
    Simulation program. It presents a list of menu options to the user
    that will let the user add, remove, search, access and print the
    cards in their wallet.

    Acts as the middleman for all the various modules. Responsible for
    the application's flow of control and passing the flow of control
    to the right class based on user input.

    Attributes
    ----------
    user: User
        An object of type User that this application is running for.
    tx_mgr: TransactionManager
        An object of type TransactionManager that records transactions.
    menu_dict: a dict of Menu objects
        A dictionary of String / Menu objects as the key / value pairs.

    Static Methods
    --------------
    setup()
        Initializes the User attribute of this Driver object.
    get_menu_choice()
        Displays the menu choices to the user and prompts the user to
        make a selection.

    Methods
    -------
    __init__()
        The initialization method for the Driver class.
    start()
        Begins the main functionalities of the F.A.M. application.
    """
    def __init__(self):
        """
        Initialize a Driver object. The initialization method calls
        the static setup methods for setting up each object that belongs
        to this instance of the Driver class.
        """
        self.user = None

    @staticmethod
    def load_test_user() -> User:
        """
        Initializes and returns an object representing a test user with
        pre-set hardcoded budgets. This is a helper function to speed
        up development.

        :return: User, an object of type User
        """
        new_user = User.generate_new_user(USER_TEST_DATA)
        return new_user

    def start(self) -> None:
        self.execute_startup_menu()
        self.execute_main_menu()

    def execute_startup_menu(self) -> None:
        """
        Initialize the User attribute of this object. Prompts the user
        for all the details.
        """
        new_user = None
        user_choice = Menu.prompt_startup_menu()

        if user_choice == 1:
            user_data = User.prompt_user_registration()
            new_user = User.generate_new_user(user_data)
        elif user_choice == 2:
            new_user = Driver.load_test_user()
        elif user_choice == 3:
            print("Exiting F.A.M. application...")
            exit(1)

        self.user = new_user

    def execute_main_menu(self) -> None:
        """
        Initialize the User attribute of this object. Prompts the user
        for all the details.
        """
        user_choice = None
        while user_choice != 5:
            user_choice = Menu.prompt_main_menu()
            if user_choice == 1:
                self.view_budgets()
            elif user_choice == 2:
                self.record_transaction()
            elif user_choice == 3:
                self.view_transactions()
            elif user_choice == 4:
                self.view_bank_account_details()
            elif user_choice == 5:
                print("Exiting F.A.M. application...")
                exit(1)

    def view_budgets(self):
        """
        Prompt the user
        """
        Menu.prompt_view_budgets()
        for budget in self.user.budget_manager:
            print(f"{budget}\n")

    def record_transaction(self):
        """
        Prompt the user
        """
        Menu.prompt_record_transaction()
        tx_data = Transaction.prompt_record_tx()
        new_tx = Transaction.generate_new_tx(tx_data)

        # Convert the user budget category int input to the enum
        budget_category_int = new_tx.budget_category
        budget_category = BudgetManager.category_mapping[budget_category_int]

        # Retrieve the budget object using the enum as the key
        budget = self.user.budget_manager.budget_dict[budget_category]

        # Validate the transaction before proceeding
        validated_tx, error_msg = self.validate_transaction_record(new_tx,
                                                                   budget)
        if not validated_tx:
            print("\nUnable to record transaction:")
            print(error_msg)
            print(f"{self.user.account}\n")
            print(budget)
            return

        # User has successfully recorded a transaction
        budget.add_amount_spent(new_tx.tx_amount)
        self.user.account.add_amount_spent(new_tx.tx_amount)
        self.user.tx_manager.add_transaction(new_tx)
        print("\nSuccessfully recorded the following transaction:")
        print(new_tx)
        print("\nTransaction has been recorded under the following budget "
              "category:")
        print(budget)

    def view_transactions(self):
        """
        Prompt the user
        """
        user_choice = Menu.prompt_view_transactions()
        if user_choice == 5:
            print("Returning to main menu...")
            return

        budget_category = BudgetManager.category_mapping[user_choice]
        print(f"\nTransactions in the {budget_category.value} "
              f"category: ")
        for tx in self.user.tx_manager:
            if tx.budget_category == user_choice:
                print(f"\n{tx}")

    def view_bank_account_details(self):
        """
        Prompt the user
        """
        Menu.prompt_view_bank_account_details()
        print("Bank Account Details:")
        print(self.user.account)

        for tx_num, tx_details in \
                self.user.tx_manager.transaction_records.items():
            print(f"\nTransaction #{tx_num}:\n"
                  f"{tx_details}")

        print(f"\nSpending Summary:")
        print(f"  Starting Bank Balance: "
              f"{'{:.2f}'.format(self.user.account.starting_balance)}")
        print(f"  Total Transactions Amount: "
              f"{'{:.2f}'.format(self.user.tx_manager.calc_total_spent())}")
        print(f"  Closing Bank Account Balance: "
              f"{'{:.2f}'.format(self.user.account.current_balance)}")

    def validate_transaction_record(self, new_tx: Transaction,
                                    budget: Budget) -> (bool, str):
        validated_tx = False
        error_msg = ""

        # Perform the various checks
        if self.user.account.locked_status:
            error_msg = error_msg + "  The account has been locked out " \
                                    "completely for exceeding the budgets " \
                                    "in two categories!\n"

        if budget.locked_status:
            error_msg = error_msg + "  The budget category for the " \
                                    "transaction entered is locked!\n"

        if new_tx.tx_amount > budget.calc_current_amount():
            error_msg = error_msg + "  Insufficient budget available for " \
                                    "the category selected!\n"

        if new_tx.tx_amount > self.user.account.current_balance:
            error_msg = error_msg + "  Insufficient bank balance available " \
                                    "to complete the transaction!\n"

        return validated_tx, error_msg


def main():
    """
    Entry point to the F.A.M. application.
    """
    driver = Driver()
    driver.start()


if __name__ == '__main__':
    main()
