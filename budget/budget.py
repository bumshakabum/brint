#!/usr/bin/env python

import sqlite3
import readline

# User interface to take in data
# 1/2 method to enter spending
# Method to limit spending in certain categories 'Set budgets'

# Might be better to split the db into 2 tables
### 1 for income 1 for expenditure

# Infinite loop until user says quit
def main():
    conn = sqlite3.connect('example.db')
    with conn:
        mk_table(conn)
        while True:
            print_menu()
            choice = input("What would you like to do? ")
            choice = choice.lower()
            if choice == 'e':
                spent(conn)
            elif choice == 'o':
                overview(conn)
            elif choice == 'ba':
                balance(conn)
            elif choice == 'q':
                return False

def mk_table(conn):
    # Create table in database if it doesn't exist
    cur = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS finances
    (Id INTEGER PRIMARY KEY, Date TEXT, Category TEXT, Description TEXT, Amount REAL)'''
    cur.execute(query)
    conn.commit

def print_menu():
    # TODO: First time user should have an option to input initial capital
    # TODO: Option to clear the database
    # TODO: Option to delete entries
    # TODO: Option to modify entries
    ### SUBTODO: Need a way to organize id so user can pick id to modify
    print()
    print("make an [E]ntry")
    print("[O]verview of spending")
    print("set a [B]udget")
    print("check [BA]lance")
    print("[Q]uit")
    print()

def spent(conn):


    amount = input("Amount([-]/+): ")
    description = input("Description: ")

    # display existing categories
    unique_query(conn, 'category')
    category = input("Category: ")

    # Figure out expenditure and income (-/+)
    if '-' not in amount and '+' not in amount:
        amount = '-' + amount
    amount = float(amount)

    # put into database
    entry(conn, (category, description, amount))

    # TODO: Check against budget for specified category
    budget_check(conn)

def budget_check(conn):
    """ check if user is within budget """
    pass

def unique_query(conn, column):
    """ Print unique values of specified column """

    cur = conn.cursor()
    query = "SELECT DISTINCT {0} FROM finances".format(column)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(' ', row[0])

def entry(conn, col_vals):
    cur = conn.cursor()
    query = "INSERT INTO finances VALUES(NULL, date(), ?, ?, ?)"
    cur.execute(query, col_vals)

    conn.commit()

def capital(conn):
    # set initial capital
    # Insert as a regular entry under capital category
    query = "INSERT INTO"
    pass

def balance(conn):
    """ returns the balance of the account """
    cur = conn.cursor()
    query = "SELECT SUM(amount) FROM finances"
    cur.execute(query)
    bal = cur.fetchall()[0][0]
    bal = "{:.2f}".format(bal)
    print()
    print("Balance:", bal)

def budget():
    # TODO: Set monthly threshold warning?
    # TODO: Set weekly ""
    # TODO: Set budget for category
    pass

def query(conn, columns):
    cur = conn.cursor()
    query = "SELECT {0}, {1}, {2}, {3} FROM finances".format(*columns)
    cur.execute(query)
    return cur.fetchall()

def overview(conn):
    """ Display overview of finances """

    print()
    print("OVERVIEW")
    print()


    rows = query(conn, ('id','date','category','description','amount'))

    cat_longest = longest_string_len(conn, 'category')
    desc_longest = longest_string_len(conn, 'description')
    # TODO: Headings
    date_len = longest_string_len(conn, 'date')
    amount_len = longest_string_len(conn, 'amount')
    header = 'Date' + ' ' * (date_len - 2)
    header += 'Category' + ' ' * (cat_longest - 6) + 'Description'
    padding = 80 - len(header) - len('Entry')
    header += ' ' * padding + 'Entry'
    # TODO: If there's no data, formatting is fucked
    print(header)
    print('-' * 80)

    # TODO: if row is bigger than 80, add a newline

    for row in rows:
        date, category, description, amount = row
        amount = "{:.2f}".format(amount)
        # align leftside items between each other
        cat_to_desc = cat_longest - len(category)
        line_out = date + '  ' + category + ' ' * cat_to_desc + '  ' + description
        padding = 80 - (len(amount) + len(line_out))
        line_out += ' ' * padding + amount
        print(line_out)

def header(conn):
    query()

def longest_string_len(conn, column):
    cur = conn.cursor()
    query = '''SELECT {0} FROM finances
    ORDER BY LENGTH({0}) DESC LIMIT 1'''.format(column)
    cur.execute(query)
    if not cur.fetchall():
        return 0
    print(cur.fetchall())
    longest_string = cur.fetchall()[0][0]
    return len(str(longest_string))

if __name__ == '__main__':
    main()
