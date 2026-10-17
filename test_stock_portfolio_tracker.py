"""
CodeAlpha Python Internship - Task 2: Stock Portfolio Tracker
Simple automatic tests.   Run with:  python -m unittest -v
"""

import os
import tempfile
import unittest

import stock_portfolio_tracker as spt


class TestCalculations(unittest.TestCase):
    def test_value_of_one_holding(self):
        self.assertEqual(spt.calculate_value("AAPL", 10), 1800)

    def test_total_of_portfolio(self):
        portfolio = {"AAPL": 10, "TSLA": 5}   # 1800 + 1250
        self.assertEqual(spt.calculate_total(portfolio), 3050)

    def test_empty_portfolio_total_is_zero(self):
        self.assertEqual(spt.calculate_total({}), 0)

    def test_adding_same_stock_twice_sums_quantity(self):
        portfolio = {}
        spt.add_to_portfolio(portfolio, "AAPL", 3)
        spt.add_to_portfolio(portfolio, "AAPL", 2)
        self.assertEqual(portfolio, {"AAPL": 5})

    def test_share_percentage(self):
        self.assertAlmostEqual(spt.calculate_share(250, 1000), 25.0)

    def test_share_with_zero_total_does_not_crash(self):
        self.assertEqual(spt.calculate_share(0, 0), 0.0)

    def test_money_format(self):
        self.assertEqual(spt.money(3050), "$3,050.00")

    def test_price_list_has_many_stocks(self):
        self.assertGreaterEqual(len(spt.STOCK_PRICES), 20)
        self.assertEqual(spt.STOCK_PRICES["AAPL"], 180)
        self.assertEqual(spt.STOCK_PRICES["TSLA"], 250)


class TestRemoving(unittest.TestCase):
    def test_remove_whole_stock(self):
        portfolio = {"AAPL": 10, "TSLA": 5}
        removed = spt.remove_from_portfolio(portfolio, "AAPL")
        self.assertEqual(removed, 10)
        self.assertEqual(portfolio, {"TSLA": 5})

    def test_remove_some_shares(self):
        portfolio = {"AAPL": 10}
        removed = spt.remove_from_portfolio(portfolio, "AAPL", 4)
        self.assertEqual(removed, 4)
        self.assertEqual(portfolio, {"AAPL": 6})

    def test_remove_more_than_owned_removes_all(self):
        portfolio = {"AAPL": 3}
        removed = spt.remove_from_portfolio(portfolio, "AAPL", 99)
        self.assertEqual(removed, 3)
        self.assertEqual(portfolio, {})


class TestReportsAndFiles(unittest.TestCase):
    def test_report_contains_total_and_codealpha(self):
        report = spt.build_report({"AAPL": 10, "TSLA": 5})
        self.assertIn("$3,050.00", report)
        self.assertIn("Largest holding  : AAPL", report)
        self.assertIn("CodeAlpha Python Internship - Task 2", report)

    def test_percentage_report(self):
        report = spt.build_percentage_report({"AAPL": 10, "TSLA": 5})
        self.assertIn("59.0%", report)   # 1800 / 3050
        self.assertIn("41.0%", report)   # 1250 / 3050

    def test_filename_cleaning(self):
        self.assertEqual(spt.make_filename("", "csv"), "portfolio.csv")
        self.assertEqual(spt.make_filename("my.txt", "csv"), "my.csv")
        self.assertEqual(spt.make_filename("../../evil", "txt"), "evil.txt")

    def test_save_txt_and_csv(self):
        portfolio = {"MSFT": 3}
        with tempfile.TemporaryDirectory() as folder:
            txt_path = os.path.join(folder, "p.txt")
            csv_path = os.path.join(folder, "p.csv")
            spt.save_as_txt(portfolio, txt_path)
            spt.save_as_csv(portfolio, csv_path)
            with open(txt_path, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("$990.00", text)
            self.assertIn("SHARE OF TOTAL PORTFOLIO", text)
            with open(csv_path, encoding="utf-8") as f:
                self.assertIn("TOTAL,,,990,100", f.read())


if __name__ == "__main__":
    unittest.main()
