"""
This module contains the Menu class that displays and prompts the user
with menu options and returns the user choices back to the driver
module to process the user's requests.
"""
from rich import print


class Menu:
    """
    The menu driver that prints out console messages for
    the F.A.M. application.

    Responsible for querying the user for input and passing the user
    choices back to the driver class to be processed.
    """

    @staticmethod
    def prompt_startup_menu() -> int:
        """
        Starts up the startup menu for registering a new user. Allows
        the user to create a new user and obtains the input or allows
        the user to load a test hardcoded user from the Driver class.

        :return: an int representing the user choice
        """
        print("\n" + "-" * 30)
        print("[bold magenta]Welcome to F.A.M.[/bold magenta]")
        print("-" * 30)
        print("Please select an option to register a user:")
        print("  1. Create a new user")
        print("  2. Load test user")
        print("  3. Exit")

        user_choice = None
        while user_choice != 3:
            try:
                user_choice = int(input("Enter your choice: "))
            except ValueError as e:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            if not 1 <= user_choice <= 3:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            return user_choice

    @staticmethod
    def prompt_main_menu() -> int:
        """
        Starts up the main menu for the F.A.M. application. Allows
        the user to choose from various features and functionalities
        of the program. Output is obtained and returned back to the
        Driver class to be processed.

        :return: an int representing the user choice
        """
        print("\n" + "-" * 30)
        print("[bold magenta]F.A.M. Main Menu[/bold magenta]")
        print("-" * 30)
        print("  1. View Budgets")
        print("  2. Record a Transaction")
        print("  3. View Transactions by Budget")
        print("  4. View Bank Account Details")
        print("  5. Exit")

        user_choice = None
        while user_choice != 5:
            try:
                user_choice = int(input("Enter your choice: "))
            except ValueError as e:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            if not 1 <= user_choice <= 5:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            return user_choice

    @staticmethod
    def prompt_view_budgets() -> None:
        """
        Displays the View Budget header.
        """
        print("\n" + "-" * 30)
        print("[bold magenta]View Budgets[/bold magenta]")
        print("-" * 30)

    @staticmethod
    def prompt_record_transaction() -> None:
        """
        Displays the Record a Transaction header.
        """
        print("\n" + "-" * 30)
        print("[bold magenta]Record a Transaction[/bold magenta]")
        print("-" * 30)

    @staticmethod
    def prompt_view_transactions() -> int:
        """
        Displays the budget selections when viewing all transactions
        of a specific budget.

        :return: an int representing the user choice
        """
        print("\n" + "-" * 30)
        print("[bold magenta]View Transactions by Budget[/bold magenta]")
        print("-" * 30)
        print("  1. Games and Entertainment")
        print("  2. Clothing and Accessories")
        print("  3. Eating Out")
        print("  4. Miscellaneous")
        print("  5. Back")

        user_choice = None
        while user_choice != 5:
            try:
                user_choice = int(input("Enter your choice: "))
            except ValueError as e:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            if not 1 <= user_choice <= 5:
                print("[red]Invalid choice entered. Please enter a valid "
                      "choice.[/red]")
                continue

            return user_choice

    @staticmethod
    def prompt_view_bank_account_details() -> None:
        """
        Displays the View Bank Account details header.
        """
        print("\n" + "-" * 30)
        print("[bold magenta]View Bank Account Details[/bold magenta]")
        print("-" * 30)
