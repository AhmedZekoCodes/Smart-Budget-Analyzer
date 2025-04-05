import csv
from datetime import datetime
import logging
from budget_interfaces import DataSource
from budget_domain import CreditTransaction, DebitTransaction

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CSVDataSource(DataSource):
    def __init__(self, file_path):
        self.file_path = file_path
    
    def fetch_data(self):
        transactions = []
        try:
            with open(self.file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Defensive check: ensure required fields are present.
                    if not all(key in row for key in ['date', 'amount', 'category', 'type']):
                        logger.warning("Skipping row with missing fields: %s", row)
                        continue
                    try:
                        date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
                        amount = float(row['amount'])
                        category = row['category']
                        trans_type = row['type'].strip().lower()
                    except Exception as e:
                        logger.warning("Skipping row due to conversion error: %s; Error: %s", row, e)
                        continue
                    # Defensive: skip transactions with negative amounts.
                    if amount < 0:
                        logger.warning("Skipping row due to negative amount: %s", row)
                        continue
                    if trans_type == 'credit':
                        transaction = CreditTransaction(date_obj, amount, category, row.get('sourceInfo', '').strip())
                    elif trans_type == 'debit':
                        transaction = DebitTransaction(date_obj, amount, category, row.get('destinationInfo', '').strip())
                    else:
                        logger.warning("Skipping row due to invalid type: %s", row)
                        continue
                    transactions.append(transaction)
        except Exception as e:
            logger.error("Error reading CSV file: %s", e)
        logger.info("Fetched %d transactions from %s", len(transactions), self.file_path)
        return transactions
