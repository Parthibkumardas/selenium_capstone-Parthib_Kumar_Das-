import pytest

from pages.home_page import HomePage
from utils.csv_reader import get_test_data

SEARCH_DATA = get_test_data("search_data")


@pytest.mark.regression
@pytest.mark.parametrize("row", SEARCH_DATA, ids=[row["test_id"] for row in SEARCH_DATA])
def test_search_data_driven(driver, row):
    results = HomePage(driver).search_for(row["search_term"])

    if row["expected_result"] == "found":
        names = results.get_product_names()
        assert len(names) >= int(row["min_count"]), f"Expected >= {row['min_count']} products, got {names}"
        assert any(row["expected_product"].lower() in name.lower() for name in names), (
            f"'{row['expected_product']}' not found in {names}"
        )
    else:
        assert results.has_no_results(), "Expected the 'no product' message"
        assert "no product that matches" in results.get_no_result_message()


@pytest.mark.smoke
def test_search_results_heading_contains_search_term(driver):
    results = HomePage(driver).search_for("iphone")
    assert "iphone" in results.get_heading().lower()
