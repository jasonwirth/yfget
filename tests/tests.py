__author__ = 'jasonwirth'

from lxml import etree, html
from yfget import YahooFinanceGet, Converter
import unittest



class TestFormatConverter(unittest.TestCase):
    def test_convert_string_to_num(self):
        value = Converter.big_num_to_int('301.64B')
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
    #     value = self.yfget.lookup_table(table_name, col_name)
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

    # ---- Management Effectiveness ----------------------------------------


    def test_return_on_assets_ttm(self):
        value = self.yfget.return_on_assets_ttm()
        self.assertEqual(value, 0.0973,)


    def test_return_on_equity_ttm(self):
        value = self.yfget.return_on_equity_ttm()
        self.assertEqual(value, 0.1636)


    def test_revenue_ttm(self):
        value = self.yfget.revenue_ttm()
        self.assertEqual(value, 53500000000)


    def test_revenue_per_share_ttm(self):
        value = self.yfget.revenue_per_share_ttm()
        self.assertEqual(value, 162.86)


    def test_qtrly_revenue_growth_yoy(self):
        value = self.yfget.qtrly_revenue_growth_yoy()
        self.assertEqual(value, 0.3120)


    def test_gross_profit_ttm(self):
        value = self.yfget.gross_profit_ttm()
        self.assertEqual(value, 29540000000)


    def test_ebitda_ttm(self):
        value = self.yfget.ebitda_ttm()
        self.assertAlmostEqual(value, 16810000000, delta=5)


    def test_net_income_avl_to_common_ttm(self):
        value = self.yfget.net_income_avl_to_common_ttm()
        self.assertEqual(value, 11220000000)


    def test_diluted_eps_ttm(self):
        value = self.yfget.diluted_eps_ttm()
        self.assertEqual(value, 33.42)


    def test_qtrly_earnings_growth_yoy(self):
        value = self.yfget.qtrly_earnings_growth_yoy()
        self.assertEqual(value, 0.1580)


    def test_total_cash_mrq(self):
        value = self.yfget.total_cash_mrq()
        self.assertEqual(value, 50100000000)


    def test_total_cash_per_share_mrq(self):
        value = self.yfget.total_cash_per_share_mrq()
        self.assertEqual(value, 151.00)


    def test_total_debt_mrq(self):
        value = self.yfget.total_debt_mrq()
        self.assertEqual(value, 7380000000)


    def test_total_debt_to_equity_mrq(self):
        value = self.yfget.total_debt_to_equity_mrq()
        self.assertEqual(value, 9.77)


    def test_current_ratio_mrq(self):
        value = self.yfget.current_ratio_mrq()
        self.assertEqual(value, 4.74)


    def test_book_value_per_share_mrq(self):
        value = self.yfget.book_value_per_share_mrq()
        self.assertEqual(value, 228.01)


    def test_operating_cash_flow_ttm(self):
        value = self.yfget.operating_cash_flow_ttm()
        self.assertAlmostEqual(value, 16560000000, delta=5)


    def test_levered_free_cash_flow_ttm(self):
        value = self.yfget.levered_free_cash_flow_ttm()
        self.assertEqual(value, 10990000000)


    def test_text_equals(self):
        value = self.yfget.lookup_table('EBITDA (ttm)', exact=True)
        self.assertEquals(value, '16.81B' )