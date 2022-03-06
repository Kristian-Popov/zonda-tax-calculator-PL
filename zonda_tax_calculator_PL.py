"""
Parse transaction logs from Zonda exchange (CSV format) and calculate values needed for PIT-38.
"""

import csv
import argparse
import locale

from decimal import *

INCOME_TYPE='Otrzymanie środków z transakcji na rachunek'
EXPENSE_TYPE='Pobranie środków z transakcji z rachunku'
CURRENCY='PLN'

def zonda_calculate_tax():
    decimal_context = getcontext()
    decimal_context.traps[FloatOperation] = True

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, action='append', required=True)
    args = parser.parse_args()

    income = Decimal()
    expense = Decimal()
    for csv_file_name in args.csv:
        with open(csv_file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            # Skip first line
            next(reader)

            for row in reader:
                transaction_type = str(row[1])
                # TODO better way to handle comma
                transaction_amount = Decimal(row[2].replace(",", "."))
                transaction_currency = str(row[3])

                if transaction_type.startswith(INCOME_TYPE) and transaction_currency == CURRENCY:
                    assert(transaction_amount > 0)
                    print(f"Found income with amount {transaction_amount}")
                    income = income + transaction_amount
                elif transaction_type.startswith(EXPENSE_TYPE) and transaction_currency == CURRENCY:
                    assert(transaction_amount < 0)
                    print(f"Found expense with amount {transaction_amount}")
                    expense = expense + transaction_amount

    print(f"Income/przychód: { income }")
    print(f"Koszt/expense: { expense }")

zonda_calculate_tax()
