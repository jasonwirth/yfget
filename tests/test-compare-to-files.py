import unittest

from yfget import YahooFinanceGet


class TestCompareToFile(unittest.TestCase):
    def test_compare_AAPL_plain_text(self):
        import ast

        # Read our file with the dict stored as a text file
        with open("AAPL-dict.txt", "r") as f:
            dict_txt = f.read()

        # Convert our text to a python dict
        self.text_dict = ast.literal_eval(dict_txt)

        yfg = YahooFinanceGet()
        yfg.load_summary_from_html("AAPL-Key-Statistics.html")
        self.yfg_dict = yfg.to_dict(fmt="text")

        self.maxDiff = None

        self.assertDictEqual(self.text_dict,
                             self.yfg_dict)


    def test_compare_AAPL_numeric(self):
        import ast

        # Read our file with the dict stored as a text file
        with open("AAPL-dict-numeric.txt", "r") as f:
            dict_txt = f.read()

        # Convert our text to a python dict
        self.text_dict = ast.literal_eval(dict_txt)

        yfg = YahooFinanceGet()
        yfg.load_summary_from_html("AAPL-Key-Statistics.html")
        self.yfg_dict = yfg.to_dict()

        self.maxDiff = None

        self.assertDictEqual(self.text_dict,
                             self.yfg_dict)


    def test_compare_GOOG_plain_text(self):
        import ast

        # Read our file with the dict stored as a text file
        with open("GOOG-dict.txt", "r") as f:
            dict_txt = f.read()

        # Convert our text to a python dict
        self.text_dict = ast.literal_eval(dict_txt)

        yfg = YahooFinanceGet()
        yfg.load_summary_from_html("GOOG-Key-Statistics.html")
        self.yfg_dict = yfg.to_dict(fmt="text")

        self.maxDiff = None

        self.assertDictEqual(self.text_dict,
                             self.yfg_dict)


    def test_compare_GOOG_numeric(self):
        import ast

        # Read our file with the dict stored as a text file
        with open("GOOG-dict.txt", "r") as f:
            dict_txt = f.read()

        # Convert our text to a python dict
        self.text_dict = ast.literal_eval(dict_txt)

        yfg = YahooFinanceGet()
        yfg.load_summary_from_html("GOOG-Key-Statistics.html")
        self.yfg_dict = yfg.to_dict()

        self.maxDiff = None

        self.assertDictEqual(self.text_dict,
                             self.yfg_dict)
