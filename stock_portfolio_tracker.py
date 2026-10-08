"""
CodeAlpha Python Internship - Task 2: Stock Portfolio Tracker
==============================================================

A simple console program that calculates the total value of your
stock investments.

How it works:
    1. Stock prices are stored in a hardcoded dictionary (STOCK_PRICES).
    2. The user types a stock name and a quantity, as many times as they want.
    3. The program shows each holding and the total investment value.
    4. Optionally, the result is saved to a .txt or .csv file.

Key concepts used: dictionary, input/output, basic arithmetic,
                   file handling (optional), loops, functions.
"""

import csv
from datetime import datetime

# ---------------------------------------------------------------------------
# Hardcoded stock prices (price of ONE share, in US dollars).
# You can add more stocks here if you like.
# ---------------------------------------------------------------------------
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 330,
    "AMZN": 130,
}


def show_available_stocks():
    """Print every stock the program knows about, with its price."""
    print("\nAvailable stocks:")
    print("-" * 24)
    for name, price in STOCK_PRICES.items():
        print(f"  {name:<6} ${price}")
    print("-" * 24)


def get_quantity(stock_name):
    """
    Ask the user for a quantity until a valid whole number (1 or more)
    is entered, then return it.
    """
    while True:
        text = input(f"Enter quantity of {stock_name}: ").strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Invalid quantity. Please enter a whole number like 5.")


def collect_portfolio():
    """
    Repeatedly ask the user for stock names and quantities.
    Returns a dictionary like {"AAPL": 10, "TSLA": 5}.
    """
    portfolio = {}
    print("\nType a stock name to add it to your portfolio.")
    print("Type 'done' when you have finished.")

    while True:
        name = input("\nStock name (or 'done'): ").strip().upper()

        if name == "DONE":
            break
        if name not in STOCK_PRICES:
            print(f"  '{name}' is not in the price list. Please try again.")
            continue

        quantity = get_quantity(name)
        # If the same stock is entered twice, add the quantities together.
        portfolio[name] = portfolio.get(name, 0) + quantity
        print(f"  Added {quantity} x {name}.")

    return portfolio


def calculate_total(portfolio):
    """Return the total investment value of the portfolio."""
    total = 0
    for name, quantity in portfolio.items():
        total += STOCK_PRICES[name] * quantity
    return total


def build_report(portfolio, total):
    """Create the summary text so we can print it and also save it."""
    lines = []
    lines.append("=" * 44)
    lines.append("        STOCK PORTFOLIO SUMMARY")
    lines.append("=" * 44)
    lines.append(f"{'Stock':<8}{'Qty':>6}{'Price':>10}{'Value':>14}")
    lines.append("-" * 44)
    for name, quantity in portfolio.items():
        price = STOCK_PRICES[name]
        value = price * quantity
        lines.append(f"{name:<8}{quantity:>6}{'$' + str(price):>10}{'$' + format(value, ',.2f'):>14}")
    lines.append("-" * 44)
    lines.append(f"{'TOTAL INVESTMENT:':<24}{'$' + format(total, ',.2f'):>20}")
    lines.append("=" * 44)
    return "\n".join(lines)


def save_as_txt(report, filename="portfolio.txt"):
    """Save the report to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report + "\n")
        file.write(f"Saved on: {datetime.now():%Y-%m-%d %H:%M}\n")


def save_as_csv(portfolio, total, filename="portfolio.csv"):
    """Save the portfolio to a CSV file (opens in Excel / Google Sheets)."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        for name, quantity in portfolio.items():
            price = STOCK_PRICES[name]
            writer.writerow([name, quantity, price, price * quantity])
        writer.writerow(["TOTAL", "", "", total])


def ask_to_save(report, portfolio, total):
    """Ask the user whether to save the result, and in which format."""
    choice = input("\nSave result to a file? (txt / csv / no): ").strip().lower()

    if choice == "txt":
        save_as_txt(report)
        print("Saved to portfolio.txt")
    elif choice == "csv":
        save_as_csv(portfolio, total)
        print("Saved to portfolio.csv")
    else:
        print("Result not saved.")


def main():
    """Run the program from start to finish."""
    print("=== Welcome to the Stock Portfolio Tracker ===")
    show_available_stocks()

    portfolio = collect_portfolio()

    if not portfolio:
        print("\nYou did not add any stocks. Goodbye!")
        return

    total = calculate_total(portfolio)
    report = build_report(portfolio, total)
    print("\n" + report)

    ask_to_save(report, portfolio, total)
    print("\nThank you for using the Stock Portfolio Tracker!")


# This line makes sure main() runs only when you run this file directly.
if __name__ == "__main__":
    main()
