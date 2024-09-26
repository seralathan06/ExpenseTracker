import click
import csv
import os
from datetime import datetime

# Constants
CSV_FILE = 'expenses.csv'
FIELDNAMES = ['ID', 'Date', 'Description', 'Amount', 'Category']

# Initialize CSV if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

# Generate the next ID for a new expense
def get_next_id():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if rows:
            return int(rows[-1]['ID']) + 1
        return 1

# Add an expense
@click.command()
@click.option('--description', prompt='Expense description', help='Description of the expense')
@click.option('--amount', prompt='Expense amount', type=float, help='Amount of the expense')
@click.option('--category', default='General', help='Category of the expense')
def add(description, amount, category):
    initialize_csv()
    expense_id = get_next_id()
    date = datetime.now().strftime('%Y-%m-%d')

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({'ID': expense_id, 'Date': date, 'Description': description, 'Amount': amount, 'Category': category})

    click.echo(f'Expense added successfully (ID: {expense_id})')

# List all expenses
@click.command()
def list_expenses():
    initialize_csv()
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        click.echo(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount':<10} {'Category':<10}")
        click.echo('-' * 60)
        for row in reader:
            click.echo(f"{row['ID']:<5} {row['Date']:<12} {row['Description']:<20} {row['Amount']:<10} {row['Category']:<10}")

# Delete an expense
@click.command()
@click.option('--id', prompt='Expense ID', type=int, help='ID of the expense to delete')
def delete(id):
    initialize_csv()
    expenses = []
    expense_found = False

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ID']) != id:
                expenses.append(row)
            else:
                expense_found = True

    if not expense_found:
        click.echo(f'Expense with ID {id} not found.')
        return

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)

    click.echo(f'Expense deleted successfully (ID: {id})')

# Show total expenses
@click.command()
@click.option('--month', type=int, default=None, help='Filter by month (1-12)')
def summary(month):
    initialize_csv()
    total_expense = 0
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expense_date = datetime.strptime(row['Date'], '%Y-%m-%d')
            if month is None or expense_date.month == month:
                total_expense += float(row['Amount'])

    if month:
        click.echo(f'Total expenses for month {month}: ${total_expense}')
    else:
        click.echo(f'Total expenses: ${total_expense}')

# Main command group
@click.group()
def expense_tracker():
    pass

expense_tracker.add_command(add)
expense_tracker.add_command(list_expenses, name='list')
expense_tracker.add_command(delete)
expense_tracker.add_command(summary)

if __name__ == '__main__':
    expense_tracker()
