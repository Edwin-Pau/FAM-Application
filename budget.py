"""
This module contains the various classes that represent the various
budget categories, and budgets available to a user.
"""
from __future__ import annotations
from enum import Enum
from rich import print


class BudgetCategory(Enum):
    """
    This is an enum that contains the various budget categories and
    their values are string representations of that category.
    """
    GAMES_AND_ENTERTAINMENT = "Games and Entertainment"
    CLOTHING_AND_ACCESSORIES = "Clothing and Accessories"
    EATING_OUT = "Eating Out"
    MISCELLANEOUS = "Miscellaneous"


class BudgetManager:
    """
    An object of type BudgetManager manages a list of Budget objects
    with their budget categories.
    """
    category_mapping = {
        1: BudgetCategory.GAMES_AND_ENTERTAINMENT,
        2: BudgetCategory.CLOTHING_AND_ACCESSORIES,
        3: BudgetCategory.EATING_OUT,
        4: BudgetCategory.MISCELLANEOUS
    }
    """
    A dictionary that maps an int to a BudgetCategory enum. The int
    is used as input from the user, which translates into a budget
    category for this application.
    """

    def __init__(self, budget_dict: dict):
        """
        Initializes a BudgetManager object that deals with budget
        objects. It holds a dictionary object that holds budget objects.

        :param budget_dict: a dict that tracks each budget category.
        The key is the budget enum and the value is the budget object.
        """
        self.budget_dict = budget_dict

    def __iter__(self) -> BudgetManagerIterator:
        """
        Used to allow the BudgetManager class to be an iterable object.

        :return: a BudgetManager iterator.
        """
        return BudgetManagerIterator(self)

    @staticmethod
    def generate_budget_mgr(user_data: dict) -> BudgetManager:
        """
        Generator function to build a new BudgetManager object using
        the provided user data.

        :param user_data: a dict containing the user data, which has
        the budget values for each budget category.

        :return: a BudgetManager object.
        """
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

    @staticmethod
    def issue_locked_status(budget_str: str) -> None:
        """
        Prints out and notifies the user that the budget is locked.

        :param budget_str: a str for the budget category.
        """
        print(f"\n[red]Warning:[/red] Budget category {budget_str} "
              f"is locked!\n")


class BudgetManagerIterator:
    """
    Iterator that iterates over all the budget objects in the
    BudgetManager object.
    """
    def __init__(self, budget_mgr: BudgetManager):
        """"
        Initializes a BudgetManagerIterator object that is used to
        iterate over the BudgetManager class's budgets dictionary.

        :param budget_mgr: a BudgetManager object.
        """
        self.budget_dict = budget_mgr.budget_dict
        self.curr_index = 0

    def __next__(self) -> Budget:
        """"
        Responsible for returning the next element from the iterable
        BudgetManager object.

        :return: a Budget object from the dictionary.
        """
        budgets_keys_list = list(self.budget_dict.keys())
        if self.curr_index == len(budgets_keys_list) or \
                len(budgets_keys_list) == 0:
            raise StopIteration()

        next_budget = self.budget_dict.get(budgets_keys_list[self.curr_index])
        self.curr_index += 1

        return next_budget

    def __iter__(self) -> BudgetManagerIterator:
        """"
        Returns an object of BudgetManager iterator for BudgetManager
        to use, allowing it to iterate through the dictionary of Budget
        objects.

        :return: a BudgetManagerIterator object.
        """
        return self


class Budget:
    """
    An object of type Budget represents a budget category and
    all the data for that budget associated with it.
    """
    def __init__(self, budget_category: BudgetCategory, amount_total: float):
        """
        Initializes a Budget object.

        :param budget_category: a BudgetCategory enum.
        :param amount_total: a float representing the budget total.
        """
        self.budget_category = budget_category
        self.amount_total = amount_total
        self.amount_spent = 0
        self.locked_status = False

    def __str__(self) -> str:
        """
        A string magic method to return a string representation of the
        Budget object, which includes all its data and details.

        :return: a str representing the Budget object.
        """
        formatted_str = f"  Category: {self.budget_category.value}\n"\
                        f"  Budget Total: " \
                        f"{'{:.2f}'.format(self.amount_total)}\n"\
                        f"  Budget Spent: " \
                        f"{'{:.2f}'.format(self.amount_spent)}\n"\
                        f"  Budget Available: " \
                        f"{'{:.2f}'.format(self.calc_current_amount())}\n"\
                        f"  Budget Locked: {self.locked_status}"
        return formatted_str

    def calc_current_amount(self) -> float:
        """
        Calculates the current amount available in the budget. This amount
        is negative is the user goes over the allocated budget amount
        (which is allowed for some user types).

        :return: a float for the new current leftover amount.
        """
        return self.amount_total - self.amount_spent

    def lock_budget(self) -> None:
        """
        Sets the Budget object's locked status to True (locked).
        """
        self.locked_status = True

    def add_amount_spent(self, amount_spent: float) -> None:
        """
        Adds an amount to the amount spent in the budget object.

        :param amount_spent: a float, amount spent in the Budget object
        """
        self.amount_spent += amount_spent
