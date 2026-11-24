"""Tests for the loading and saving module."""

from unittest.mock import Mock, patch
import pandas as pd

from life_expectancy.loading import load_data, save_data


@patch("life_expectancy.loading.pd.read_csv")
def test_load_data(mock_read_csv: Mock) -> None:
    """Test load_data reads data from raw file using a mock."""
    dummy_df = pd.DataFrame({"col1": [1, 2]})
    mock_read_csv.return_value = dummy_df

    actual_df = load_data()

    mock_read_csv.assert_called_once()
    pd.testing.assert_frame_equal(actual_df, dummy_df)


@patch("pandas.DataFrame.to_csv")
def test_save_data(mock_to_csv: Mock) -> None:
    """Test save_data calls to_csv without writing to disk."""
    dummy_df = pd.DataFrame({"col1": [1, 2]})

    save_data(dummy_df, country="PT")

    mock_to_csv.assert_called_once()
    # Verifica que o argumento index=False foi passado
    _, kwargs = mock_to_csv.call_args
    assert kwargs.get("index") is False
