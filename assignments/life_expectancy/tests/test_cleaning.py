"""Tests for the cleaning module."""

from unittest.mock import Mock, patch
import pandas as pd

from life_expectancy.cleaning import clean_data, main


def test_clean_data(
    eu_life_expectancy_raw: pd.DataFrame,
    eu_life_expectancy_expected: pd.DataFrame,
) -> None:
    """Test clean_data function with sample input and expected output fixtures."""
    df_actual = clean_data(eu_life_expectancy_raw, country="PT")

    pd.testing.assert_frame_equal(df_actual, eu_life_expectancy_expected)


@patch("life_expectancy.cleaning.save_data")
@patch("life_expectancy.cleaning.load_data")
def test_main(
    mock_load_data: Mock,
    mock_save_data: Mock,
    eu_life_expectancy_raw: pd.DataFrame,
    eu_life_expectancy_expected: pd.DataFrame,
) -> None:
    """Test main pipeline orchestrates load, clean, and save using mocks."""
    mock_load_data.return_value = eu_life_expectancy_raw

    actual_df = main(country="PT")

    mock_load_data.assert_called_once()
    mock_save_data.assert_called_once()
    pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_expected)
