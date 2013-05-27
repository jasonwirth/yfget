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


    def test_get_cell_date(self):
        value = self.yfget.lookup_table('Short % of Float', col_position=0)
        value = Converter.extract_date(value)
        self.assertEqual(value, 'Apr 30, 2013')


    #============================================================
    # Trading Information
    #============================================================

    def test_beta(self):
        value = self.yfget.beta()
        self.assertEqual(value, 1.16)


    def test_fifty_two_week_change(self):
        value = self.yfget.fifty_two_week_change()
        self.assertEqual(value, 0.4805)


    def test_sp500_fifty_two_week_change(self):
        value = self.yfget.sp500_fifty_two_week_change()
        self.assertEqual(value, 0.2874)


    def test_fifty_two_week_high_price(self):
        value = self.yfget.fifty_two_week_high_price()
        self.assertEqual(value, 919.98)


    def test_fifty_two_week_high_date(self):
        value = self.yfget.fifty_two_week_high_date()
        self.assertEqual(value, "May 16, 2013")


    def test_fifty_two_week_low_price(self):
        value = self.yfget.fifty_two_week_low_price()
        self.assertEqual(value, 556.52)


    def test_fifty_two_week_low_date(self):
        value = self.yfget.fifty_two_week_low_date()
        self.assertEqual(value, "Jun 14, 2012")


    def test_fifty_day_moving_average(self):
        value = self.yfget.fifty_day_moving_average()
        self.assertEqual(value, 824.41)


    def test_two_hundred_day_moving_average(self):
        value = self.yfget.two_hundred_day_moving_average()
        self.assertEqual(value, 761.92)


    def test_avg_vol_3_month(self):
        value = self.yfget.avg_vol_3_month()
        self.assertEqual(value, 2314660)


    def test_avg_vol_10_day(self):
        value = self.yfget.avg_vol_10_day()
        self.assertEqual(value, 2447740)


    def test_shares_outstanding(self):
        value = self.yfget.shares_outstanding()
        self.assertEqual(value, 331770000)


    def test_float(self):
        value = self.yfget.float()
        self.assertEqual(value, 270730000)


    def test_pct_held_by_insiders(self):
        value = self.yfget.pct_held_by_insiders()
        self.assertAlmostEqual(value, 0.0033)


    def test_pct_held_by_institutions(self):
        value = self.yfget.pct_held_by_institutions()
        self.assertEqual(value, 0.8560)


    def test_shares_short_value(self):
        value = self.yfget.shares_short_value()
        self.assertEqual(value, 4120000)


    def test_shares_short_date(self):
        value = self.yfget.shares_short_date()
        self.assertEqual(value, "Apr 30, 2013")


    def test_short_ratio_value(self):
        value = self.yfget.short_ratio_value()
        self.assertEqual(value, 1.70)


    def test_short_ratio_date(self):
        value = self.yfget.short_ratio_date()
        self.assertEqual(value, "Apr 30, 2013")


    def test_short_pct_of_float_value(self):
        value = self.yfget.short_pct_of_float_value()
        self.assertEqual(value, 0.0150)


    def test_short_pct_of_float_date(self):
        value = self.yfget.short_pct_of_float_date()
        self.assertEqual(value, "Apr 30, 2013")


    def test_shares_short_prior_month(self):
        value = self.yfget.shares_short_prior_month()
        self.assertEqual(value, 3560000)


    def test_forward_annual_dividend_rate(self):
        value = self.yfget.forward_annual_dividend_rate()
        self.assertEqual(value, 'N/A')


    def test_forward_annual_dividend_yield(self):
        value = self.yfget.forward_annual_dividend_yield()
        self.assertEqual(value, 'N/A')


    def test_trailing_annual_dividend_yield(self):
        value = self.yfget.trailing_annual_dividend_yield()
        self.assertEqual(value, 'N/A')


    def test_trailing_annual_dividend_yield(self):
        value = self.yfget.trailing_annual_dividend_yield()
        self.assertEqual(value, 'N/A')


    def test_five_year_average_dividend_yield(self):
        value = self.yfget.five_year_average_dividend_yield()
        self.assertEqual(value, 'N/A')


    def test_payout_ratio(self):
        value = self.yfget.payout_ratio()
        self.assertEqual(value, 'N/A')


    def test_dividend_date(self):
        value = self.yfget.dividend_date()
        self.assertEqual(value, 'N/A')


    def test_ex_dividend_date(self):
        value = self.yfget.ex_dividend_date()
        self.assertEqual(value, 'N/A')


    def test_last_split_factor_new_per_old(self):
        value = self.yfget.last_split_factor_new_per_old()
        self.assertEqual(value, 'N/A')


    def test_last_split_date(self):
        value = self.yfget.last_split_date()
        self.assertEqual(value, 'N/A')


class TestLoadingURLData(unittest.TestCase):
    def test_loads_url_and_reads_name(self):
        yfget = YahooFinanceGet()
        yfget.load_summary_from_url(symbol='GOOG')

        self.assertEqual(yfget.get_company_name(), "Google Inc.")


    def test_loading_incorrect_symbol(self):
        yfget = YahooFinanceGet()
        self.assertRaises(IOError, yfget.load_summary_from_url,'GOGG')



class TestGetSummaryText(unittest.TestCase):
    def setUp(self):
        yfg = YahooFinanceGet()
        yfg.load_summary_from_html('GOOG-Key-Statistics.html')
        self.yfget = yfg


    #==================================================================================================================
    # VALUATION
    #==================================================================================================================
    def test_get_market_cap_text(self):
        market_cap_str = self.yfget.get_market_cap(fmt='str')
        market_cap_dec = self.yfget.get_market_cap()

        self.assertEqual(market_cap_str, '301.64B')
        self.assertEqual(market_cap_dec, 301640000000)


    def test_get_enterprise_value_text(self):
        value = self.yfget.get_enterprise_value(format="text")
        self.assertEqual(value, "261.14B")


    def test_get_trailing_pe_text(self):
        value = self.yfget.get_trailing_pe(format="text")
        self.assertEqual(value, "27.20")


    def test_get_forward_pe_text(self):
        value = self.yfget.get_forward_pe(format="text")
        self.assertEqual(value, "17.10")


    def test_get_peg_ratio_text(self):
        value = self.yfget.get_peg_ratio(format="text")
        self.assertEqual(value, "1.32")


    def test_get_price_to_sales_ttm_text(self):
        value = self.yfget.get_price_to_sales_ttm(format="text")
        self.assertEqual(value, "5.61")


    def test_get_price_to_book_mrq_text(self):
        value = self.yfget.get_price_to_book_mrq(format="text")
        self.assertEqual(value, "3.96")


    def test_get_enterprise_value_to_revenue_ttm_text(self):
        value = self.yfget.get_enterprise_value_to_revenue_ttm(format="text")
        self.assertEqual(value, "4.88")


    def test_get_enterprise_value_to_ebitda_ttm_text(self):
        value = self.yfget.get_enterprise_value_to_ebitda_ttm(format="text")
        self.assertEqual(value, "15.53")


    #==================================================================================================================
    #  Financial Highlights
    #==================================================================================================================
    # ---- Fiscal Year -----------------------------------------
    def test_fiscal_year_ends_text(self):
        value = self.yfget.fiscal_year_ends(format="text")
        self.assertEqual(value, "Dec 30")


    def test_most_recent_quarter_mrq_text(self):
        value = self.yfget.most_recent_quarter_mrq(format="text")
        self.assertEqual(value, "Mar 31, 2013")


    # ---- Profitability -----------------------------------------
    def test_profit_margin_ttm_text(self):
        value = self.yfget.profit_margin_ttm(format="text")
        # self.assertEqual(value, 0.2092)
        self.assertAlmostEquals(value, "20.92%")


    def test_operating_margin_ttm_text(self):
        value = self.yfget.operating_margin_ttm(format="text")
        self.assertEqual(value, "25.30%")


    # ---- Management Effectiveness ----------------------------------------


    def test_return_on_assets_ttm_text(self):
        value = self.yfget.return_on_assets_ttm(format="text")
        self.assertEqual(value, "9.73%")


    def test_return_on_equity_ttm_text(self):
        value = self.yfget.return_on_equity_ttm(format="text")
        self.assertEqual(value, "16.36%")


    def test_revenue_ttm_text(self):
        value = self.yfget.revenue_ttm(format="text")
        self.assertEqual(value, "53.50B")


    def test_revenue_per_share_ttm_text(self):
        value = self.yfget.revenue_per_share_ttm(format="text")
        self.assertEqual(value, "162.86")


    def test_qtrly_revenue_growth_yoy_text(self):
        value = self.yfget.qtrly_revenue_growth_yoy(format="text")
        self.assertEqual(value, "31.20%")


    def test_gross_profit_ttm_text(self):
        value = self.yfget.gross_profit_ttm(format="text")
        self.assertEqual(value, "29.54B")


    def test_ebitda_ttm_text(self):
        value = self.yfget.ebitda_ttm(format="text")
        self.assertAlmostEqual(value, "16.81B")


    def test_net_income_avl_to_common_ttm_text(self):
        value = self.yfget.net_income_avl_to_common_ttm(format="text")
        self.assertEqual(value, "11.22B")


    def test_diluted_eps_ttm_text(self):
        value = self.yfget.diluted_eps_ttm(format="text")
        self.assertEqual(value, "33.42")


    def test_qtrly_earnings_growth_yoy_text(self):
        value = self.yfget.qtrly_earnings_growth_yoy(format="text")
        self.assertEqual(value, "15.80%")


    def test_total_cash_mrq_text(self):
        value = self.yfget.total_cash_mrq(format="text")
        self.assertEqual(value, "50.10B")


    def test_total_cash_per_share_mrq_text(self):
        value = self.yfget.total_cash_per_share_mrq(format="text")
        self.assertEqual(value, "151.00")


    def test_total_debt_mrq_text(self):
        value = self.yfget.total_debt_mrq(format="text")
        self.assertEqual(value, "7.38B")


    def test_total_debt_to_equity_mrq_text(self):
        value = self.yfget.total_debt_to_equity_mrq(format="text")
        self.assertEqual(value, "9.77")


    def test_current_ratio_mrq_text(self):
        value = self.yfget.current_ratio_mrq(format="text")
        self.assertEqual(value, "4.74")


    def test_book_value_per_share_mrq_text(self):
        value = self.yfget.book_value_per_share_mrq(format="text")
        self.assertEqual(value, "228.01")


    def test_operating_cash_flow_ttm_text(self):
        value = self.yfget.operating_cash_flow_ttm(format="text")
        self.assertAlmostEqual(value, "16.56B", delta=5)


    def test_levered_free_cash_flow_ttm_text(self):
        value = self.yfget.levered_free_cash_flow_ttm(format="text")
        self.assertEqual(value, "10.99B")


    def test_text_equals_text(self):
        value = self.yfget.lookup_table('EBITDA (ttm)', exact=True)
        self.assertEquals(value, '16.81B')


    #============================================================
    # Trading Information
    #============================================================

    def test_beta_text(self):
        value = self.yfget.beta(format="text")
        self.assertEqual(value, "1.16")


    def test_fifty_two_week_change_text(self):
        value = self.yfget.fifty_two_week_change(format="text")
        self.assertEqual(value, "48.05%")


    def test_sp500_fifty_two_week_change_text(self):
        value = self.yfget.sp500_fifty_two_week_change(format="text")
        self.assertEqual(value, "28.74%")


    def test_fifty_two_week_high_price_text(self):
        value = self.yfget.fifty_two_week_high_price(format="text")
        self.assertEqual(value, "919.98")


    def test_fifty_two_week_low_price_text(self):
        value = self.yfget.fifty_two_week_low_price(format="text")
        self.assertEqual(value, "556.52")


    def test_fifty_day_moving_average_text(self):
        value = self.yfget.fifty_day_moving_average(format="text")
        self.assertEqual(value, "824.41")


    def test_two_hundred_day_moving_average_text(self):
        value = self.yfget.two_hundred_day_moving_average(format="text")
        self.assertEqual(value, "761.92")


    def test_avg_vol_3_month_text(self):
        value = self.yfget.avg_vol_3_month(format="text")
        self.assertEqual(value, "2,314,660")


    def test_avg_vol_10_day_text(self):
        value = self.yfget.avg_vol_10_day(format="text")
        self.assertEqual(value, "2,447,740")


    def test_shares_outstanding_text(self):
        value = self.yfget.shares_outstanding(format="text")
        self.assertEqual(value, "331.77M")


    def test_float_text(self):
        value = self.yfget.float(format="text")
        self.assertEqual(value, "270.73M")


    def test_pct_held_by_insiders_text(self):
        value = self.yfget.pct_held_by_insiders(format="text")
        self.assertAlmostEqual(value, "0.33%")


    def test_pct_held_by_institutions_text(self):
        value = self.yfget.pct_held_by_institutions(format="text")
        self.assertEqual(value, "85.60%")


    def test_shares_short_value_text(self):
        value = self.yfget.shares_short_data(format="text")
        self.assertEqual(value, "4.12M")


    def test_short_ratio_value_text(self):
        value = self.yfget.short_ratio_data(format="text")
        self.assertEqual(value, "1.70")


    def test_short_pct_of_float_value_text(self):
        value = self.yfget.short_pct_of_float_data(format="text")
        self.assertEqual(value, "1.50%")


    def test_shares_short_prior_month_text(self):
        value = self.yfget.shares_short_prior_month(format="text")
        self.assertEqual(value, "3.56M")


    def test_forward_annual_dividend_rate_text(self):
        value = self.yfget.forward_annual_dividend_rate(format="text")
        self.assertEqual(value, 'N/A')


    def test_forward_annual_dividend_yield_text(self):
        value = self.yfget.forward_annual_dividend_yield(format="text")
        self.assertEqual(value, 'N/A')


    def test_trailing_annual_dividend_yield_text(self):
        value = self.yfget.trailing_annual_dividend_yield(format="text")
        self.assertEqual(value, 'N/A')


    def test_trailing_annual_dividend_yield_text(self):
        value = self.yfget.trailing_annual_dividend_yield(format="text")
        self.assertEqual(value, 'N/A')


    def test_five_year_average_dividend_yield_text(self):
        value = self.yfget.five_year_average_dividend_yield(format="text")
        self.assertEqual(value, 'N/A')


    def test_payout_ratio_text(self):
        value = self.yfget.payout_ratio(format="text")
        self.assertEqual(value, 'N/A')


    def test_dividend_date_text(self):
        value = self.yfget.dividend_date(format="text")
        self.assertEqual(value, 'N/A')


    def test_ex_dividend_date_text(self):
        value = self.yfget.ex_dividend_date(format="text")
        self.assertEqual(value, 'N/A')


    def test_last_split_factor_new_per_old_text(self):
        value = self.yfget.last_split_factor_new_per_old(format="text")
        self.assertEqual(value, 'N/A')


    def test_last_split_date_text(self):
        value = self.yfget.last_split_date(format="text")
        self.assertEqual(value, 'N/A')

