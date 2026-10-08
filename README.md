# 📈 Stock Portfolio Tracker

**CodeAlpha Python Programming Internship – Task 2**

A beginner-friendly console program that calculates the total value of your stock investments using a hardcoded price list, and optionally saves the result to a `.txt` or `.csv` file.

---

## ✅ Task Requirements (and how they are met)

| Requirement | How this project meets it |
|---|---|
| User inputs stock names and quantity | `collect_portfolio()` asks for a stock name and a quantity in a loop |
| Hardcoded dictionary of stock prices | `STOCK_PRICES = {"AAPL": 180, "TSLA": 250, ...}` |
| Display total investment value | `build_report()` + `calculate_total()` print a table and the total |
| Optionally save to `.txt` or `.csv` | `save_as_txt()` and `save_as_csv()` |
| Key concepts: dictionary, input/output, arithmetic, file handling | All used (see below) |

## 🧠 Concepts Used

- **Dictionary** – stores prices (`STOCK_PRICES`) and the user's portfolio
- **Input / Output** – `input()` and `print()`
- **Basic arithmetic** – `price * quantity`, summed into a total
- **File handling** – `open()`, `write()`, and the `csv` module
- **Extras** – functions, `while` loops, input validation, f-string formatting

## 🚀 How to Run

1. Install Python 3.8 or newer (https://www.python.org/downloads/).
2. Download `stock_portfolio_tracker.py`.
3. Open a terminal in that folder and run:

```bash
python stock_portfolio_tracker.py
```

(On some systems use `python3` instead of `python`.)

You can also run it in Google Colab or any online Python editor by pasting the code in.

## 🖥️ Example Session

```
=== Welcome to the Stock Portfolio Tracker ===

Available stocks:
------------------------
  AAPL   $180
  TSLA   $250
  GOOGL  $140
  MSFT   $330
  AMZN   $130
------------------------

Stock name (or 'done'): aapl
Enter quantity of AAPL: 10
  Added 10 x AAPL.

Stock name (or 'done'): TSLA
Enter quantity of TSLA: 5
  Added 5 x TSLA.

Stock name (or 'done'): done

============================================
        STOCK PORTFOLIO SUMMARY
============================================
Stock      Qty     Price         Value
--------------------------------------------
AAPL        10      $180     $1,800.00
TSLA         5      $250     $1,250.00
--------------------------------------------
TOTAL INVESTMENT:                  $3,050.00
============================================

Save result to a file? (txt / csv / no): csv
Saved to portfolio.csv
```

## 📂 Output Files

- `portfolio.txt` – the summary table plus the date and time it was saved
- `portfolio.csv` – columns `Stock, Quantity, Price, Value`, with a final `TOTAL` row; opens in Excel or Google Sheets

## 🗂️ Project Structure

```
CodeAlpha_StockPortfolioTracker/
├── stock_portfolio_tracker.py   # main program
└── README.md                    # this documentation
```

## 🔍 Code Overview

| Function | Purpose |
|---|---|
| `show_available_stocks()` | Prints the stocks and their prices |
| `get_quantity()` | Asks for a quantity until a valid whole number is typed |
| `collect_portfolio()` | Collects stock names and quantities from the user |
| `calculate_total()` | Adds up price × quantity for every stock |
| `build_report()` | Builds the summary text |
| `save_as_txt()` / `save_as_csv()` | Write the result to a file |
| `ask_to_save()` | Asks whether and how to save |
| `main()` | Runs everything in order |

## 🛡️ Input Handling

- Stock names are not case-sensitive (`aapl` works the same as `AAPL`)
- Unknown stock names are rejected with a message
- Quantity must be a whole number greater than 0
- Entering the same stock twice adds the quantities together
- Pressing `done` with nothing added exits politely

## 🔧 Ideas to Extend (optional)

- Add more stocks to `STOCK_PRICES`
- Allow removing a stock from the portfolio
- Show each stock's share of the total as a percentage
- Fetch live prices from an API (needs the `requests` library)

## 👤 Author

Your Name – CodeAlpha Python Programming Intern
GitHub: `https://github.com/your-username`

---
*Prices are fixed example values for learning purposes only and are not real market data.*
