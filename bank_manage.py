import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password
        )
        self.cursor = self.connection.cursor()

    def initialize_database(self, db_name):
        self.connect()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.connection.database = db_name
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                balance FLOAT DEFAULT 0
            )
        """)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


class BankManagementSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_account(self, name, initial_balance=0):
        query = "INSERT INTO accounts (name, balance) VALUES (%s, %s)"
        self.db_manager.cursor.execute(query, (name, initial_balance))
        self.db_manager.connection.commit()
        print("Account created successfully!")

    def view_accounts(self):
        self.db_manager.cursor.execute("SELECT * FROM accounts")
        accounts = self.db_manager.cursor.fetchall()
        print("\nList of Accounts:")
        for account in accounts:
            print(f"ID: {account[0]}, Name: {account[1]}, Balance: {account[2]}")
        print()

    def deposit(self, account_id, amount):
        query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
        self.db_manager.cursor.execute(query, (amount, account_id))
        self.db_manager.connection.commit()
        print(f"Deposited {amount} successfully!")

    def withdraw(self, account_id, amount):
        query = "SELECT balance FROM accounts WHERE account_id = %s"
        self.db_manager.cursor.execute(query, (account_id,))
        balance = self.db_manager.cursor.fetchone()[0]
        if balance >= amount:
            query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            self.db_manager.cursor.execute(query, (amount, account_id))
            self.db_manager.connection.commit()
            print(f"Withdrew {amount} successfully!")
        else:
            print("Insufficient balance!")

    def menu(self):
        while True:
            print("\n--- Bank Management System ---")
            print("1. Add Account")
            print("2. View Accounts")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter account holder name: ")
                balance = float(input("Enter initial balance: "))
                self.add_account(name, balance)
            elif choice == 2:
                self.view_accounts()
            elif choice == 3:
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter amount to deposit: "))
                self.deposit(account_id, amount)
            elif choice == 4:
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter amount to withdraw: "))
                self.withdraw(account_id, amount)
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    # Configure database credentials
    HOST = "localhost"
    USER = "root"
    PASSWORD = "######"
    DB_NAME = "bank_system"

    db_manager = DatabaseManager(HOST, USER, PASSWORD)
    db_manager.initialize_database(DB_NAME)

    bank_system = BankManagementSystem(db_manager)
    bank_system.menu()

    db_manager.close()

