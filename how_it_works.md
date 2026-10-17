# 🔍 How It Works

**CodeAlpha Python Programming Internship – Task 2: Stock Portfolio Tracker**

This file explains, step by step, how the program works inside.
It is written for beginners, so you can understand every part and explain it confidently
(for example in your LinkedIn video).

---

## 1. The Big Picture

```
        ┌────────────────────┐
        │   STOCK_PRICES     │  ← hardcoded dictionary (the "price list")
        └─────────┬──────────┘
                  │
 User types ──►  portfolio  ──► calculate ──► report ──► screen
 name + qty     (dictionary)     total        (table)     └──► .txt / .csv file
```

The program keeps **two dictionaries**:

| Dictionary | Example | Purpose |
|---|---|---|
| `STOCK_PRICES` | `{"AAPL": 180, "TSLA": 250}` | Fixed price of **one share** (never changes while running) |
| `portfolio` | `{"AAPL": 10, "TSLA": 5}` | How many shares the **user** owns |

Everything else is just reading from these two dictionaries and doing simple maths.

---

## 2. The Core Maths

For each stock:

```
value of one holding = price of one share × quantity
```

Then:

```
total investment = sum of all holding values
share of portfolio (%) = holding value ÷ total × 100
```

**Example**

| Stock | Qty | Price | Value | Share |
|---|---|---|---|---|
| AAPL | 10 | $180 | $1,800 | 59.0 % |
| TSLA | 5 | $250 | $1,250 | 41.0 % |
| **Total** | | | **$3,050** | 100 % |

In code (`calculate_total`):

```python
total = 0
for name, quantity in portfolio.items():
    total += STOCK_PRICES[name] * quantity
```

---

## 3. Program Flow

```
START
  │
  ▼
Show MAIN MENU  ◄──────────────────────────┐
  │                                         │
  ├─ 1 → Add a stock      ──────────────────┤
  ├─ 2 → Remove a stock   ──────────────────┤
  ├─ 3 → View full report ──────────────────┤
  ├─ 4 → Show share % ──────────────────────┤
  ├─ 5 → Save to file     ──────────────────┤
  ├─ other → "Please type 1 to 6" ──────────┘
  │
  └─ 6 → (ask to save if unsaved) → Goodbye → END
```

The menu runs inside a `while True:` loop. It only stops when the user chooses **6**
(`break`).

---

## 4. Each Menu Option Explained

### Option 1 – Add a stock (`add_stock_flow`)
1. Shows all available stocks and prices.
2. Asks for a stock name and converts it to **UPPERCASE** (`aapl` → `AAPL`).
3. If the name is not in `STOCK_PRICES`, shows an error and asks again.
4. Asks for a quantity (`ask_quantity`) – repeats until the user types a whole number ≥ 1.
5. Calls `add_to_portfolio`. If you add the same stock twice, quantities are **added together**.

```python
portfolio[name] = portfolio.get(name, 0) + quantity
```
`.get(name, 0)` returns the old quantity, or `0` if the stock is new.

### Option 2 – Remove a stock (`remove_stock_flow`)
1. Shows what you own and asks which stock to remove.
2. Asks **how many shares** to remove – type a number, or just press **Enter** to remove all of them.
3. `remove_from_portfolio()` does the work:
   - no number, or a number ≥ what you own → the stock is deleted (`del portfolio[name]`)
   - a smaller number → only the quantity is lowered (`portfolio[name] = owned - quantity`)

Example: you own 10 AAPL and remove 4 → 6 AAPL are left.

### Option 3 – View portfolio (`view_flow`)
Calls `build_report(portfolio, color=True)` and prints the coloured table with the total.

### Option 4 – Show share % of each stock (`percentage_flow`)
Calls `build_percentage_report()`, which prints only the percentage of each stock with a long
bar, biggest first:

```
AAPL     52.9%  ████████████████
NVDA     28.2%  ████████
```
The formula is `holding value ÷ total × 100` (`calculate_share`).

### Option 5 – Save to file (`save_flow`)
1. Asks for `txt` or `csv`.
2. Asks for a file name (Enter = default `portfolio.txt` / `portfolio.csv`).
3. Cleans the name with `make_filename` (blocks tricks like `../../file` and forces the right extension).
4. Saves with `save_as_txt` or `save_as_csv`.
5. Wrapped in `try / except OSError` so the program never crashes if saving fails.

### Option 6 – Exit
If there are **unsaved changes**, the program asks whether you want to save first.
This uses a simple True/False variable called `unsaved`.

---

## 5. How the Price List Grows

`STOCK_PRICES` holds **20 stocks**. The task example (`AAPL: 180`, `TSLA: 250`) is kept exactly,
and 18 more are added. To add another one, add a line such as `"SPOT": 190,`. Nothing else
needs to change – the menu, the validation and the report all read from this dictionary.

The "Available stocks" list is printed in **two columns** so 20 stocks still fit on the screen.

---

## 5b. How the Report Is Built (`build_report`)

1. Calculates the total.
2. Gets the rows from `sorted_rows()`, a list of `(name, quantity, price, value)`.
3. `sorted_rows()` **sorts** them so the biggest value comes first:
   ```python
   rows.sort(key=lambda row: row[3], reverse=True)
   ```
4. Prints each row with aligned columns using f-string formatting:
   - `{name:<8}` → left-align in 8 characters
   - `{quantity:>6}` → right-align in 6 characters
   - `{value:,.2f}` → thousands separator + 2 decimals (`1,800.00`)
5. Draws a bar chart: every 5 % = one `█` block.
   ```python
   bar = "█" * round(share / BAR_UNIT)
   ```
6. Adds extra facts: number of stocks, total shares, largest holding.

The same function builds the **screen** version (with colours) and the **file** version
(plain text) – only the `color` argument changes. This avoids writing the code twice.

---

## 6. File Handling

### `.txt` file
Writes the plain report exactly as it looks on screen (without colours), followed by the
share-% table. The header contains *CodeAlpha Python Internship - Task 2*.

### `.csv` file
Uses Python's built-in `csv` module:

```
Stock,Quantity,Price,Value,Share %
AAPL,10,180,1800,59.02
TSLA,5,250,1250,40.98
TOTAL,,,3050,100
```
Open it in Excel or Google Sheets to see a normal table.

Both use `with open(...)`, which **automatically closes the file** when finished.

---

## 7. Safety & Error Handling

| Problem | What the program does |
|---|---|
| Unknown stock name | Shows an error, asks again |
| Quantity is text, `0`, negative or decimal | Shows an error, asks again |
| Wrong menu number | Shows "Please type a number from 1 to 6" |
| Empty portfolio | Friendly message instead of an empty table |
| Removing a stock you do not own | Error message, nothing changes |
| Removing more shares than you own | The stock is simply removed completely |
| Dividing by zero (total = 0) | `calculate_share` returns `0.0` instead of crashing |
| File cannot be saved | Error message, program keeps running |
| User presses Ctrl+C | Program says goodbye instead of showing an error |

---

## 8. Colours in the Terminal

Colours use **ANSI escape codes** such as `"\033[92m"` (green). The `paint()` function adds
a colour code before the text and a reset code after it.

Colours are switched **off automatically** when:
- the output is not a real terminal (`sys.stdout.isatty()`), or
- the environment variable `NO_COLOR` is set.

This is why saved files never contain strange colour characters.

---

## 9. Why Functions Are Split This Way

The code is divided into clear sections:

| Section | Contains | Uses `input`/`print`? |
|---|---|---|
| 1. Data | `STOCK_PRICES` | – |
| 2. Colours | `paint`, `setup_terminal` | – |
| 3. Calculations | `calculate_value`, `calculate_total`, `calculate_share`, `add_to_portfolio`, `remove_from_portfolio`, `sorted_rows`, `money` | **No** |
| 4. Reports | `build_report`, `build_percentage_report` | No (return text) |
| 5. File handling | `save_as_txt`, `save_as_csv`, `make_filename` | No |
| 6. User input | `add_stock_flow`, `save_flow`, ... | **Yes** |
| 7. Main | `main` | Yes |

Keeping calculations separate from `input()`/`print()` makes them **easy to test**.
That is why `test_stock_portfolio_tracker.py` can check the maths automatically.

---

## 10. Running the Automatic Tests

```bash
python -m unittest -v
```

The 15 tests check: value of a holding, total, empty portfolio, adding the same stock twice,
percentages, zero-total safety, money format, the 20-stock price list, removing all / some /
too many shares, report content (including the CodeAlpha header), the share-% report,
file-name cleaning, and saving both `.txt` and `.csv` files. If everything is correct you will see `OK`.

---

## 11. Python Concepts Used (cheat sheet)

| Concept | Where |
|---|---|
| Dictionary | `STOCK_PRICES`, `portfolio` |
| `input()` / `print()` | all `*_flow` functions |
| Arithmetic | `calculate_value`, `calculate_total`, `calculate_share` |
| `while` loop | main menu, quantity check |
| `for` loop | totals, report rows |
| `if / elif / else` | menu choices |
| Functions | whole program |
| f-strings | report formatting |
| `lambda` | sorting rows |
| File handling (`open`, `csv`) | saving results |
| `try / except` | saving files, Ctrl+C |
| `if __name__ == "__main__"` | program entry point |

---

## 12. Try It Yourself (practice ideas)

1. Add a new stock to `STOCK_PRICES` and see it appear in the menu.
2. Change `BAR_UNIT` from `5` to `10` – what happens to the chart?
3. Change `REPORT_WIDTH` and see how the table changes.
4. Add a menu option that clears the whole portfolio.
5. Add 5 more stocks to `STOCK_PRICES` and check the two-column list.
