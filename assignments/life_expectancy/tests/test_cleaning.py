"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from life_expectancy.region import Region
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected: pd.DataFrame) -> None:
    """Run the `main` function and compare the output to the expected output"""
    df_actual = main(country=Region.PT)

    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )

    pd.testing.assert_frame_equal(
        df_actual, pt_life_expectancy_expected
    )


def test_region_countries() -> None:
    """Country regions include countries but exclude aggregate regions."""
    countries = Region.countries()

    assert len(countries) == 46
    assert Region.PT in countries
    assert Region.DE_TOT not in countries
    assert Region.FX not in countries
    assert Region.EU28 not in countries
    assert Region.EFTA not in countries
