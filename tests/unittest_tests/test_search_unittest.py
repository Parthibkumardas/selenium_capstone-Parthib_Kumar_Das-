from pages.home_page import HomePage
from tests.unittest_tests.base_test import BaseTest
from utils.csv_reader import get_test_data

SEARCH_DATA = get_test_data("search_data")


class SearchUnittest(BaseTest):

    def test_search_results_heading_contains_search_term(self):
        results = HomePage(self.driver).search_for("iphone")
        self.assertIn("iphone", results.get_heading().lower())


def _build_search_test(row):
    def test(self):
        results = HomePage(self.driver).search_for(row["search_term"])
        if row["expected_result"] == "found":
            names = results.get_product_names()
            self.assertGreaterEqual(len(names), int(row["min_count"]), f"Got {names}")
            self.assertTrue(
                any(row["expected_product"].lower() in name.lower() for name in names),
                f"'{row['expected_product']}' not found in {names}",
            )
        else:
            self.assertTrue(results.has_no_results(), "Expected the 'no product' message")
            self.assertIn("no product that matches", results.get_no_result_message())
    return test


for _row in SEARCH_DATA:
    setattr(SearchUnittest, f"test_{_row['test_id'].lower()}_data_driven", _build_search_test(_row))
