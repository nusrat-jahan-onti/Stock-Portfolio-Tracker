# 📈 Stock Portfolio Tracker

**CodeAlpha Python Programming Internship – TASK 2**

A menu-driven console program that calculates the total value of your stock investments using a hardcoded price list. It shows each stock's share of the total as a percentage and can optionally save the result to a `.txt` or `.csv` file.

> 📘 Want to understand the code step by step? Read **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)**.

---

## 📋 CodeAlpha Task 2 – Requirements Checklist

| CodeAlpha Task 2 requirement | Status | How this project meets it |
|---|---|---|
| **Goal:** simple stock tracker that calculates total investment from manually defined prices | ✅ | `calculate_total()` = Σ price × quantity |
| User inputs stock names and quantity | ✅ | Menu option **1** (Add a stock) |
| Hardcoded dictionary of stock prices (e.g. `{"AAPL": 180, "TSLA": 250}`) | ✅ | `STOCK_PRICES` – keeps `AAPL: 180` and `TSLA: 250` exactly as in the task, plus 18 more stocks |
| Display total investment value | ✅ | Menu option **3** prints the table with **TOTAL INVESTMENT** |
| Optionally save the result in a `.txt` or `.csv` file | ✅ | Menu option **5** |
| Key concepts: dictionary, input/output, basic arithmetic, file handling | ✅ | All used (see below) |

## ✨ Extra Features (beyond the CodeAlpha minimum)

- ➕ **20 stocks** in the price list – adding more takes just one line
- ➖ **Remove a stock** – completely, or only some of its shares
- 📊 **Share % of every stock** – its own menu option (**4**) and also inside the full report, with bar charts
- 🏆 Largest holding and portfolio statistics
- 🎨 Coloured output (switches off automatically when not in a terminal)
- 🛡️ Input validation for stock names, quantities and menu choices
- 💾 Custom file name when saving, plus an unsaved-changes warning on exit
- 🧪 **15 automatic unit tests**
- 📦 No installation needed – only Python's standard library

## 🧠 Concepts Used

- **Dictionary** – prices (`STOCK_PRICES`) and the user's `portfolio`
- **Input / Output** – `input()` and `print()`
- **Basic arithmetic** – `price × quantity`, totals, percentages
- **File handling** – `open()`, `write()` and the `csv` module
- **Extras** – functions, `while`/`for` loops, f-strings, `try/except`, `lambda`, unit testing

## 🚀 How to Run

1. Install Python 3.8 or newer (https://www.python.org/downloads/).
2. Download this project folder.
3. Open a terminal inside the folder and run:

```bash
python stock_portfolio_tracker.py
```

(On some systems use `python3` instead of `python`.)

You can also paste the code into Google Colab or an online Python editor.

## 🖥️ Example Session

```
📈  STOCK PORTFOLIO TRACKER  📈
CodeAlpha Python Internship - Task 2

──────── MAIN MENU ────────
  1. Add a stock
  2. Remove a stock
  3. View portfolio & total
  4. Show share % of each stock
  5. Save to file (.txt / .csv)
  6. Exit
Choose an option (1-6): 1

Available stocks
────────────────────────────────────────
  AAPL   $180      AMD    $120
  TSLA   $250      ORCL   $115
  GOOGL  $140      ADBE   $520
  ...
Stock name (or 'back'): aapl
Quantity of AAPL: 10
  ✓ Added 10 x AAPL = $1,800.00
```

**Option 3 – full report:**

```
════════════════════════════════════════════════════════════════════
                      STOCK PORTFOLIO SUMMARY
                CodeAlpha Python Internship - Task 2
                    Generated: 2026-10-17 13:10
════════════════════════════════════════════════════════════════════
Stock      Qty     Price         Value   Share  Chart
────────────────────────────────────────────────────────────────────
AAPL        10      $180     $1,800.00   52.9%  ███████████
NVDA         2      $480       $960.00   28.2%  ██████
WMT          4      $160       $640.00   18.8%  ████
────────────────────────────────────────────────────────────────────
TOTAL INVESTMENT                                           $3,400.00
════════════════════════════════════════════════════════════════════
Different stocks : 3
Total shares     : 16
Largest holding  : AAPL (52.9% of portfolio)
```

**Option 4 – share % of each stock:**

```
SHARE OF TOTAL PORTFOLIO (%)
────────────────────────────────────────────────────────────────────
AAPL     52.9%  ████████████████
NVDA     28.2%  ████████
WMT      18.8%  ██████
────────────────────────────────────────────────────────────────────
TOTAL   100.0%  ($3,400.00)
```

**Option 2 – remove (all or some shares):**

```
You own: AAPL (10), TSLA (5), NVDA (3), WMT (4)
Stock to remove (or 'back'): nvda
How many shares of NVDA to remove? (1-3, or press Enter for all): 1
  ✓ Removed 1 x NVDA. 2 left.
```

## ➕ How to Add More Stocks

Open `stock_portfolio_tracker.py`, find `STOCK_PRICES` and add one line:

```python
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "SPOT": 190,    # <- your new stock
}
```
It appears in the menu automatically.

## 📂 Output Files

- `portfolio.txt` – the full report plus the share-% table (no colours); the report header mentions *CodeAlpha Python Internship - Task 2*
- `portfolio.csv` – columns `Stock, Quantity, Price, Value, Share %` with a final `TOTAL` row; opens in Excel or Google Sheets

## 🧪 Run the Tests

```bash
python -m unittest -v
```

You should see `Ran 15 tests ... OK`.

## 🗂️ Project Structure

```
CodeAlpha_StockPortfolioTracker/
├── stock_portfolio_tracker.py        # main program
├── test_stock_portfolio_tracker.py   # automatic tests
├── README.md                         # project overview (this file)
└── HOW_IT_WORKS.md                   # detailed explanation of the code
```

## 🔍 Code Overview

| Function | Purpose |
|---|---|
| `calculate_value()` | price × quantity for one stock |
| `calculate_total()` | total of the whole portfolio |
| `calculate_share()` | percentage of the portfolio for one stock |
| `remove_from_portfolio()` | remove all or some shares of a stock |
| `build_report()` | full summary table (screen and file) |
| `build_percentage_report()` | share-% table |
| `save_as_txt()` / `save_as_csv()` | write the result to a file |
| `add_stock_flow()` / `remove_stock_flow()` | menu options 1 and 2 |
| `view_flow()` / `percentage_flow()` / `save_flow()` | menu options 3, 4 and 5 |
| `main()` | runs the menu loop |

## 🔧 Ideas to Extend (optional)

- Add a "clear portfolio" option
- Save and load the portfolio between runs
- Fetch live prices from an API (needs the `requests` library)

## 👤 Author

Your Name – CodeAlpha Python Programming Intern
GitHub: `https://github.com/your-username`

---
*CodeAlpha Python Programming Internship – Task 2. Prices are fixed example values for learning purposes only and are not real market data.*
