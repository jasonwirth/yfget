__author__ = 'jasonwirth'

from lxml import etree, html
from yfget import YahooFinanceGet, Converter


import unittest

class TestFormatConverter(unittest.TestCase):
    def test_convert_string_to_num(self):
        value = Converter.string_to_int('301.64B')
        self.assertEqual(value, 301640000000)


    def test_convert_percent_to_dec(self):
        value = Converter.percent_to_dec('25.30%')
        self.assertEqual(value, 0.253)


class TestGetSummary(unittest.TestCase):
    def setUp(self):
        yfg = YahooFinanceGet()

        yfg.load_summary_from_html('GOOG-Key-Statistics.html')

        self.yfget = yfg


    def test_has_root(self):
        self.assertIn("<Element html", self.yfget.root.__repr__())


    def test_get_company_name(self):
        name = self.yfget.get_company_name()

        self.assertEqual(name, 'Google Inc.')

    def test_get_company_symbol(self):
        symbol = self.yfget.get_company_symbol()
        self.assertEqual(symbol, 'GOOG')

    # def test_get_valuation(self):
    #
    #     self.yfget.get_table('Valuation Measures')


    # def test_get_table(self):
    #     table_name = "Valuation Measures"
    #     col_name = "Market Cap"
    #     value = self.yfget.get_table_data(table_name, col_name)
    #     self.assertEqual(value, '301.64B')



    #==================================================================================================================
    # VALUATION
    #==================================================================================================================
    def test_get_market_cap(self):
        market_cap_str = self.yfget.get_market_cap(fmt='str')
        market_cap_dec = self.yfget.get_market_cap()


        self.assertEqual(market_cap_str, '301.64B')
        self.assertEqual(market_cap_dec, 301640000000)


    def test_get_enterprise_value(self):
        value = self.yfget.get_enterprise_value()
        self.assertEqual(value, 261140000000)

    def test_get_trailing_pe(self):
        value = self.yfget.get_trailing_pe()
        self.assertEqual(value, 27.20)

    def test_get_forward_pe(self):
        value = self.yfget.get_forward_pe()
        self.assertEqual(value, 17.10)

    def test_get_peg_ratio(self):
        value = self.yfget.get_peg_ratio()
        self.assertEqual(value, 1.32)

    def test_get_price_to_sales_ttm(self):
        value = self.yfget.get_price_to_sales_ttm()
        self.assertEqual(value, 5.61)

    def test_get_price_to_book_mrq(self):
        value = self.yfget.get_price_to_book_mrq()
        self.assertEqual(value, 3.96)

    def test_get_enterprise_value_to_revenue_ttm(self):
        value = self.yfget.get_enterprise_value_to_revenue_ttm()
        self.assertEqual(value, 4.88)

    def test_get_enterprise_value_to_ebitda_ttm(self):
        value = self.yfget.get_enterprise_value_to_ebitda_ttm()
        self.assertEqual(value, 15.53)


    #==================================================================================================================
    #  Financial Highlights
    #==================================================================================================================
    # ---- Fiscal Year -----------------------------------------
    def test_fiscal_year_ends(self):
        value = self.yfget.fiscal_year_ends()
        self.assertEqual(value, "Dec 30")


    def test_most_recent_quarter_mrq(self):
        value = self.yfget.most_recent_quarter_mrq()
        self.assertEqual(value, "Mar 31, 2013")


    # ---- Profitability -----------------------------------------
    def test_profit_margin_ttm(self):
        value = self.yfget.profit_margin_ttm()
        # self.assertEqual(value, 0.2092)
        self.assertAlmostEquals(value, 0.2092)


    def test_operating_margin_ttm(self):
        value = self.yfget.operating_margin_ttm()
        self.assertEqual(value, 0.2530)

