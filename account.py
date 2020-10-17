"""
This module contains the Account classes that contains the various
data regarding the user's account, such as a bank account.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from rich import print


class Account(ABC):
    """
    This is an abstract class that refers to a generic account type. It
    contains the interface that a concrete account class must
    implement.
    """

    def __init__(self, account_number: str, locked_status=False):
        """
        Initialization method for the Account object.

        :param account_number: a str, representing the account number.
        :param locked_status: a bool, true if locked, false otherwise.
        """
        self.account_number = account_number
        self.locked_status = locked_status

    @abstractmethod
    def __str__(self) -> str:
        """
        A string magic method should be implemented by the concrete
        classes to print a representation of the concrete account
        object.

        :return: a str representing the Account object.
        """
        pass


class BankAccount(Account):
    """
    An object of type BankAccount inherits from the Account base
    abstract class. This is a concrete class that is used by the User
    object and represents the data and details of a user's bank account.
    """

    def __init__(self, account_number: str, bank_name: str,
                 starting_balance: float):
        """
        Initializes a BankAccount object.

        :param account_number: a str, representing the account number.
        :param bank_name: a str, representing the bank name.
        :param starting_balance: a float, representing the starting
                                 bank balance.
        """
        super().__init__(account_number)
        self.bank_name = bank_name
        self.starting_balance = starting_balance
        self.current_balance = starting_balance

    @staticmethod
    def generate_bank_account(user_data: dict) -> BankAccount:
        """
        Generator function that generates a new bank account object.

        :param user_data: a dict with all the required user data.

        :return: a BankAccount object.
        """
        bank_account = BankAccount(user_data["bank_account_number"],
                                   user_data["bank_name"],
                                   user_data["bank_balance"])

        return bank_account

    def add_amount_spent(self, amount_spent: float) -> None:
        """
        Adds an amount spent to the BankAccount object.

        :param amount_spent: a float, representing an amount spent
        """
        self.current_balance -= amount_spent

    @staticmethod
    def issue_locked_warning() -> None:
        """
        Issues a locked warning to the user if the BankAccount is
        locked.
        """
        print("\n[red]Warning:[/red] Your bank account has been completely "
              "locked out for exceeding 2 or more categories!")

    def __str__(self) -> str:
        """
        A string magic method to return a string representation of the
        BankAccount object, which includes all its data and details.

        :return: a str representing the BankAccount object.
        """
        formatted_str = f"  Account Number: {self.account_number}\n"\
                        f"  Bank Name: {self.bank_name}\n"\
                        f"  Starting Balance: " \
                        f"{'{:.2f}'.format(self.starting_balance)}\n"\
                        f"  Current Balance: " \
                        f"{'{:.2f}'.format(self.current_balance)}\n"\
                        f"  Account Locked: {self.locked_status}"

        return formatted_str
