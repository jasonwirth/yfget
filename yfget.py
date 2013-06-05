import urllib
import urllib2

__author__ = 'jasonwirth'


from lxml import etree, html
import re



class Converter(object):
    @classmethod
    def big_num_to_int(cls, str_num, decimals=2):
        # Can be NA
        if str_num == "N/A":
            return 0.0

        # Can be 0.00
        if str_num == "0.00":
            return float(str_num)

        # Can be big int
        letter = str_num[-1]
        if not letter.isalpha():
            return float(str_num)
        num = str_num[:-1]
        left, right = num.split('.')
        left, right = int(left), int(right)
        if letter =='M':
            value = left * 1e6 + right * 1e4 
        elif letter == 'B':
            value = left * 1e9 + right * 1e7
        elif letter == "T":
            value = left * 1e12 + right * 1e9
        else:
            raise Exception("Value: %s doesnt fit" % str_num)
        return int(value)


    @classmethod
    def percent_to_dec(cls, percent_str, decimals=4):
        value = percent_str[:-1]
        value = float(value)
        return round(value / 100, decimals)


    @classmethod
    def extract_date(cls, text):
        # TODO: Make this return a datetime object
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


    def market_cap(self, fmt=None):
        data = self.lookup_table('Market Cap')
        if fmt == 'text':
            return data
        return Converter.big_num_to_int(data)



    def get_enterprise_value(self, fmt=None):
        data = self.lookup_table('Enterprise Value')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def trailing_pe(self, fmt=None):
        data = self.lookup_table('Trailing P/E')
        if fmt == "text":
            return data
        return float(data)


    def forward_pe(self, fmt=None):
        data = self.lookup_table('Forward P/E')
        if fmt == "text":
            return data
        return float(data)


    def peg_ratio(self, fmt=None):
        data = self.lookup_table('PEG Ratio')
        if fmt == "text":
            return data
        return float(data)


    def price_to_sales_ttm(self, fmt=None):
        data = self.lookup_table('Price/Sales')
        if fmt == "text":
            return data
        return float(data)


    def price_to_book_mrq(self, fmt=None):
        data = self.lookup_table('Price/Book')
        if fmt == "text":
            return data
        return float(data)


    def enterprise_value_to_revenue_ttm(self, fmt=None):
        data = self.lookup_table('Enterprise Value/Revenue')
        if fmt == "text":
            return data
        return float(data)


    def enterprise_value_to_ebitda_ttm(self, fmt=None):
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
        return Converter.big_num_to_int(data)


    def current_ratio_mrq(self, fmt=None):
        data = self.lookup_table('Current Ratio (mrq)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


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


    def fifty_two_week_high_date(self, fmt=None):
        data = self.lookup_table('52-Week High', col_position=0)
        str_date = Converter.extract_date(data)
        if fmt=="text":
            return str_date
        else:
            # TODO: Return a datetime object
            return str_date


    def fifty_two_week_low_price(self, fmt=None):
        data = self.lookup_table('52-Week Low')
        if fmt == "text":
            return data
        return float(data)


    def fifty_two_week_low_date(self, fmt=None):
        data = self.lookup_table('52-Week Low', col_position=0)
        str_date = Converter.extract_date(data)
        if fmt == "text":
            return str_date
        else:
            # TODO: Return a datetime object
            return str_date


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


    def shares_short_date(self, fmt=None):
        data = self.lookup_table('Shares Short', col_position=0)
        str_date = Converter.extract_date(data)
        if fmt == "text":
            return str_date
            # TODO: Return a datetime object
        else:
            return str_date


    # def short_ratio_data(self, fmt=None):
    #     data = self.lookup_table('Short Ratio')
    #     if fmt == "text":
    #         return data
    #     return float(data)


    def short_ratio_date(self, fmt=None):
        data = self.lookup_table('Short Ratio', col_position=0)
        str_date = Converter.extract_date(data)
        if fmt == "text":
            return str_date
            # TODO: Return a datetime object
        else:
            return str_date


    # def short_pct_of_float_data(self, fmt=None):
    #     data = self.lookup_table('Short % of Float')
    #     if fmt == "text":
    #         return data
    #     return Converter.percent_to_dec(data)


    def short_pct_of_float_date(self, fmt=None):
        data = self.lookup_table('Short % of Float', col_position=0)
        str_date = Converter.extract_date(data)
        if fmt == "text":
            return str_date
            # TODO: Return a datetime object
        else:
            return str_date


    def shares_short_prior_month(self, fmt=None):
        data = self.lookup_table('Shares Short (prior month)')
        if fmt == "text":
            return data
        return Converter.big_num_to_int(data)


    def forward_annual_dividend_rate(self, fmt=None):
        data = self.lookup_table('Forward Annual Dividend Rate')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def forward_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Forward Annual Dividend Yield')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def trailing_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def trailing_annual_dividend_yield(self, fmt=None):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


    def five_year_average_dividend_yield(self, fmt=None):
        data = self.lookup_table('5 Year Average Dividend Yield')
        if fmt == "text":
            return data
        return data


    def payout_ratio(self, fmt=None):
        data = self.lookup_table('Payout Ratio')
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


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


    def last_update(self):
        # elements = self.root.xpath('//*[@id="yfs_t53_goog"]')
        # elements = self.root.xpath('//span[@class="time_rtq"]/span')
        elements = self.root.xpath('//*[@id="yfs_market_time"]')
        text = elements[0].text_content()
        return text.split(" - ")[0]





    #============================
    def to_dict(self, fmt=None):
        d = {
            "company": self.get_company_name(),
            "symbol": self.get_company_symbol(),
            "last_updated": self.last_update(),
            "valuation_measures":
                {
                    "market_cap": self.market_cap(fmt=fmt),
                    "enterprise_value": self.get_enterprise_value(fmt=fmt),
                    "trailing_pe": self.trailing_pe(fmt=fmt),
                    "forward_pe": self.forward_pe(fmt=fmt),
                    "peg_ratio": self.peg_ratio(fmt=fmt),
                    "price-to-sales_ttm": self.price_to_sales_ttm(fmt=fmt),
                    "price-to-book_mrq": self.price_to_book_mrq(fmt=fmt),
                    "enterprise_value-to-revenue_ttm": self.enterprise_value_to_revenue_ttm(fmt=fmt),
                    "enterprise_value-to-ebitda_ttm": self.enterprise_value_to_ebitda_ttm(fmt=fmt)
                },
            "financial_highlights":
                {
                    "fiscal_year":
                        {
                            "fiscal_year_ends": self.fiscal_year_ends(fmt=fmt),
                            "most_recent_quarter_mrq": self.most_recent_quarter_mrq(fmt=fmt)
                        },
                    "profitability":
                        {
                            "profit_margin_ttm": self.profit_margin_ttm(fmt=fmt),
                            "operating_margin_ttm": self.operating_margin_ttm(fmt=fmt)
                        },
                    "management_effectiveness":
                        {
                            "return_on_assets_ttm": self.return_on_assets_ttm(fmt=fmt),
                            "return_on_equity_ttm": self.return_on_equity_ttm(fmt=fmt)
                        },
                    "income_statement":
                        {
                            "revenue_ttm": self.revenue_ttm(fmt=fmt),
                            "revenue_per_share_ttm": self.revenue_per_share_ttm(fmt=fmt),
                            "qtrly_revenue_growth_yoy": self.qtrly_revenue_growth_yoy(fmt=fmt),
                            "gross_profit_ttm": self.gross_profit_ttm(fmt=fmt),
                            "ebitda_ttm": self.ebitda_ttm(fmt=fmt),
                            "net_income_avl_to_common_ttm": self.net_income_avl_to_common_ttm(fmt=fmt),
                            "diluted_eps_ttm": self.diluted_eps_ttm(fmt=fmt),
                            "qtrly_earnings_growth_yoy": self.qtrly_earnings_growth_yoy(fmt=fmt)
                        },
                    "balance_sheet":
                        {
                            "total_cash_mrq": self.total_cash_mrq(fmt=fmt),
                            "total_cash_per_share_mrq": self.total_cash_per_share_mrq(fmt=fmt),
                            "total_debt_mrq": self.total_debt_mrq(fmt=fmt),
                            "total_debt_to_equity_mrq": self.total_debt_to_equity_mrq(fmt=fmt),
                            "current_ratio_mrq": self.current_ratio_mrq(fmt=fmt),
                            "book_value_per_share_mrq": self.book_value_per_share_mrq(fmt=fmt)
                        },
                    "cash_flow_statement":
                        {
                            "operating_cash_flow_ttm": self.operating_cash_flow_ttm(fmt=fmt),
                            "levered_free_cash_flow_ttm": self.levered_free_cash_flow_ttm(fmt=fmt)
                        }
                },
            "trading_information":
                {
                    "stock_price_history":
                        {
                            "beta": self.beta(fmt=fmt),
                            "52-week_change": self.fifty_two_week_change(fmt=fmt),
                            "sp500_52-week_change": self.sp500_fifty_two_week_change(fmt=fmt),
                            "52-week_high":
                                {
                                    "value": self.fifty_two_week_high_price(fmt=fmt),
                                    "date": self.fifty_two_week_high_date(fmt=fmt)
                                },
                            "52-week_low":
                                {
                                    "value": self.fifty_two_week_low_price(fmt=fmt),
                                    "date": self.fifty_two_week_low_date(fmt=fmt)
                                },
                            "50-day_moving_average": self.fifty_day_moving_average(fmt=fmt),
                            "200-day_moving_average": self.two_hundred_day_moving_average(fmt=fmt)
                        },
                    "share_statistics":
                        {
                            "avg_vol_3_month:": self.avg_vol_3_month(fmt=fmt),
                            "avg_vol_10_day:": self.avg_vol_10_day(fmt=fmt),
                            "shares_outstanding:": self.shares_outstanding(fmt=fmt),
                            "float:": self.float(fmt=fmt),
                            "pct_held_by_insiders:": self.pct_held_by_insiders(fmt=fmt),
                            "pct_held_by_institutions:": self.pct_held_by_institutions(fmt=fmt),
                            "shares_short":
                                {
                                    "value": self.shares_short_value(fmt=fmt),
                                    "date": self.shares_short_date(fmt=fmt)
                                },
                            "short_ratio":
                                {
                                    "value": self.short_ratio_value(fmt=fmt),
                                    "date": self.short_ratio_date(fmt=fmt)
                                },
                            "short_pct_of_float":
                                {
                                    "value": self.short_pct_of_float_value(fmt=fmt),
                                    "date": self.short_pct_of_float_date(fmt=fmt)
                                },
                            "shares_short_prior_month:": self.shares_short_prior_month(fmt=fmt)
                        },
                    "dividends & splits":
                        {
                            "forward_annual_dividend_rate:": self.forward_annual_dividend_rate(fmt=fmt),
                            "forward_annual_dividend_yield:": self.forward_annual_dividend_yield(fmt=fmt),
                            "trailing_annual_dividend_yield:": self.trailing_annual_dividend_yield(fmt=fmt),
                            "trailing_annual_dividend_yield_pct:": self.trailing_annual_dividend_yield_pct(fmt=fmt),
                            "5_year_average_dividend_yield:": self.five_year_average_dividend_yield(fmt=fmt),
                            "payout_ratio:": self.payout_ratio(fmt=fmt),
                            "dividend_date:": self.dividend_date(fmt=fmt),
                            "ex-dividend_date:": self.ex_dividend_date(fmt=fmt),
                            "last_split_factor_new_per_old:": self.last_split_factor_new_per_old(fmt=fmt),
                            "last_split_date:": self.last_split_date(fmt=fmt)
                        }
                }
        }

        return d


    def trailing_annual_dividend_yield_pct(self, fmt=None):
        data = self.lookup_table("Trailing Annual Dividend Yield", occurrence=1)
        if fmt == "text":
            return data
        return Converter.percent_to_dec(data)


