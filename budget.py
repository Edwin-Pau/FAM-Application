"""
This module contains the various classes that represent the various
budget categories available to a user.
"""
from __future__ import annotations
from enum import Enum


class BudgetCategory(Enum):
    """
    This is an enum that contains the various budget categories.
    """
    GAMES_AND_ENTERTAINMENT = "Games and Entertainment"
    CLOTHING_AND_ACCESSORIES = "Clothing and Accessories"
    EATING_OUT = "Eating Out"
    MISCELLANEOUS = "Miscellaneous"


class BudgetManager:
    """
    An object of type BudgetManager manages a list of budget categories.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """
    category_mapping = {
        1: BudgetCategory.GAMES_AND_ENTERTAINMENT,
        2: BudgetCategory.CLOTHING_AND_ACCESSORIES,
        3: BudgetCategory.EATING_OUT,
        4: BudgetCategory.MISCELLANEOUS
    }
    """
    A dictionary that maps required user registration input attributes 
    to their string representations, which is used for prompting the 
    user during application startup.
    """

    def __init__(self, budget_dict: dict):
        """
        Initializes a TransactionManager object.
        """
        self.budget_dict = budget_dict

    def __iter__(self):
        """
        Used to allow the Wallet class to be an iterable object.
        :return: a CardIterator object
        """
        return BudgetManagerIterator(self)

    @staticmethod
    def generate_budget_mgr(user_data: dict):
        budget_dict = {}
        budget_games_and_entertainment = Budget(
            BudgetCategory.GAMES_AND_ENTERTAINMENT,
            user_data["budget_games_and_entertainment"]
        )
        budget_clothing_and_accessories = Budget(
            BudgetCategory.CLOTHING_AND_ACCESSORIES,
            user_data["budget_clothing_and_accessories"]
        )
        budget_eating_out = Budget(
            BudgetCategory.EATING_OUT,
            user_data["budget_eating_out"]
        )
        budget_miscellaneous = Budget(
            BudgetCategory.MISCELLANEOUS,
            user_data["budget_miscellaneous"]
        )
        budget_dict[BudgetCategory.GAMES_AND_ENTERTAINMENT] \
            = budget_games_and_entertainment
        budget_dict[BudgetCategory.CLOTHING_AND_ACCESSORIES] \
            = budget_clothing_and_accessories
        budget_dict[BudgetCategory.EATING_OUT] \
            = budget_eating_out
        budget_dict[BudgetCategory.MISCELLANEOUS] \
            = budget_miscellaneous
        budget_mgr = BudgetManager(budget_dict)

        return budget_mgr


class BudgetManagerIterator:
    """
    Iterator that iterates over all the users' cards in the wallet.
    __init__(wallet: Wallet)
        The initialization method for the CardIterator class.
    """
    def __init__(self, budget_mgr: BudgetManager):
        """"
        Initializes a CardIterator object that is used to iterate
        over the Wallet class's dictionary of Card objects.
        :param wallet: an object of type Wallet
        """
        self.budget_dict = budget_mgr.budget_dict
        self.curr_index = 0

    def __next__(self) -> str:
        """"
        Responsible for returning the next element from the iterable
        Wallet object.
        :return: a str representing the details of the Card object
        """
        budgets_keys_list = list(self.budget_dict.keys())
        if self.curr_index == len(budgets_keys_list) or \
                len(budgets_keys_list) == 0:
            raise StopIteration()

        next_budget = self.budget_dict.get(budgets_keys_list[self.curr_index])
        self.curr_index += 1

        return next_budget

    def __iter__(self):
        """"
        Returns an object of CardIterator for the Wallet object to use,
        allowing it to iterate through the dictionary of cards.
        :return: an object of type CardIterator
        """
        return self


class Budget:
    """
    An object of type BudgetManager manages a list of budget categories.

    Attributes
    ----------

    Static Methods
    --------------

    Methods
    -------
    __init__()
        The initialization method for the TransactionManager class.
    """
    def __init__(self, budget_category: BudgetCategory, amount_total: float):
        """
        Initializes a BudgetCategory object.
        """
        self.budget_category = budget_category
        self.amount_total = amount_total
        self.amount_spent = 0
        self.locked_status = False

    def __str__(self) -> str:
        """
        Initializes a BudgetCategory object.
        """
        formatted_str = f"  Category: {self.budget_category.value}\n"\
                        f"  Amount Total: " \
                        f"{'{:.2f}'.format(self.amount_total)}\n"\
                        f"  Amount Spent: " \
                        f"{'{:.2f}'.format(self.amount_spent)}\n"\
                        f"  Amount Available: " \
                        f"{'{:.2f}'.format(self.calc_current_amount())}\n"\
                        f"  Budget Locked: {self.locked_status}"
        return formatted_str

    def calc_current_amount(self):
        """
        Initializes a BudgetCategory object.
        """
        return self.amount_total - self.amount_spent

    def lock_budget(self):
        """
        Initializes a BudgetCategory object.
        """
        self.locked_status = True

    def add_amount_spent(self, amount_spent: float):
        """
        Initializes a BudgetCategory object.
        """
        self.amount_spent += amount_spent
