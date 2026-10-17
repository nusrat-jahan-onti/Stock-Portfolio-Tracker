"""
CodeAlpha Python Programming Internship - TASK 2: Stock Portfolio Tracker (v3.0)
================================================================================

A menu-driven console program that calculates the total value of your
stock investments, shows each stock's share of the total as a percentage,
and can save the result to a .txt or .csv file.

CodeAlpha Task 2 rules (all followed):
    * User inputs stock names and quantity.
    * Stock prices come from a hardcoded dictionary (STOCK_PRICES).
    * Total investment value is displayed.
    * Result can optionally be saved to a .txt or .csv file.
    * Key concepts used: dictionary, input/output, basic arithmetic,
      file handling.

Extra features (v3.0):
    * 20 stocks in the hardcoded price list (easy to add more)
    * Remove a stock completely OR remove only some of its shares
    * Percentage share of every stock (own menu option + in the report)
    * Coloured, aligned report sorted by value, with a bar chart
    * Safe input checking and an "unsaved changes" warning on exit

Only Python's standard library is used - nothing to install.
"""

import csv
import os
import sys
from datetime import datetime

PROJECT_NAME = "CodeAlpha Python Internship - Task 2: Stock Portfolio Tracker"

# ---------------------------------------------------------------------------
# 1. DATA  -  hardcoded stock prices (price of ONE share, in US dollars)
#    To add a new stock, just add one more  "SYMBOL": price,  line below.
# ---------------------------------------------------------------------------
STOCK_PRICES = {
    "AAPL": 180,    # Apple
    "TSLA": 250,    # Tesla
    "GOOGL": 140,   # Alphabet (Google)
    "MSFT": 330,    # Microsoft
    "AMZN": 130,    # Amazon
    "NFLX": 450,    # Netflix
    "NVDA": 480,    # Nvidia
    "META": 310,    # Meta (Facebook)
    "IBM": 150,     # IBM
    "INTC": 35,     # Intel
    "AMD": 120,     # AMD
    "ORCL": 115,    # Oracle
    "ADBE": 520,    # Adobe
    "CRM": 215,     # Salesforce
    "UBER": 60,     # Uber
    "DIS": 90,      # Disney
    "NKE": 105,     # Nike
    "KO": 60,       # Coca-Cola
    "PEP": 170,     # PepsiCo
    "WMT": 160,     # Walmart
}

REPORT_WIDTH = 68   # width of the report table (number of characters)
BAR_UNIT = 5        # every 5 % of the portfolio = one block in the chart

# ---------------------------------------------------------------------------
# 2. COLOURS  -  small helper so the program looks nice in the terminal
# ---------------------------------------------------------------------------
COLORS = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
}
RESET = "\033[0m"

# Use colours only when printing to a real terminal (not when saving to a file).
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def setup_terminal():
    """Make colours and special characters work on Windows too."""
    if os.name == "nt":
        os.system("")  # turns on ANSI colour support in Windows terminals
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass  # older Python versions: just continue


def paint(text, color, enabled=True):
    """Return `text` wrapped in a colour code (or plain text if colours are off)."""
    if enabled and USE_COLOR:
        return f"{COLORS[color]}{text}{RESET}"
    return text


# ---------------------------------------------------------------------------
# 3. CALCULATION FUNCTIONS  (no input/print here, so they are easy to test)
# ---------------------------------------------------------------------------
def add_to_portfolio(portfolio, name, quantity):
    """Add `quantity` shares of `name`. Adding the same stock twice sums them."""
    portfolio[name] = portfolio.get(name, 0) + quantity


def remove_from_portfolio(portfolio, name, quantity=None):
    """
    Remove shares of `name`.
      quantity=None            -> remove the whole stock
      quantity >= owned shares -> remove the whole stock
      otherwise                -> just lower the quantity
    Returns the number of shares that were removed.
    """
    owned = portfolio[name]
    if quantity is None or quantity >= owned:
        del portfolio[name]
        return owned
    portfolio[name] = owned - quantity
    return quantity


def calculate_value(name, quantity):
    """Value of one holding = price of one share x number of shares."""
    return STOCK_PRICES[name] * quantity


def calculate_total(portfolio):
    """Total investment value of the whole portfolio."""
    total = 0
    for name, quantity in portfolio.items():
        total += calculate_value(name, quantity)
    return total


def calculate_share(value, total):
    """Percentage of the portfolio that one holding makes up."""
    if total == 0:
        return 0.0
    return value / total * 100


def sorted_rows(portfolio):
    """
    List of (name, quantity, price, value) for every stock,
    sorted so the biggest value comes first.
    """
    rows = []
    for name, quantity in portfolio.items():
        rows.append((name, quantity, STOCK_PRICES[name],
                     calculate_value(name, quantity)))
    rows.sort(key=lambda row: row[3], reverse=True)
    return rows


def money(amount):
    """Format a number as money, e.g. 3050 -> $3,050.00"""
    return f"${amount:,.2f}"


# ---------------------------------------------------------------------------
# 4. REPORTS  -  build the text tables (used for screen AND for files)
# ---------------------------------------------------------------------------
def build_report(portfolio, color=False):
    """
    Return the full portfolio summary as one string.
    color=True  -> coloured version for the screen
    color=False -> plain version, safe to save in a file
    """
    total = calculate_total(portfolio)
    rows = sorted_rows(portfolio)
    line_double = "═" * REPORT_WIDTH
    line_single = "─" * REPORT_WIDTH

    lines = []
    lines.append(paint(line_double, "cyan", color))
    lines.append(paint("STOCK PORTFOLIO SUMMARY".center(REPORT_WIDTH), "bold", color))
    lines.append(paint("CodeAlpha Python Internship - Task 2".center(REPORT_WIDTH), "dim", color))
    lines.append(paint(f"Generated: {datetime.now():%Y-%m-%d %H:%M}".center(REPORT_WIDTH), "dim", color))
    lines.append(paint(line_double, "cyan", color))
    header = f"{'Stock':<8}{'Qty':>6}{'Price':>10}{'Value':>14}{'Share':>8}  Chart"
    lines.append(paint(header, "bold", color))
    lines.append(line_single)

    for name, quantity, price, value in rows:
        share = calculate_share(value, total)
        bar = "█" * round(share / BAR_UNIT)
        text = (f"{name:<8}{quantity:>6}{'$' + str(price):>10}"
                f"{money(value):>14}{share:>7.1f}%  ")
        lines.append(text + paint(bar, "green", color))

    lines.append(line_single)
    total_text = f"{'TOTAL INVESTMENT':<30}{money(total):>38}"
    lines.append(paint(total_text, "bold", color))
    lines.append(line_double)

    # A few extra facts about the portfolio.
    if rows:
        biggest = rows[0]
        biggest_share = calculate_share(biggest[3], total)
        total_shares = sum(row[1] for row in rows)
        lines.append(f"Different stocks : {len(rows)}")
        lines.append(f"Total shares     : {total_shares}")
        lines.append(f"Largest holding  : {biggest[0]} ({biggest_share:.1f}% of portfolio)")

    return "\n".join(lines)


def build_percentage_report(portfolio, color=False):
    """
    Return a table that shows ONLY each stock's share of the total (%),
    with a long bar so the difference between stocks is easy to see.
    """
    total = calculate_total(portfolio)
    rows = sorted_rows(portfolio)
    bar_length = 30   # a 100 % share would fill this many blocks

    lines = []
    lines.append(paint("SHARE OF TOTAL PORTFOLIO (%)", "bold", color))
    lines.append("─" * REPORT_WIDTH)
    for name, quantity, price, value in rows:
        share = calculate_share(value, total)
        bar = "█" * max(1, round(share / 100 * bar_length))
        lines.append(f"{name:<7}{share:>6.1f}%  {paint(bar, 'green', color)}")
    lines.append("─" * REPORT_WIDTH)
    lines.append(f"{'TOTAL':<7}{100.0:>6.1f}%  ({money(total)})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. FILE HANDLING  (optional part of the CodeAlpha task)
# ---------------------------------------------------------------------------
def make_filename(user_text, extension):
    """Clean the file name typed by the user and force the right extension."""
    name = os.path.basename(user_text.strip())  # blocks things like ../../x
    root, _ = os.path.splitext(name)
    if not root:
        root = "portfolio"
    return f"{root}.{extension}"


def save_as_txt(portfolio, filename):
    """Save the plain-text report (no colours)."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(build_report(portfolio, color=False) + "\n\n")
        file.write(build_percentage_report(portfolio, color=False) + "\n")


def save_as_csv(portfolio, filename):
    """Save the portfolio as CSV (opens in Excel / Google Sheets)."""
    total = calculate_total(portfolio)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value", "Share %"])
        for name, quantity, price, value in sorted_rows(portfolio):
            writer.writerow([name, quantity, price, value,
                             round(calculate_share(value, total), 2)])
        writer.writerow(["TOTAL", "", "", total, 100 if total else 0])


# ---------------------------------------------------------------------------
# 6. USER INPUT FUNCTIONS  (these use input() and print())
# ---------------------------------------------------------------------------
def show_available_stocks():
    """Print every stock the program knows, with its price (2 columns)."""
    print(paint("\nAvailable stocks", "bold"))
    print("─" * 40)
    names = list(STOCK_PRICES)
    half = (len(names) + 1) // 2
    for i in range(half):
        left = names[i]
        cell = f"  {paint(f'{left:<6}', 'cyan')} {'$' + str(STOCK_PRICES[left]):<8}"
        if i + half < len(names):
            right = names[i + half]
            cell += f"  {paint(f'{right:<6}', 'cyan')} ${STOCK_PRICES[right]}"
        print(cell)
    print("─" * 40)


def ask_quantity(prompt):
    """Ask for a quantity until a whole number (1 or more) is typed."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print(paint("  ✗ Please enter a whole number like 5.", "red"))


def add_stock_flow(portfolio):
    """Menu option 1. Returns True if something was added."""
    show_available_stocks()
    while True:
        name = input("\nStock name (or 'back'): ").strip().upper()
        if name == "BACK":
            return False
        if name not in STOCK_PRICES:
            print(paint(f"  ✗ '{name}' is not in the price list.", "red"))
            continue
        quantity = ask_quantity(f"Quantity of {name}: ")
        add_to_portfolio(portfolio, name, quantity)
        value = calculate_value(name, quantity)
        print(paint(f"  ✓ Added {quantity} x {name} = {money(value)}", "green"))
        return True


def remove_stock_flow(portfolio):
    """Menu option 2. Returns True if something was removed."""
    if not portfolio:
        print(paint("\nYour portfolio is empty - nothing to remove.", "yellow"))
        return False

    print("\nYou own: " + ", ".join(f"{n} ({q})" for n, q in portfolio.items()))
    name = input("Stock to remove (or 'back'): ").strip().upper()
    if name == "BACK":
        return False
    if name not in portfolio:
        print(paint(f"  ✗ You do not own '{name}'.", "red"))
        return False

    owned = portfolio[name]
    answer = input(f"How many shares of {name} to remove? "
                   f"(1-{owned}, or press Enter for all): ").strip()
    if answer == "":
        quantity = None                      # remove everything
    elif answer.isdigit() and int(answer) > 0:
        quantity = int(answer)
    else:
        print(paint("  ✗ Please enter a whole number, or press Enter.", "red"))
        return False

    removed = remove_from_portfolio(portfolio, name, quantity)
    if name in portfolio:
        print(paint(f"  ✓ Removed {removed} x {name}. {portfolio[name]} left.", "green"))
    else:
        print(paint(f"  ✓ Removed all {removed} x {name} from your portfolio.", "green"))
    return True


def view_flow(portfolio):
    """Menu option 3 - full report."""
    if not portfolio:
        print(paint("\nYour portfolio is empty. Add a stock first (option 1).", "yellow"))
        return
    print("\n" + build_report(portfolio, color=True))


def percentage_flow(portfolio):
    """Menu option 4 - share of each stock as a percentage."""
    if not portfolio:
        print(paint("\nYour portfolio is empty. Add a stock first (option 1).", "yellow"))
        return
    print("\n" + build_percentage_report(portfolio, color=True))


def save_flow(portfolio):
    """Menu option 5. Returns True if a file was saved."""
    if not portfolio:
        print(paint("\nNothing to save - your portfolio is empty.", "yellow"))
        return False

    choice = input("\nSave as (txt / csv / back): ").strip().lower()
    if choice not in ("txt", "csv"):
        print("Not saved.")
        return False

    typed = input(f"File name (press Enter for 'portfolio.{choice}'): ")
    filename = make_filename(typed, choice)

    try:
        if choice == "txt":
            save_as_txt(portfolio, filename)
        else:
            save_as_csv(portfolio, filename)
    except OSError as error:
        print(paint(f"  ✗ Could not save the file: {error}", "red"))
        return False

    print(paint(f"  ✓ Saved to {filename}", "green"))
    return True


def print_menu():
    """Show the main menu."""
    print(paint("\n──────── MAIN MENU ────────", "cyan"))
    print("  1. Add a stock")
    print("  2. Remove a stock")
    print("  3. View portfolio & total")
    print("  4. Show share % of each stock")
    print("  5. Save to file (.txt / .csv)")
    print("  6. Exit")


# ---------------------------------------------------------------------------
# 7. MAIN PROGRAM
# ---------------------------------------------------------------------------
def main():
    """Run the program until the user chooses Exit."""
    setup_terminal()
    portfolio = {}      # {"AAPL": 10, "TSLA": 5}
    unsaved = False     # True when there are changes not yet saved to a file

    print(paint("\n📈  STOCK PORTFOLIO TRACKER  📈", "bold"))
    print(paint("CodeAlpha Python Internship - Task 2", "dim"))

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            if add_stock_flow(portfolio):
                unsaved = True
        elif choice == "2":
            if remove_stock_flow(portfolio):
                unsaved = True
        elif choice == "3":
            view_flow(portfolio)
        elif choice == "4":
            percentage_flow(portfolio)
        elif choice == "5":
            if save_flow(portfolio):
                unsaved = False
        elif choice == "6":
            if portfolio and unsaved:
                answer = input("You have unsaved changes. Save before exit? (y/n): ")
                if answer.strip().lower().startswith("y"):
                    save_flow(portfolio)
            print(paint("\nThank you for using the Stock Portfolio Tracker. Goodbye! 👋", "green"))
            break
        else:
            print(paint("  ✗ Please type a number from 1 to 6.", "red"))


# Run main() only when this file is executed directly (not when imported).
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram stopped. Goodbye!")
