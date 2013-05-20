__author__ = 'jasonwirth'


from lxml import etree, html

class Converter(object):
    @classmethod
    def string_to_int(cls, str_num):
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



class YahooFinanceGet(object):
    def __init__(self):
        self.data = None
        self.root = None

    def load_summary_from_html(self, html_file):
        with open(html_file, 'r') as f:
            html_string = f.read()
        self.root = html.fromstring(html_string)


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


    def get_table_data(self, column_name, occurance=0, exact=False):
        if exact:
            xpath = "//td[text()='%s']" % column_name
        else:
            xpath = "//td[contains(text(),'%s')]" % column_name
        title_td = self.root.xpath(xpath)[occurance]
        tr = title_td.getparent()
        row = tr.getchildren()
        return row[1].text_content()

    def get_market_cap(self, fmt='dec'):
        data = self.get_table_data('Market Cap')
        if fmt == 'dec':
            return Converter.string_to_int(data)
        if fmt == 'str':
            return data

    def get_enterprise_value(self):
        data = self.get_table_data('Enterprise Value')
        return Converter.string_to_int(data)

    def get_trailing_pe(self):
        data = self.get_table_data('Trailing P/E')
        return float(data)

    def get_forward_pe(self):
        data = self.get_table_data('Forward P/E')
        return float(data)

    def get_peg_ratio(self):
        data = self.get_table_data('PEG Ratio')
        return float(data)

    def get_price_to_sales_ttm(self):
        data = self.get_table_data('Price/Sales')
        return float(data)

    def get_price_to_book_mrq(self):
        data = self.get_table_data('Price/Book')
        return float(data)

    def get_enterprise_value_to_revenue_ttm(self):
        data = self.get_table_data('Enterprise Value/Revenue')
        return float(data)

    def get_enterprise_value_to_ebitda_ttm(self):
        data = self.get_table_data('Enterprise Value/EBITDA')
        return float(data)

    #===========================================================
    #  Financial highlights
    #-----------------------------------------------------------

    # ---- Fiscal Year -----------------------------------------

    def fiscal_year_ends(self):
        data = self.get_table_data('Fiscal Year Ends')
        return data

    def most_recent_quarter_mrq(self):
        data = self.get_table_data('Most Recent Quarter (mrq)')
        return data


    # ---- Profitability ----------------------------------------
    def profit_margin_ttm(self):
        data = self.get_table_data('Profit Margin')
        return Converter.percent_to_dec(data)

    def operating_margin_ttm(self):
        data = self.get_table_data('Operating Margin')
        return Converter.percent_to_dec(data)


    # ---- Management Effectiveness ----------------------------------------
    def return_on_assets_ttm(self):
        data = self.get_table_data('Return on Assets (ttm)')
        return Converter.percent_to_dec(data)


    def return_on_equity_ttm(self):
        data = self.get_table_data('Return on Equity (ttm)')
        return Converter.percent_to_dec(data)


    def revenue_ttm(self):
        data = self.get_table_data('Revenue (ttm)', occurance=1)
        return Converter.string_to_int(data)


    def revenue_per_share_ttm(self):
        data = self.get_table_data('Revenue Per Share (ttm)')
        return float(data)


    def qtrly_revenue_growth_yoy(self):
        data = self.get_table_data('Qtrly Revenue Growth (yoy)')
        return Converter.percent_to_dec(data)


    def gross_profit_ttm(self):
        data = self.get_table_data('Gross Profit (ttm)')
        return Converter.string_to_int(data)


    def ebitda_ttm(self):
        data = self.get_table_data('EBITDA (ttm)', occurance=1)
        return Converter.string_to_int(data)


    def net_income_avl_to_common_ttm(self):
        data = self.get_table_data('Net Income Avl to Common (ttm)')
        return Converter.string_to_int(data)


    def diluted_eps_ttm(self):
        data = self.get_table_data('Diluted EPS (ttm)')
        return float(data)


    def qtrly_earnings_growth_yoy(self):
        data = self.get_table_data('Qtrly Earnings Growth (yoy)')
        return Converter.percent_to_dec(data)


    def total_cash_mrq(self):
        data = self.get_table_data('Total Cash (mrq)')
        return Converter.string_to_int(data)


    def total_cash_per_share_mrq(self):
        data = self.get_table_data('Total Cash Per Share (mrq)')
        return Converter.string_to_int(data)


    def total_debt_mrq(self):
        data = self.get_table_data('Total Debt (mrq)')
        return Converter.string_to_int(data)


    def total_debt_to_equity_mrq(self):
        data = self.get_table_data('Total Debt/Equity (mrq)')
        return float(data)


    def current_ratio_mrq(self):
        data = self.get_table_data('Current Ratio (mrq)')
        return float(data)


    def book_value_per_share_mrq(self):
        data = self.get_table_data('Book Value Per Share (mrq)')
        return float(data)


    def operating_cash_flow_ttm(self):
        data = self.get_table_data('Operating Cash Flow (ttm)')
        return Converter.string_to_int(data)


    def levered_free_cash_flow_ttm(self):
        data = self.get_table_data('Levered Free Cash Flow (ttm)')
        return Converter.string_to_int(data)
