"""
This module contains the various classes that are related to a
transaction in the F.A.M. application.
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
    """

    def __init__(self):
        """
        Initializes a TransactionManager object that deals with
        Transaction objects. It holds a dictionary object that holds
        Transaction objects.

        The key is the tx number and the value is the Transaction.
        """
        self.persistent_warning = None
        self.warning_threshold = None
        self.max_locked_budgets = None
        self.lock_threshold = None
        self.transaction_records = {}
        self.current_tx_number = 1

    def __iter__(self) -> TransactionManagerIterator:
        """
        Used to allow the TransactionManager class to be an
        iterable object.

        :return: a TransactionManager iterator.
        """
        return TransactionManagerIterator(self)

    def add_transaction(self, new_tx: Transaction) -> None:
        """
        Adds a transaction to be tracked by the TransactionManager.
        The Transaction index number is incremented by 1 everytime
        to have a unique transaction number.

        :param new_tx: a Transaction object
        """
        self.transaction_records[self.current_tx_number] = new_tx
        self.current_tx_number += 1

    def calc_total_spent(self) -> float:
        """
        Calculates an updated total amount spent for all the
        transactions being tracked by this TransactionManager.

        :return: a float
        """
        total_spent = 0
        for tx in self:
            total_spent += tx.tx_amount

        return total_spent

    @staticmethod
    def generate_tx_mgr(user_data: dict) -> TransactionManager:
        """
        Generates a new TransactionManager using the user_data
        dictionary which contains all the user input data for
        building the appropriate child class TransactionManager.

        :return: a TransactionManager class
        """
        tx_mgr = None
        if user_data["user_type"] == 1:
            tx_mgr = AngelTransactionManager()
        elif user_data["user_type"] == 2:
            tx_mgr = TroublemakerTransactionManager()
        elif user_data["user_type"] == 3:
            tx_mgr = RebelTransactionManager()

        return tx_mgr

    @abstractmethod
    def issue_warning(self, budget_str: str) -> None:
        """
        Issues a warning to the user if the warning threshold has been
        exceeded.

        :param budget_str: a str
        """
        pass

    @abstractmethod
    def issue_notification(self, budget_str: str) -> None:
        """
        Issues a notification to the user if the notification
        threshold or conditions have been met.

        :param budget_str: a str
        """
        pass


class TransactionManagerIterator:
    """
    Iterator that iterates over all the Transaction objects in the
    TransactionManager object.
    """
    def __init__(self, tx_mgr: TransactionManager):
        """"
        Initializes a TransactionManagerIterator object that is used to
        iterate over the TransactionManager class's transactions
        dictionary.

        :param tx_mgr: a TransactionManager object.
        """
        self.tx_dict = tx_mgr.transaction_records
        self.curr_index = 0

    def __next__(self) -> Transaction:
        """"
        Responsible for returning the next element from the iterable
        TransactionManager object.

        :return: a Transaction object from the dictionary.
        """
        tx_keys_list = list(self.tx_dict.keys())
        if self.curr_index == len(tx_keys_list) or \
                len(tx_keys_list) == 0:
            raise StopIteration()

        next_tx = self.tx_dict.get(tx_keys_list[self.curr_index])
        self.curr_index += 1

        return next_tx

    def __iter__(self) -> TransactionManagerIterator:
        """"
        Returns an object of TransactionManager iterator for
        TransactionManager to use, allowing it to iterate through the
        dictionary of Transaction objects.

        :return: a TransactionManagerIterator object.
        """
        return self


class Transaction:
    """
    An object of type Transaction. This class represents one transaction
    by the user. It contains details about the transaction, such as
    the date/time the transaction took place, the merchant name,
    dollar amount, and the budget category that the transaction
    belongs to.
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

        :param timestamp: a datetime object
        :param tx_amount: a float for the transaction amount
        :param budget_category: an int representing a budget category
        :param merchant_name: a string representing the merchant name
        """
        self.timestamp = timestamp
        self.tx_amount = tx_amount
        self.budget_category = budget_category
        self.merchant_name = merchant_name

    def __str__(self) -> str:
        """
        A string magic method to return a string representation of the
        Transaction object, which includes all its data and details.

        :return: a str representing the Transaction object.
        """
        formatted_str = f"  Timestamp: {self.timestamp}\n" \
                        f"  Amount: " \
                        f"{'{:.2f}'.format(self.tx_amount)}\n"\
                        f"  Merchant Name: {self.merchant_name}"
        return formatted_str

    @classmethod
    def prompt_record_tx(cls) -> dict:
        """
        The user is prompted with all the required transaction fields
        to record a new transaction. The input from the user is then
        saved to a dictionary to be processed by another class.

        :return: a dict with the transaction record data
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
        This is a helper method that converts the raw data transaction
        dict containing strings from user input into the appropriate
        data types which will be used by the application.

        :param tx_data: a dict with the raw transaction data

        :return: a dict with the converted transaction data
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
        Generates a new Transaction object using the raw user input
        transaction data in the form of a dictionary.

        :param tx_data: a dict with the raw transaction data

        :return: a Transaction object
        """
        tx_data = Transaction._convert_tx_data_types(tx_data)

        new_tx = Transaction(tx_data["timestamp"],
                             tx_data["tx_amount"],
                             tx_data["budget_category"],
                             tx_data["merchant_name"])

        return new_tx


class AngelTransactionManager(TransactionManager):
    """
    Concrete child class of TransactionManager. This class represents
    a user type of an Angel with its states and behaviours as outlined
    by the F.A.M. application specs.
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

    def issue_warning(self, budget_str: str) -> None:
        """
        Issues a warning to the user when they've exceeded the
        warning threshold.

        :param budget_str: a str representing the budget category
        """
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str) -> None:
        """
        Issues a notification to the user when they've exceeded the
        a budget category limit.

        :param budget_str: a str representing the budget category
        """
        print(f"\n[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")


class TroublemakerTransactionManager(TransactionManager):
    """
    Concrete child class of TransactionManager. This class represents
    a user type of a Troublemaker with its states and behaviours as
    outlined by the F.A.M. application specs.
    """
    def __init__(self):
        """
        Initializes an TroublemakerTransactionManager object.
        """
        super().__init__()
        self.lock_threshold = 1.2
        self.warning_threshold = 0.75
        self.max_locked_budgets = None
        self.persistent_warning = False

    def issue_warning(self, budget_str: str):
        """
        Issues a warning to the user when they've exceeded the
        warning threshold.

        :param budget_str: a str representing the budget category
        """
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str):
        """
        Issues a notification to the user when they've exceeded the
        budget limit.

        :param budget_str: a str representing the budget category
        """
        print(f"\n[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")


class RebelTransactionManager(TransactionManager):
    """
    Concrete child class of TransactionManager. This class represents
    a user type of a Rebel with its states and behaviours as
    outlined by the F.A.M. application specs.
    """
    def __init__(self):
        """
        Initializes an RebelTransactionManager object.
        """
        super().__init__()
        self.lock_threshold = 1
        self.warning_threshold = 0.5
        self.max_locked_budgets = 2
        self.persistent_warning = True

    def issue_warning(self, budget_str: str):
        """
        Issues a warning to the user when they've exceeded the
        warning threshold.

        :param budget_str: a str representing the budget category
        """
        print(f"\n[red]Warning:[/red] You have exceeded more than "
              f"{self.warning_threshold * 100}% in the {budget_str} "
              f"budget category!")

    def issue_notification(self, budget_str: str):
        """
        Issues a notification to the user when they've exceeded the
        budget limit.

        :param budget_str: a str representing the budget category
        """
        print("\n" + "[red]@[/red]" * 79)
        print(f"[red]Notification:[/red] Budget category {budget_str} "
              f"exceeded!\n"
              "You should use the main menu to review your budget "
              "allowance in each category.")
        print("[red]@[/red]" * 79)
