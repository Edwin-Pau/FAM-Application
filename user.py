"""
This module contains the User class that contains the various user data,
such as the user's name, age, budget, account, and user type.
"""
from __future__ import annotations

from account import Account, BankAccount
from budget import BudgetManager, Budget
from transaction import TransactionManager


class User:
    """
    An object of type User.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    """

    user_registration_fields = {
        "name": "Name: ",
        "age": "Age: ",
        "user_type": "Type of User (1-3):\n"
                     "  1. The Angel\n"
                     "  2. The Troublemaker\n"
                     "  3. The Rebel\n",
        "bank_account_number": "Bank Account Number: ",
        "bank_name": "Name of the Bank: ",
        "bank_balance": "Current Bank Balance: ",
        "budget_games_and_entertainment": "Budget for Games and "
                                          "Entertainment: ",
        "budget_clothing_and_accessories": "Budget for Clothing and "
                                           "Accessories: ",
        "budget_eating_out": "Budget for Eating Out: ",
        "budget_miscellaneous": "Budget for Miscellaneous Items: "
    }
    """
    A dictionary that maps required user registration input attributes 
    to their string representations, which is used for prompting the 
    user during application startup.
    """

    def __init__(self, name: str, age: int, tx_manager: TransactionManager,
                 account: Account, budget_manager: BudgetManager):
        """
        Initializes a User object.
        """
        self.name = name
        self.age = age
        self.tx_manager = tx_manager
        self.account = account
        self.budget_manager = budget_manager

    def __str__(self) -> str:
        """
        Initializes a User object.
        """
        formatted_str = f"\nName: {self.name}"\
                        f"\nAge: {self.age}"\
                        f"\nAccount: {self.account}" \
                        f"\nTx Manager: {self.tx_manager}" \
                        f"\nBudget Manager: {self.budget_manager}"
        return formatted_str

    @classmethod
    def prompt_user_registration(cls) -> dict:
        """
        On application startup, the user must register their child's
        financial details. Displays and prompts the user to enter
        all the required information for registering a user.

        :return: a dict with the user registration data
        """
        user_data = {}
        for key, value in User.user_registration_fields.items():
            data = input(f"Enter the {value}")
            user_data[key] = data

        return user_data

    @classmethod
    def _convert_user_data_types(cls, user_data: dict) -> dict:
        """
        On application startup, the user must register their child's
        financial details. Displays and prompts the user to enter
        all the required information for registering a user.

        :return: a dict with the user registration data
        """
        converted_user_data = user_data

        converted_user_data["age"] = int(user_data["age"])
        converted_user_data["user_type"] = int(user_data["user_type"])
        converted_user_data["bank_balance"] = float(user_data["bank_balance"])
        converted_user_data["budget_games_and_entertainment"] \
            = float(user_data["budget_games_and_entertainment"])
        converted_user_data["budget_clothing_and_accessories"] \
            = float(user_data["budget_clothing_and_accessories"])
        converted_user_data["budget_eating_out"] \
            = float(user_data["budget_eating_out"])
        converted_user_data["budget_miscellaneous"] \
            = float(user_data["budget_miscellaneous"])

        return converted_user_data

    @staticmethod
    def generate_new_user(user_data: dict) -> User:
        """
        Initialize the User attribute of this object. Prompts the user
        for all the details.

        :return: User, an object of type User.
        """
        user_data = User._convert_user_data_types(user_data)
        name = user_data["name"]
        age = int(user_data["age"])
        tx_mgr = TransactionManager.generate_tx_mgr(user_data)
        bank_account = BankAccount.generate_bank_account(user_data)
        budget_mgr = BudgetManager.generate_budget_mgr(user_data)
        new_user = User(name, age, tx_mgr, bank_account, budget_mgr)

        return new_user

    def update_lock_status(self):
        lock_threshold = self.tx_manager.lock_threshold
        num_categories_locked = 0
        for budget in self.budget_manager:

            budget_threshold = budget.amount_spent / budget.amount_total
            if lock_threshold and budget_threshold > lock_threshold:
                budget.lock_budget()

            if budget.locked_status:
                num_categories_locked += 1

        self._update_account_lock_status(num_categories_locked)

    def _update_account_lock_status(self, num_categories_locked: int):
        max_locked_budgets = self.tx_manager.max_locked_budgets
        if max_locked_budgets and num_categories_locked >= max_locked_budgets:
            self.account.locked_status = True
            self.account.issue_locked_warning()

    def check_and_issue_user_warnings(self, current_budget: Budget):
        warning_threshold = self.tx_manager.warning_threshold
        persistent_warning = self.tx_manager.persistent_warning
        budget_category_str = current_budget.budget_category.value
        issue_warning = False
        issue_notification = False

        if persistent_warning:
            for budget in self.budget_manager:
                budget_threshold = budget.amount_spent / budget.amount_total

                if budget_threshold > warning_threshold:
                    issue_warning = True

        if current_budget.locked_status:
            issue_warning = True

        if current_budget.amount_spent / current_budget.amount_total > 1:
            issue_notification = True

        if issue_warning:
            self.tx_manager.issue_warning(budget_category_str)

        if issue_notification:
            self.tx_manager.issue_notification(budget_category_str)
