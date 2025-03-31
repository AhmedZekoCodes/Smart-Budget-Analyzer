# budget_domain.py
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Transaction:
    def __init__(self, date, amount, category):
        # Private attributes for encapsulation.
        self._date = date
        self._amount = amount
        self._category = category
    
    def validate(self):
        if self._amount < 0:
            raise ValueError("Amount must be non-negative")
    
    def get_details(self):
        return f"Date: {self._date.strftime('%Y-%m-%d')}, Amount: {self._amount}, Category: {self._category}"
    
    def get_date(self):
        return self._date
    
    def get_amount(self):
        return self._amount
    
    def get_category(self):
        return self._category

class CreditTransaction(Transaction):
    def __init__(self, date, amount, category, source_info):
        super().__init__(date, amount, category)
        self.__source_info = source_info  # Extra encapsulated attribute
    
    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}, Source: {self.__source_info}"

class DebitTransaction(Transaction):
    def __init__(self, date, amount, category, destination_info):
        super().__init__(date, amount, category)
        self.__destination_info = destination_info  # Extra encapsulated attribute
    
    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}, Destination: {self.__destination_info}"

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self._transactions = []
    
    def add_transaction(self, transaction):
        try:
            transaction.validate()
            self._transactions.append(transaction)
            logger.debug("Transaction added: %s", transaction.get_details())
        except Exception as e:
            logger.error("Failed to add transaction: %s", e)
    
    def get_transactions(self):
        return self._transactions

# TransactionFactory using the Factory pattern.
class TransactionFactory:
    @staticmethod
    def create_transaction(trans_type, date, amount, category, extra_info):
        if trans_type.lower() == 'credit':
            return CreditTransaction(date, amount, category, extra_info)
        elif trans_type.lower() == 'debit':
            return DebitTransaction(date, amount, category, extra_info)
        else:
            raise ValueError("Invalid transaction type")

# TransactionManager for advanced sorting and filtering.
class TransactionManager:
    def __init__(self, transactions):
        self.transactions = transactions
    
    def sort_by_date(self, reverse=False):
        sorted_list = sorted(self.transactions, key=lambda t: t.get_date(), reverse=reverse)
        logger.info("Transactions sorted by date.")
        return sorted_list
    
    def filter_by_category(self, category):
        filtered = [t for t in self.transactions if t.get_category().lower() == category.lower()]
        logger.info("Filtered %d transactions for category '%s'.", len(filtered), category)
        return filtered
    
    def total_amount_by_type(self, trans_type):
        if trans_type.lower() == 'credit':
            total = sum(t.get_amount() for t in self.transactions if "Source:" in t.get_details())
        elif trans_type.lower() == 'debit':
            total = sum(t.get_amount() for t in self.transactions if "Destination:" in t.get_details())
        else:
            total = 0
        logger.info("Total %s amount: %f", trans_type, total)
        return total
