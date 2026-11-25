"""Tests for the data format strategies."""

from pathlib import Path
import pandas as pd
import pytest

from life_expectancy.region import Region
from life_expectancy.strategies import JSONStrategy, TSVStrategy, get_strategy

from . import FIXTURES_DIR


def test_tsv_strategy_load(eu_life_expectancy_raw: pd.DataFrame) -> None:
    """TSVStrategy loads a tab-separated file."""
    actual_df = TSVStrategy().load(FIXTURES_DIR / "eu_life_expectancy_raw.tsv")

    pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_raw)


def test_tsv_strategy_clean(
    eu_life_expectancy_raw: pd.DataFrame,
    eu_life_expectancy_expected: pd.DataFrame,
) -> None:
    """TSVStrategy cleans wide TSV data into the expected long format."""
    actual_df = TSVStrategy().clean(eu_life_expectancy_raw, Region.PT)

    pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_expected)


def test_json_strategy_load(eurostat_life_expect_raw: pd.DataFrame) -> None:
    """JSONStrategy loads a JSON file."""
    actual_df = JSONStrategy().load(FIXTURES_DIR / "eurostat_life_expect.json")

    pd.testing.assert_frame_equal(actual_df, eurostat_life_expect_raw)


def test_json_strategy_load_zip(eurostat_life_expect_raw: pd.DataFrame) -> None:
    """JSONStrategy loads a zipped JSON file."""
    actual_df = JSONStrategy().load(FIXTURES_DIR / "eurostat_life_expect.zip")

    pd.testing.assert_frame_equal(actual_df, eurostat_life_expect_raw)


@pytest.mark.parametrize(
    "file_name, expected_strategy",
    [
        ("data.tsv", TSVStrategy),
        ("data.json", JSONStrategy),
        ("data.zip", JSONStrategy),
        ("DATA.JSON", JSONStrategy),
    ],
)
def test_get_strategy(file_name: str, expected_strategy: type) -> None:
    """get_strategy picks the strategy from the file extension."""
    assert isinstance(get_strategy(Path(file_name)), expected_strategy)


def test_get_strategy_unsupported_format() -> None:
    """get_strategy raises a clear error for unknown extensions."""
    with pytest.raises(ValueError, match="Unsupported file format"):
        get_strategy(Path("data.xlsx"))


def test_json_strategy_clean(
    eurostat_life_expect_raw: pd.DataFrame,
    eu_life_expectancy_expected: pd.DataFrame,
) -> None:
    """JSONStrategy output matches the TSV pipeline output."""
    actual_df = JSONStrategy().clean(eurostat_life_expect_raw, Region.PT)

    pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_expected)
