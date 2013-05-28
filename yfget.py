import urllib
import urllib2

__author__ = 'jasonwirth'


from lxml import etree, html
import re



class Converter(object):
    @classmethod
    def big_num_to_int(cls, str_num, decimals=2):
        letter = str_num[-1]
        num = str_num[:-1]
        left, right = num.split('.')
        left, right = int(left), int(right)
        if letter =='M':
            value = left * 1e6 + right * 1e4 
        elif letter == 'B':
            value = left * 1e9 + right * 1e7
        elif letter == "T":
            value = left * 1e12 + right * 1e9
        return value


    @classmethod
    def percent_to_dec(cls, percent_str, decimals=4):
        value = percent_str[:-1]
        value = float(value)
        return round(value / 100, decimals)


    @classmethod
    def extract_date(cls, text):
        pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}"
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        else:
            return None


    @classmethod
    def remove_comma(cls, str_num):
        return int(str_num.replace(',', ''))




class YahooFinanceGet(object):
    def __init__(self):
        self.data = None
        self.root = None


    def load_summary_from_html(self, html_file):
        with open(html_file, 'r') as f:
            html_string = f.read()
        self.root = html.fromstring(html_string)


    def load_summary_from_url(self, symbol):
        address = "http://finance.yahoo.com/q/ks?s=%s+Key+Statistics" % (symbol)
        url = urllib2.urlopen(address)
        html_string = url.read()
        root = html.fromstring(html_string)
        # Look for error code in html
        contents = root.text_content()
        err_msg = "There are no All Markets results for %s" % (symbol)
        if err_msg in contents:
            raise IOError(err_msg)
        self.root = root


    def get_company_name(self):
        element = self.root.xpath('//div[@class="title"]/h2')[0]
        name_and_symbol = element.text_content()
        name = name_and_symbol.split(' ')[:-1]
        name = ' '.join(name)
        return name


    def get_company_symbol(self):
        element = self.root.xpath('//div[@class="title"]/h2')[0]
        name_and_symbol = element.text_content()
        symbol = name_and_symbol.split(' ')[-1]
        symbol = symbol[1:-1]
        return symbol


    def lookup_table(self, column_name, col_position=1, occurrence=0, exact=False):
        """
        Searches table table for values
        :param column_name:  specify the field to look up, similar to vlookup
        :param col_position: number of offset in the table, 0 is the column name, 1... is the first value
        :param occurrence: sometimes there are multiple matches, this finds the n-th occurrence (0-based index)
        :param exact: Finds the exact match.
        :return: text from the cell
        """
        if exact:
            xpath = "//td[text()='%s']" % column_name
        else:
            xpath = "//td[contains(text(),'%s')]" % column_name
        title_td = self.root.xpath(xpath)[occurrence]
        tr = title_td.getparent()
        row = tr.getchildren()
        return row[col_position ].text_content()


    def get_market_cap(self, fmt='dec'):
        data = self.lookup_table('Market Cap')
        if fmt == 'dec':
            return Converter.big_num_to_int(data)
        if fmt == 'str':
            return data


    def get_enterprise_value(self, fmt=None):
        data = self.lookup_table('Enterprise Value')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def get_trailing_pe(self, fmt=None):
        data = self.lookup_table('Trailing P/E')
        if fmt == "text":
            return data
        return float(data)


    def get_forward_pe(self, fmt=None):
        data = self.lookup_table('Forward P/E')
        if fmt == "text":
            return data
        return float(data)


    def get_peg_ratio(self, fmt=None):
        data = self.lookup_table('PEG Ratio')
        if fmt == "text":
            return data
        return float(data)


    def get_price_to_sales_ttm(self, fmt=None):
        data = self.lookup_table('Price/Sales')
        if fmt == "text":
            return data
        return float(data)


    def get_price_to_book_mrq(self, fmt=None):
        data = self.lookup_table('Price/Book')
        if fmt == "text":
            return data
        return float(data)


    def get_enterprise_value_to_revenue_ttm(self, fmt=None):
        data = self.lookup_table('Enterprise Value/Revenue')
        if fmt == "text":
            return data
        return float(data)


    def get_enterprise_value_to_ebitda_ttm(self, fmt=None):
        data = self.lookup_table('Enterprise Value/EBITDA')
        if fmt == "text":
            return data
        return float(data)


    #===========================================================
    #  Financial highlights
    #-----------------------------------------------------------

    # ---- Fiscal Year -----------------------------------------

    def fiscal_year_ends(self, fmt=None):
        data = self.lookup_table('Fiscal Year Ends')
        if fmt == "text":
            return data
        return data


    def most_recent_quarter_mrq(self, fmt=None):
        data = self.lookup_table('Most Recent Quarter (mrq)')
        if fmt == "text":
            return data
        return data


    # ---- Profitability ----------------------------------------

    def profit_margin_ttm(self, fmt=None):
        data = self.lookup_table('Profit Margin')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def operating_margin_ttm(self, fmt=None):
        data = self.lookup_table('Operating Margin')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    # ---- Management Effectiveness ----------------------------------------

    def return_on_assets_ttm(self, fmt=None):
        data = self.lookup_table('Return on Assets (ttm)')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def return_on_equity_ttm(self, fmt=None):
        data = self.lookup_table('Return on Equity (ttm)')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def revenue_ttm(self, fmt=None):
        data = self.lookup_table('Revenue (ttm)', occurrence=1)
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def revenue_per_share_ttm(self, fmt=None):
        data = self.lookup_table('Revenue Per Share (ttm)')
        if fmt == "text":
            return data
        return float(data)


    def qtrly_revenue_growth_yoy(self, fmt=None):
        data = self.lookup_table('Qtrly Revenue Growth (yoy)')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def gross_profit_ttm(self, fmt=None):
        data = self.lookup_table('Gross Profit (ttm)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def ebitda_ttm(self, fmt=None):
        data = self.lookup_table('EBITDA (ttm)', occurrence=1)
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def net_income_avl_to_common_ttm(self, fmt=None):
        data = self.lookup_table('Net Income Avl to Common (ttm)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def diluted_eps_ttm(self, fmt=None):
        data = self.lookup_table('Diluted EPS (ttm)')
        if fmt == "text":
            return data
        return float(data)


    def qtrly_earnings_growth_yoy(self, fmt=None):
        data = self.lookup_table('Qtrly Earnings Growth (yoy)')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def total_cash_mrq(self, fmt=None):
        data = self.lookup_table('Total Cash (mrq)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def total_cash_per_share_mrq(self, fmt=None):
        data = self.lookup_table('Total Cash Per Share (mrq)')
        if fmt == "text":
            return data
        return float(data)


    def total_debt_mrq(self, fmt=None):
        data = self.lookup_table('Total Debt (mrq)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def total_debt_to_equity_mrq(self, fmt=None):
        data = self.lookup_table('Total Debt/Equity (mrq)')
        if fmt == "text":
            return data
        return float(data)


    def current_ratio_mrq(self, fmt=None):
        data = self.lookup_table('Current Ratio (mrq)')
        if fmt == "text":
            return data
        return float(data)


    def book_value_per_share_mrq(self, fmt=None):
        data = self.lookup_table('Book Value Per Share (mrq)')
        if fmt == "text":
            return data
        return float(data)


    def operating_cash_flow_ttm(self, fmt=None):
        data = self.lookup_table('Operating Cash Flow (ttm)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def levered_free_cash_flow_ttm(self, fmt=None):
        data = self.lookup_table('Levered Free Cash Flow (ttm)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    #===========================================================
    #  TRADING INfmtION
    #===========================================================

    def beta(self, fmt=None):
        data = self.lookup_table('Beta')
        if fmt == "text":
            return data
        return float(data)


    def fifty_two_week_change(self, fmt=None):
        data = self.lookup_table('52-Week Change')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def sp500_fifty_two_week_change(self, fmt=None):
        data = self.lookup_table('S&P500 52-Week Change')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def fifty_two_week_high_price(self, fmt=None):
        data = self.lookup_table('52-Week High')
        if fmt == "text":
            return data
        return float(data)


    def fifty_two_week_high_date(self):
        data = self.lookup_table('52-Week High', col_position=0)
        return Converter.extract_date(data)


    def fifty_two_week_low_price(self, fmt=None):
        data = self.lookup_table('52-Week Low')
        if fmt == "text":
            return data
        return float(data)


    def fifty_two_week_low_date(self):
        data = self.lookup_table('52-Week Low', col_position=0)
        return Converter.extract_date(data)


    def fifty_day_moving_average(self, fmt=None):
        data = self.lookup_table('50-Day Moving Average')
        if fmt == "text":
            return data
        return float(data)


    def two_hundred_day_moving_average(self, fmt=None):
        data = self.lookup_table('200-Day Moving Average')
        if fmt == "text":
            return data
        return float(data)


    def avg_vol_3_month(self, fmt=None):
        data = self.lookup_table('Avg Vol (3 month)')
        if fmt == "text":
            return data
        return Converter.remove_comma(data)


    def avg_vol_10_day(self, fmt=None):
        data = self.lookup_table('Avg Vol (10 day)')
        if fmt == "text":
            return data
        return Converter.remove_comma(data)


    def shares_outstanding(self, fmt=None):
        data = self.lookup_table('Shares Outstanding')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def float(self, fmt=None):
        data = self.lookup_table('Float')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def pct_held_by_insiders(self, fmt=None):
        data = self.lookup_table("Held by Insiders")
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def pct_held_by_institutions(self, fmt=None):
        data = self.lookup_table('Held by Institutions')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def shares_short_data(self, fmt=None):
        data = self.lookup_table('Shares Short')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def shares_short_date(self):
        data = self.lookup_table('Shares Short', col_position=0)
        return Converter.extract_date(data)


    def short_ratio_data(self, fmt=None):
        data = self.lookup_table('Short Ratio')
        if fmt == "text":
            return data
        return float(data)


    def short_ratio_date(self):
        data = self.lookup_table('Short Ratio', col_position=0)
        return Converter.extract_date(data)


    def short_pct_of_float_data(self, fmt=None):
        data = self.lookup_table('Short % of Float')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def short_pct_of_float_date(self):
        data = self.lookup_table('Short % of Float', col_position=0)
        return Converter.extract_date(data)


    def shares_short_prior_month(self, fmt=None):
        data = self.lookup_table('Shares Short (prior month)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def forward_annual_dividend_rate(self, fmt=None):
        data = self.lookup_table('Forward Annual Dividend Rate')
        if fmt == "text":
            return data
        return data


    def forward_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Forward Annual Dividend Yield')
        if fmt == "text":
            return data
        return data


    def trailing_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        if fmt == "text":
            return data
        return data


    def trailing_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        if fmt == "text":
            return data
        return data


    def five_year_average_dividend_yield(self, fmt=None):
        data = self.lookup_table('5 Year Average Dividend Yield')
        if fmt == "text":
            return data
        return data


    def payout_ratio(self, fmt=None):
        data = self.lookup_table('Payout Ratio')
        if fmt == "text":
            return data
        return data


    def dividend_date(self, fmt=None):
        data = self.lookup_table('Dividend Date')
        if fmt == "text":
            return data
        return data


    def ex_dividend_date(self, fmt=None):
        data = self.lookup_table('Ex-Dividend Date')
        if fmt == "text":
            return data
        return data


    def last_split_factor_new_per_old(self, fmt=None):
        data = self.lookup_table('Last Split Factor (new per old)')
        if fmt == "text":
            return data
        return data


    def last_split_date(self, fmt=None):
        data = self.lookup_table('Last Split Date')
        if fmt == "text":
            return data
        return data


    def shares_short_value(self, fmt=None):
        data = self.lookup_table('Shares Short')
        if fmt=="text":
            return data
        return Converter.big_num_to_int(data)


    def short_pct_of_float_value(self, fmt=None):
        data = self.lookup_table("Short % of Float")
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def short_ratio_value(self, fmt=None):
        data = self.lookup_table("Short Ratio")
        if fmt == "text":
            return data
        return float(data)

    def to_dict(self, fmt=None):
        d = {
            "company": self.get_company_name(),
            "symbol": self.get_company_symbol(),
            "last_updated": self.last_update(),
            "valuation_measures":
                {
                    "market_cap": 301640000000,
                    "enterprise_value": 261140000000,
                    "trailing_pe": 27.20,
                    "forward_pe": 17.10,
                    "peg_ratio": 1.32,
                    "price-to-sales_ttm": 5.61,
                    "price-to-book_mrq": 3.96,
                    "enterprise_value-to-revenue_ttm": 4.88,
                    "enterprise_value-to-ebitda_ttm": 15.53
                },
            "financial_highlights":
                {
                    "fiscal_year":
                        {
                            "fiscal_year_ends": "Dec 30",
                            "most_recent_quarter_mrq": "Mar 31, 2013"
                        },
                    "profitability":
                        {
                            "profit_margin_ttm": 0.2092,
                            "operating_margin_ttm": 0.2530
                        },
                    "management_effectiveness":
                        {
                            "return_on_assets_ttm": 0.0973,
                            "return_on_equity_ttm": 0.1636
                        },
                    "income_statement":
                        {
                            "revenue_ttm": 53500000000,
                            "revenue_per_share_ttm": 162.86,
                            "qtrly_revenue_growth_yoy": 0.3120,
                            "gross_profit_ttm": 29540000000,
                            "ebitda_ttm": 16810000000,
                            "net_income_avl_to_common_ttm": 11220000000,
                            "diluted_eps_ttm": 33.42,
                            "qtrly_earnings_growth_yoy": 0.1580
                        },
                    "balance_sheet":
                        {
                            "total_cash_mrq": 50100000000,
                            "total_cash_per_share_mrq": 151.00,
                            "total_debt_mrq": 7380000000,
                            "total_debt-to-equity_mr": 9.77,
                            "current_ratio_mrq": 4.74,
                            "book_value_per_share_mrq": 228.01
                        },
                    "cash_flow_statement":
                        {
                            "operating_cash_flow_ttm": 16560000000,
                            "levered_free_cash_flow_ttm": 10990000000
                        }
                },
            "trading_information":
                {
                    "stock_price_history":
                        {
                            "beta": 1.16,
                            "52-week_change": 0.4805,
                            "sp500_52-week_change": 0.2874,
                            "52-week_high":
                                {
                                    "value": 919.98,
                                    "date": "may 16, 2013"
                                },
                            "52-week_low":
                                {
                                    "value": 556.52,
                                    "date": "jun 14, 2012"
                                },
                            "50-day_moving_average": 824.41,
                            "200-day_moving_average": 761.92
                        },
                    "share_statistics":
                        {
                            "avg_vol_3_month:": 2314660,
                            "avg_vol_10_day:": 2447740,
                            "shares_outstanding:": 331770000,
                            "float:": 270730000,
                            "pct_held_by_insiders:": 0.033,
                            "pct_held_by_institutions:": 0.8560,
                            "shares_short":
                                {
                                    "value": 4120000,
                                    "date": "apr 30, 2013"
                                },
                            "short_ratio":
                                {
                                    "value": 1.70,
                                    "date": "apr 30, 2013"
                                },
                            "short_pct_of_float":
                                {
                                    "value": 0.150,
                                    "date": "apr 30, 2013"
                                },
                            "shares_short_prior_month:": 3560000
                        },
                    "dividends & splits":
                        {
                            "forward_annual_dividend_rate:": None,
                            "forward_annual_dividend_yield:": None,
                            "trailing_annual_dividend_yield:": None,
                            "xtrailing_annual_dividend_yield:": None,
                            "5_year_average_dividend_yield:": None,
                            "payout_ratio:": None,
                            "dividend_date:": None,
                            "ex-dividend_date:": None,
                            "last_split_factor_new_per_old:": None,
                            "last_split_date:": None
                        }
                }
            }

        return d
