"""
This module contains the Account classes that contains the various
data regarding the user's account, such as a bank account.
"""

from abc import ABC, abstractmethod


class Account(ABC):
    """
    This is an abstract class that refers to a generic account type. It
    contains the interfaces that a concrete account class must
    implement.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    """

    def __init__(self, account_number: str, locked_status=False):
        """
        Initialization method for the UserType object.
        """
        self.account_number = account_number
        self.locked_status = locked_status

    @abstractmethod
    def __str__(self):
        pass


class BankAccount(Account):
    """
    An object of type BankAccount.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    """

    def __init__(self, account_number: str, bank_name: str,
                 starting_balance: float):
        """
        Initializes a BankAccount object.
        """
        super().__init__(account_number)
        self.bank_name = bank_name
        self.starting_balance = starting_balance
        self.current_balance = starting_balance

    @staticmethod
    def generate_bank_account(user_data: dict):
        bank_account = BankAccount(user_data["bank_account_number"],
                                   user_data["bank_name"],
                                   user_data["bank_balance"])

        return bank_account

    def add_amount_spent(self, amount_spent: float):
        """
        Initializes a BudgetCategory object.
        """
        self.current_balance -= amount_spent

    def __str__(self):
        formatted_str = f"  Account Number: {self.account_number}\n"\
                        f"  Bank Name: {self.bank_name}\n"\
                        f"  Starting Balance: " \
                        f"{'{:.2f}'.format(self.starting_balance)}\n"\
                        f"  Current Balance: " \
                        f"{'{:.2f}'.format(self.current_balance)}\n"\
                        f"  Account Locked: {self.locked_status}"
        return formatted_str
