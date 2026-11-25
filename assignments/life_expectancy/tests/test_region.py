"""Tests for the Region enum."""

from life_expectancy.region import Region


def test_region_countries() -> None:
    """Country regions include countries but exclude aggregate regions."""
    countries = Region.countries()

    assert len(countries) == 46
    assert Region.PT in countries
    assert Region.DE_TOT not in countries
    assert Region.FX not in countries
    assert Region.EU28 not in countries
    assert Region.EFTA not in countries
