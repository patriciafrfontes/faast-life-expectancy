"""Tests for the loading and saving module."""

from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd

from life_expectancy.loading import load_data, save_data
from life_expectancy.region import Region

from . import FIXTURES_DIR


def test_load_data_uses_strategy() -> None:
    """Test load_data delegates loading to the given strategy."""
    dummy_df = pd.DataFrame({"col1": [1, 2]})
    mock_strategy = Mock()
    mock_strategy.load.return_value = dummy_df

    actual_df = load_data(Path("some_file"), mock_strategy)

    mock_strategy.load.assert_called_once_with(Path("some_file"))
    pd.testing.assert_frame_equal(actual_df, dummy_df)


def test_load_data_picks_strategy_from_extension(
    eurostat_life_expect_raw: pd.DataFrame,
) -> None:
    """Test load_data chooses the strategy when none is given."""
    actual_df = load_data(FIXTURES_DIR / "eurostat_life_expect.json")

    pd.testing.assert_frame_equal(actual_df, eurostat_life_expect_raw)


@patch("pandas.DataFrame.to_csv")
def test_save_data(mock_to_csv: Mock) -> None:
    """Test save_data calls to_csv without writing to disk."""
    dummy_df = pd.DataFrame({"col1": [1, 2]})

    save_data(dummy_df, country=Region.PT)

    mock_to_csv.assert_called_once()
    # Verifica que o argumento index=False foi passado
    _, kwargs = mock_to_csv.call_args
    assert kwargs.get("index") is False
