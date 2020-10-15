"""
This module contains the various classes that represent, store, and
manage users' transactions.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from rich import print


class TransactionManager(ABC):
    """
    An abstract base class that represents a generic TransactionManager.
    Different user types will extend this abstract class to make a
    specific and concrete class of a TransactionManager, such as a
    RebelTransactionManager.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """

    def __init__(self):
        """
        Initializes a TransactionManager object.
        """
        self.transaction_records = {}
        self.current_tx_number = 1

    def __iter__(self):
        """
        Used to allow the Wallet class to be an iterable object.
        :return: a CardIterator object
        """
        return TransactionManagerIterator(self)

    def as_dict(self):
        return self.transaction_records

    def add_transaction(self, new_tx: Transaction):
        """
        Creates a new transaction and adds it to the dictionary that
        contains all the transaction records for this manager to track.
        """
        self.transaction_records[self.current_tx_number] = new_tx
        self.current_tx_number += 1

    def calc_total_spent(self) -> float:
        """
        Creates a new transaction and adds it to the dictionary that
        contains all the transaction records for this manager to track.
        """
        total_spent = 0
        for tx in self:
            total_spent += tx.tx_amount

        return total_spent

    @staticmethod
    def generate_tx_mgr(user_data: dict):
        tx_mgr = None
        if user_data["user_type"] == 1:
            tx_mgr = AngelTransactionManager()
        elif user_data["user_type"] == 2:
            tx_mgr = TroublemakerTransactionManager()
        elif user_data["user_type"] == 3:
            tx_mgr = RebelTransactionManager()

        return tx_mgr

    @abstractmethod
    def issue_warning(self, budget_str: str):
        pass

    @abstractmethod
    def issue_notification(self, budget_str: str):
        pass


class TransactionManagerIterator:
    """
    Iterator that iterates over all the users' cards in the wallet.
    __init__(wallet: Wallet)
        The initialization method for the CardIterator class.
    """
    def __init__(self, tx_mgr: TransactionManager):
        """"
        Initializes a CardIterator object that is used to iterate
        over the Wallet class's dictionary of Card objects.
        :param
        """
        self.tx_dict = tx_mgr.transaction_records
        self.curr_index = 0

    def __next__(self) -> str:
        """"
        Responsible for returning the next element from the iterable
        Wallet object.
        :return: a str representing the details of the Card object
        """
        tx_keys_list = list(self.tx_dict.keys())
        if self.curr_index == len(tx_keys_list) or \
                len(tx_keys_list) == 0:
            raise StopIteration()

        next_tx = self.tx_dict.get(tx_keys_list[self.curr_index])
        self.curr_index += 1

        return next_tx

    def __iter__(self):
        """"
        Returns an object of CardIterator for the Wallet object to use,
        allowing it to iterate through the dictionary of cards.
        :return: an object of type CardIterator
        """
        return self


class Transaction:
    """
    An object of type Transaction. This class represents one transaction
    by the user. It contains details about the transaction, such as
    the date/time the transaction took place, the user that initiated
    the transaction, the merchant name, dollar amount, and the budget
    category that the transaction belongs to.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the Transaction class.
    """

    transaction_fields = {
        "year": "Transaction Year: ",
        "month": "Transaction Month: ",
        "day": "Transaction Day: ",
        "tx_amount": "Transaction Amount: ",
        "budget_category": "Budget Category (1-4):\n"
                           "  1. Games and Entertainment\n"
                           "  2. Clothing and Accessories\n"
                           "  3. Eating Out\n"
                           "  4. Miscellaneous\n",
        "merchant_name": "Merchant Name: "
    }

    def __init__(self, timestamp: datetime, tx_amount: float,
                 budget_category: int, merchant_name: str):
        """
        Initializes a Transaction object.
        """
        self.timestamp = timestamp
        self.tx_amount = tx_amount
        self.budget_category = budget_category
        self.merchant_name = merchant_name

    def __str__(self):
        formatted_str = f"  Timestamp: {self.timestamp}\n" \
                        f"  Amount: " \
                        f"{'{:.2f}'.format(self.tx_amount)}\n"\
                        f"  Merchant Name: {self.merchant_name}"
        return formatted_str

    @classmethod
    def prompt_record_tx(cls) -> dict:
        """
        On application startup, the user must register their child's
        financial details. Displays and prompts the user to enter
        all the required information for registering a user.

        :return: a dict with the user registration data
        """
        tx_data = {}

        for key, value in Transaction.transaction_fields.items():
            input_valid = False
            while not input_valid:
                data = input(f"Enter the {value}")

                if key == "tx_amount" and float(data) < 0:
                    print("[red]Please ensure the transaction amount is "
                          "greater than or equal to zero and try again.[/red]")
                    input_valid = False
                else:
                    input_valid = True
                    tx_data[key] = data
        return tx_data

    @classmethod
    def _convert_tx_data_types(cls, tx_data: dict) -> dict:
        """
        On application startup, the user must register their child's
        financial details. Displays and prompts the user to enter
        all the required information for registering a user.

        :return: a dict with the user registration data
        """
        converted_tx_data = tx_data
        timestamp = datetime(int(tx_data["year"]),
                             int(tx_data["month"]),
                             int(tx_data["day"]))
        converted_tx_data["timestamp"] = timestamp
        converted_tx_data["tx_amount"] = float(tx_data["tx_amount"])

        converted_tx_data["budget_category"] = int(tx_data["budget_category"])

        return converted_tx_data

    @staticmethod
    def generate_new_tx(tx_data: dict) -> Transaction:
        """
        Initialize the User attribute of this object. Prompts the user
        for all the details.

        :return: User, an object of type User.
        """
        tx_data = Transaction._convert_tx_data_types(tx_data)

        new_tx = Transaction(tx_data["timestamp"],
                             tx_data["tx_amount"],
                             tx_data["budget_category"],
                             tx_data["merchant_name"])

        return new_tx


class AngelTransactionManager(TransactionManager):
    """

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """
    def __init__(self):
        """
        Initializes an AngelTransactionManager object.
        """
        super().__init__()
        self.lock_threshold = None
        self.warning_threshold = 0.9
        self.max_locked_budgets = None
        self.persistent_warning = False

    def issue_warning(self, budget_str: str):
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str):
        print(f"\n[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")


class TroublemakerTransactionManager(TransactionManager):
    """

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """
    def __init__(self):
        """
        Initializes an AngelTransactionManager object.
        """
        super().__init__()
        self.lock_threshold = 1.2
        self.warning_threshold = 0.75
        self.max_locked_budgets = None
        self.persistent_warning = False

    def issue_warning(self, budget_str: str):
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str):
        print(f"\n[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")


class RebelTransactionManager(TransactionManager):
    """

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """
    def __init__(self):
        """
        Initializes an AngelTransactionManager object.
        """
        super().__init__()
        self.lock_threshold = 1
        self.warning_threshold = 0.5
        self.max_locked_budgets = 2
        self.persistent_warning = True

    def issue_warning(self, budget_str: str):
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str):
        print("\n" + "[red]@[/red]" * 80)
        print(f"[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")
        print("[red]@[/red]" * 80)
