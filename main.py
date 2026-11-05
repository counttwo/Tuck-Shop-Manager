
from datetime import date
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# A dictionary stores all products while the program is running.
# Each product name is the key. Its details are stored in another dictionary.
stock = {}


def load_stock():
    #Read products from stock.txt when the program starts
    try:
        file = open("stock.txt", "r")
        for line in file:
            line = line.strip()

            if line != "":
                details = line.split("|")

                # The file stores: name|price|quantity|minimum level
                name = details[0]
                price = float(details[1])
                quantity = int(details[2])
                minimum = int(details[3])

                stock[name] = {
                    "price": price,
                    "quantity": quantity,
                    "minimum": minimum
                }
        file.close()

    except FileNotFoundError:
        # If the file does not exist, create it with example products.
        print("Stock file was not found. Creating a new one.")
        


def save_stock():
    #Save the current product information to stock.txt
    file = open("stock.txt", "w")

    for name, details in stock.items():
        line = (
            name + "|" +
            str(details["price"]) + "|" +
            str(details["quantity"]) + "|" +
            str(details["minimum"]) + "\n"
        )
        file.write(line)

    file.close()


def show_stock():
    #Display all products and their current quantities
    print("\n--------------- CURRENT STOCK ---------------")

    if len(stock) == 0:
        print("There are no products in the stock list.")
    else:
        for name, details in stock.items():
            print(
                name,
                "| Price: $", format(details["price"], ".2f"),
                "| Quantity:", details["quantity"],
                "| Minimum level:", details["minimum"]
            )

    print("----------------------------------------------")


def add_product():
    #Add a new product to the stock dictionary
    name = input("Enter the product name: ").strip()

    if name == "":
        print("Product name cannot be empty.")
        return

    if name in stock:
        print("That product already exists. Use the restock option instead.")
        return

    try:
        price = float(input("Enter the selling price: $"))
        quantity = int(input("Enter the starting quantity: "))
        minimum = int(input("Enter the minimum stock warning level: "))

        if price <= 0 or quantity < 0 or minimum < 0:
            print("Price must be above zero. Quantity and minimum cannot be negative.")
            return

        stock[name] = {
            "price": price,
            "quantity": quantity,
            "minimum": minimum
        }

        save_stock()
        print("Product added successfully.")

    except ValueError:
        print("Invalid input. Enter numbers for price, quantity and minimum level.")


def restock_product():
    #Increase the quantity of an existing product
    name = input("Enter the product name to restock: ").strip()

    if name not in stock:
        print("Product not found.")
        return

    try:
        amount = int(input("How many units are being added? "))

        if amount <= 0:
            print("The restock amount must be greater than zero.")
            return

        stock[name]["quantity"] = stock[name]["quantity"] + amount
        save_stock()

        print("Stock updated successfully.")
        print("New quantity:", stock[name]["quantity"])

    except ValueError:
        print("Please enter a whole number.")


def record_sale():
    #Record a sale, reduce stock and save the transaction
    show_stock()
    name = input("Enter the product sold: ").strip()

    if name not in stock:
        print("Product not found.")
        return

    try:
        quantity_sold = int(input("Enter the quantity sold: "))

        if quantity_sold <= 0:
            print("Quantity sold must be greater than zero.")
            return

        if quantity_sold > stock[name]["quantity"]:
            print("Not enough stock. Sale was not recorded.")
            return

        price = stock[name]["price"]
        total = price * quantity_sold

        # Reduce the available stock after a successful sale.
        stock[name]["quantity"] = stock[name]["quantity"] - quantity_sold
        save_stock()

        # Save the sale date, product, quantity, unit price and total.
        today = date.today().isoformat()
        file = open("sales.txt", "a")
        file.write(
            today + "|" + name + "|" + str(quantity_sold) + "|" +
            str(price) + "|" + str(total) + "\n"
        )
        file.close()

        print("\nSale recorded successfully.")
        print("Product:", name)
        print("Quantity sold:", quantity_sold)
        print("Total: $", format(total, ".2f"))

        # Warn the user if stock is now at or below the minimum level.
        if stock[name]["quantity"] <= stock[name]["minimum"]:
            print("WARNING: " + name + " is running low on stock!")
            print("Current quantity:", stock[name]["quantity"])

    except ValueError:
        print("Invalid quantity. Please enter a whole number.")


def load_sales():
    #Read sales.txt and return all saved sales as a list
    sales = []

    try:
        file = open("sales.txt", "r")

        for line in file:
            line = line.strip()

            if line != "":
                details = line.split("|")

                sale = {
                    "date": details[0],
                    "name": details[1],
                    "quantity": int(details[2]),
                    "price": float(details[3]),
                    "total": float(details[4])
                }

                sales.append(sale)

        file.close()

    except FileNotFoundError:
        # An empty list is returned if no sales have been recorded yet.
        pass

    return sales


def daily_sales_summary():
    #Show today's total sales and the best-selling product
    sales = load_sales()
    today = date.today().isoformat()

    todays_sales = []
    product_totals = {}

    # Keep only sales made today.
    for sale in sales:
        if sale["date"] == today:
            todays_sales.append(sale)

            name = sale["name"]
            if name in product_totals:
                product_totals[name] = product_totals[name] + sale["quantity"]
            else:
                product_totals[name] = sale["quantity"]

    print("\n------------- DAILY SALES SUMMARY -------------")
    print("Date:", today)

    if len(todays_sales) == 0:
        print("No sales have been recorded today.")
        print("Total sales: $0.00")
        print("Best-selling product: None")
    else:
        total_money = 0

        for sale in todays_sales:
            total_money = total_money + sale["total"]

        best_product = max(product_totals, key=product_totals.get)
        best_quantity = product_totals[best_product]

        print("Number of transactions:", len(todays_sales))
        print("Total money collected: $", format(total_money, ".2f"))
        print("Best-selling product:", best_product)
        print("Units sold:", best_quantity)

    print("------------------------------------------------")


def show_low_stock():
    #Display products whose quantity is at or below the minimum level
    print("\n--------------- LOW STOCK ALERTS ---------------")
    found = False

    for name, details in stock.items():
        if details["quantity"] <= details["minimum"]:
            print(
                name, "- only", details["quantity"],
                "left (minimum level:", details["minimum"], ")"
            )
            found = True

    if found == False:
        print("No products are currently below their minimum stock level.")

    print("------------------------------------------------")


def main():
    #Display the menu and allow the user to choose an action
    load_stock()

    while True:
        print("\n======================================")
        print("       CAMPUS TUCK-SHOP MANAGER")
        print("======================================")
        print("1. View stock")
        print("2. Add a new product")
        print("3. Record a sale")
        print("4. Restock a product")
        print("5. View daily sales summary")
        print("6. View low-stock alerts")
        print("7. Exit")
        print("======================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            show_stock()
        elif choice == "2":
            add_product()
        elif choice == "3":
            record_sale()
        elif choice == "4":
            restock_product()
        elif choice == "5":
            daily_sales_summary()
        elif choice == "6":
            show_low_stock()
        elif choice == "7":
            save_stock()
            print("Stock saved. Thank you for using the program.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


# This starts the program.
main()
