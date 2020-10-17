#!/usr/bin/env python3

"""
This module contains the Driver class and serves as the entry point
for the Family Appointed Moderator application.
"""
from menu import Menu
from transaction import Transaction
from budget import BudgetManager, Budget
from user import User
from rich import print


class Driver:
    """
    An object of type Driver is responsible for running the F.A.M.
    application. It presents a list of menu options to the user
    that will let the user interact with the various features of
    the F.A.M. application for moderating their budgets and spendings.

    Acts as the middleman for all the various modules. Responsible for
    the application's flow of control and passing the flow of control
    to the right class based on user input.
    """
    user_test_data = {
        "name": "Edwin Pau",
        "age": "31",
        "user_type": "3",
        "bank_account_number": "A01074676",
        "bank_name": "TD Bank",
        "bank_balance": "5000",
        "budget_games_and_entertainment": "200",
        "budget_clothing_and_accessories": "200",
        "budget_eating_out": "500",
        "budget_miscellaneous": "100"
    }
    """
    Modifiable variable which is used for registering a test user
    for the load_test_data method in the Driver class.
    """

    def __init__(self):
        """
        Initialize a Driver object. The user object that belongs to the
        driver is created when the start method is called.
        """
        self.user = None

    @staticmethod
    def load_test_user() -> User:
        """
        Initializes and returns an object representing a test user with
        pre-set hardcoded settings and budgets. This is a helper
        function designed to speed up development. Uses the global
        variable dictionary USER_TEST_DATA for generating a new user.

        :return: User, an object of type User
        """
        new_user = User.generate_new_user(Driver.user_test_data)
        return new_user

    def start(self) -> None:
        """
        Entry method to start up the F.A.M. application. This method
        starts up the startup menu for registering a user, then proceeds
        to direct the flow of control to the main menu prompts.
        """
        self.execute_startup_menu()
        self.execute_main_menu()

    def execute_startup_menu(self) -> None:
        """
        Prompts the user to choose between creating a new user or
        loading the test user account. Creates a new user based on user
        input. This function sets this Driver's user account to the new
        User that is created.
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
        Prompts the user with the main menu choices. Based on the user
        input, the function will direct the flow of control to the
        appropriate driver method to handle the logic for that function.
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

    def view_budgets(self) -> None:
        """
        Prompts the user with a budget they want to view. The budget
        details for each budget category in the budget manager is then
        printed out to the user.
        """
        Menu.prompt_view_budgets()
        for budget in self.user.budget_manager:
            print(f"{budget}\n")

    def record_transaction(self) -> None:
        """
        Prompts the user with the required input for recording a new
        transaction record. The new transaction is created if it is
        validated by the system checks.

        Notifies the user if the transaction failed or succeeded.
        The system refreshes the state of all the Budget objects in the
        BudgetManager and the Transaction objects in the
        TransactionManager. Finally it issues any notifications or
        warnings to the user.
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
            print("\n[red]Warning:[/red] Unable to record transaction!")
            print(error_msg)
            print(f"{self.user.account}\n")
            print(budget)
            return

        # User has successfully recorded a transaction
        budget.add_amount_spent(new_tx.tx_amount)
        self.user.account.add_amount_spent(new_tx.tx_amount)
        self.user.tx_manager.add_transaction(new_tx)
        self.user.update_lock_status()
        print("\nSuccessfully recorded the following transaction:")
        print(new_tx)
        print("\nTransaction has been recorded under the following budget "
              "category:")
        print(budget)

        self.user.check_and_issue_user_warnings(budget)

    def view_transactions(self) -> None:
        """
        Prompts the user with the option to view transactions for
        an individual budget category. Once a budget category is
        selected, it prints out all the transactions that belong
        in that budget category.
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

    def view_bank_account_details(self) -> None:
        """
        Prints out the user's bank account details, including all the
        transactions conducted, as well as a spending summary.
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
        """
        This method is used to validate if a transaction can be
        successfully recorded for the user, based on his budget and
        account restrictions.

        :param new_tx: a Transaction object.
        :param budget: a Budget object.

        :return: a tuple of (a bool for validation, a str for error msg).
        """
        budget_threshold = self.user.tx_manager.lock_threshold
        validated_tx = True
        error_msg = ""

        # Perform the various checks
        # TODO Can refactor in the future using chain of responsibility
        if self.user.account.locked_status:
            error_msg = error_msg + "  The account has been locked out " \
                                    "completely for exceeding the budgets " \
                                    "in two categories!\n"
            validated_tx = False

        if budget.locked_status:
            error_msg = error_msg + "  The budget category for the " \
                                    "transaction entered is locked!\n"
            validated_tx = False

        if budget_threshold and \
           new_tx.tx_amount > budget.amount_total * budget_threshold:
            error_msg = error_msg + "  Exceeded allowable budget available " \
                                    "for the category selected!\n"
            validated_tx = False

        if new_tx.tx_amount > self.user.account.current_balance:
            error_msg = error_msg + "  Insufficient bank balance available " \
                                    "to complete the transaction!\n"
            validated_tx = False

        return validated_tx, error_msg


def main():
    """
    Entry point to the F.A.M. application.
    """
    driver = Driver()
    driver.start()


if __name__ == '__main__':
    main()
