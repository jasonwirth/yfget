import urllib
import urllib2

__author__ = 'jasonwirth'


from lxml import etree, html
import re



class Converter(object):
    @classmethod
    def big_num_to_int(cls, str_num):
        num = str_num[-1]
        value = float(str_num[:-1])
        if num =='M':
            value = value * 1e6
        elif num == 'B':
            value = value * 1e9
        elif num == "T":
            value = value * 1.12
        return int(value)


    @classmethod
    def percent_to_dec(cls, percent_str):
        value = percent_str[:-1]
        value = float(value)
        return value / 100


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


    def get_enterprise_value(self):
        data = self.lookup_table('Enterprise Value')
        return Converter.big_num_to_int(data)


    def get_trailing_pe(self):
        data = self.lookup_table('Trailing P/E')
        return float(data)


    def get_forward_pe(self):
        data = self.lookup_table('Forward P/E')
        return float(data)


    def get_peg_ratio(self):
        data = self.lookup_table('PEG Ratio')
        return float(data)


    def get_price_to_sales_ttm(self):
        data = self.lookup_table('Price/Sales')
        return float(data)


    def get_price_to_book_mrq(self):
        data = self.lookup_table('Price/Book')
        return float(data)


    def get_enterprise_value_to_revenue_ttm(self):
        data = self.lookup_table('Enterprise Value/Revenue')
        return float(data)


    def get_enterprise_value_to_ebitda_ttm(self):
        data = self.lookup_table('Enterprise Value/EBITDA')
        return float(data)


    #===========================================================
    #  Financial highlights
    #-----------------------------------------------------------

    # ---- Fiscal Year -----------------------------------------

    def fiscal_year_ends(self):
        data = self.lookup_table('Fiscal Year Ends')
        return data


    def most_recent_quarter_mrq(self):
        data = self.lookup_table('Most Recent Quarter (mrq)')
        return data


    # ---- Profitability ----------------------------------------

    def profit_margin_ttm(self):
        data = self.lookup_table('Profit Margin')
        return Converter.percent_to_dec(data)


    def operating_margin_ttm(self):
        data = self.lookup_table('Operating Margin')
        return Converter.percent_to_dec(data)


    # ---- Management Effectiveness ----------------------------------------

    def return_on_assets_ttm(self):
        data = self.lookup_table('Return on Assets (ttm)')
        return Converter.percent_to_dec(data)


    def return_on_equity_ttm(self):
        data = self.lookup_table('Return on Equity (ttm)')
        return Converter.percent_to_dec(data)


    def revenue_ttm(self):
        data = self.lookup_table('Revenue (ttm)', occurrence=1)
        return Converter.big_num_to_int(data)


    def revenue_per_share_ttm(self):
        data = self.lookup_table('Revenue Per Share (ttm)')
        return float(data)


    def qtrly_revenue_growth_yoy(self):
        data = self.lookup_table('Qtrly Revenue Growth (yoy)')
        return Converter.percent_to_dec(data)


    def gross_profit_ttm(self):
        data = self.lookup_table('Gross Profit (ttm)')
        return Converter.big_num_to_int(data)


    def ebitda_ttm(self):
        data = self.lookup_table('EBITDA (ttm)', occurrence=1)
        return Converter.big_num_to_int(data)


    def net_income_avl_to_common_ttm(self):
        data = self.lookup_table('Net Income Avl to Common (ttm)')
        return Converter.big_num_to_int(data)


    def diluted_eps_ttm(self):
        data = self.lookup_table('Diluted EPS (ttm)')
        return float(data)


    def qtrly_earnings_growth_yoy(self):
        data = self.lookup_table('Qtrly Earnings Growth (yoy)')
        return Converter.percent_to_dec(data)


    def total_cash_mrq(self):
        data = self.lookup_table('Total Cash (mrq)')
        return Converter.big_num_to_int(data)


    def total_cash_per_share_mrq(self):
        data = self.lookup_table('Total Cash Per Share (mrq)')
        return Converter.big_num_to_int(data)


    def total_debt_mrq(self):
        data = self.lookup_table('Total Debt (mrq)')
        return Converter.big_num_to_int(data)


    def total_debt_to_equity_mrq(self):
        data = self.lookup_table('Total Debt/Equity (mrq)')
        return float(data)


    def current_ratio_mrq(self):
        data = self.lookup_table('Current Ratio (mrq)')
        return float(data)


    def book_value_per_share_mrq(self):
        data = self.lookup_table('Book Value Per Share (mrq)')
        return float(data)


    def operating_cash_flow_ttm(self):
        data = self.lookup_table('Operating Cash Flow (ttm)')
        return Converter.big_num_to_int(data)


    def levered_free_cash_flow_ttm(self):
        data = self.lookup_table('Levered Free Cash Flow (ttm)')
        return Converter.big_num_to_int(data)


    def beta(self):
        value = self.lookup_table('Beta')
        return float(value)

    def fifty_two_week_change(self):
        value = self.lookup_table('52-Week Change')
        return Converter.percent_to_dec(value)

    def sp500_fifty_two_week_change(self):
        value = self.lookup_table('S&P500 52-Week Change')
        return Converter.percent_to_dec(value)


    def fifty_two_week_high_price(self):
        value = self.lookup_table('52-Week High')
        return float(value)


    def fifty_two_week_high_date(self):
        value = self.lookup_table('52-Week High', col_position=0)
        return Converter.extract_date(value)


    def fifty_two_week_low_price(self):
        value = self.lookup_table('52-Week Low')
        return float(value)


    def fifty_two_week_low_date(self):
        value = self.lookup_table('52-Week Low', col_position=0)
        return Converter.extract_date(value)


    def fifty_day_moving_average(self):
        value = self.lookup_table('50-Day Moving Average')
        return float(value)


    def two_hundred_day_moving_average(self):
        value = self.lookup_table('200-Day Moving Average')
        return float(value)


    def avg_vol_3_month(self):
        data = self.lookup_table('Avg Vol (3 month)')
        return Converter.remove_comma(data)


    def avg_vol_10_day(self):
        data = self.lookup_table('Avg Vol (10 day)')
        return Converter.remove_comma(data)


    def shares_outstanding(self):
        data = self.lookup_table('Shares Outstanding')
        return Converter.big_num_to_int(data)


    def float(self):
        data = self.lookup_table('Float')
        return Converter.big_num_to_int(data)


    def pct_held_by_insiders(self):
        data = self.lookup_table("Held by Insiders")
        return Converter.percent_to_dec(data)


    def pct_held_by_institutions(self):
        data = self.lookup_table('Held by Institutions')
        return Converter.percent_to_dec(data)


    def shares_short_value(self):
        data = self.lookup_table('Shares Short')
        return Converter.big_num_to_int(data)


    def shares_short_date(self):
        data = self.lookup_table('Shares Short', col_position=0)
        return Converter.extract_date(data)


    def short_ratio_value(self):
        data = self.lookup_table('Short Ratio')
        return float(data)


    def short_ratio_date(self):
        data = self.lookup_table('Short Ratio', col_position=0)
        return Converter.extract_date(data)


    def short_pct_of_float_value(self):
        data = self.lookup_table('Short % of Float')
        return Converter.percent_to_dec(data)


    def short_pct_of_float_date(self):
        data = self.lookup_table('Short % of Float', col_position=0)
        return Converter.extract_date(data)


    def shares_short_prior_month(self):
        data = self.lookup_table('Shares Short (prior month)')
        return Converter.big_num_to_int(data)


    def forward_annual_dividend_rate(self):
        data = self.lookup_table('Forward Annual Dividend Rate')
        return data


    def forward_annual_dividend_yield(self):
        data = self.lookup_table('Forward Annual Dividend Yield')
        return data


    def trailing_annual_dividend_yield(self):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        return data


    def trailing_annual_dividend_yield(self):
        data = self.lookup_table('Trailing Annual Dividend Yield')
        return data


    def five_year_average_dividend_yield(self):
        data = self.lookup_table('5 Year Average Dividend Yield')
        return data


    def payout_ratio(self):
        data = self.lookup_table('Payout Ratio')
        return data


    def dividend_date(self):
        data = self.lookup_table('Dividend Date')
        return data


    def ex_dividend_date(self):
        data = self.lookup_table('Ex-Dividend Date')
        return data


    def last_split_factor_new_per_old(self):
        data = self.lookup_table('Last Split Factor (new per old)')
        return data


    def last_split_date(self):
        data = self.lookup_table('Last Split Date')
        return data


