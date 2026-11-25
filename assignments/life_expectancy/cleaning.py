"""Data cleaning module for EU life expectancy dataset."""

import argparse
from pathlib import Path
from typing import Optional
import pandas as pd

from .loading import JSON_PATH, TSV_PATH, load_data, save_data
from .region import Region
from .strategies import DataStrategy, TSVStrategy, get_strategy

FORMATS = {
    "tsv": TSV_PATH,
    "json": JSON_PATH,
}

def clean_data(
    df: pd.DataFrame,
    country: Region = Region.PT,
    strategy: Optional[DataStrategy] = None,
) -> pd.DataFrame:
    """Cleans the life expectancy data for a given country."""
    strategy = strategy or TSVStrategy()
    return strategy.clean(df, country)

def main(country: Region = Region.PT, file_path: Path = TSV_PATH) -> pd.DataFrame:
    """Main function to load, clean, and save life expectancy data."""
    strategy = get_strategy(file_path)
    df_raw = load_data(file_path, strategy)
    df_cleaned = clean_data(df_raw, country=country, strategy=strategy)
    save_data(df_cleaned, country=country)
    return df_cleaned

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Clean EU life expectancy data.")
    parser.add_argument(
        "--country",
        choices=[region.value for region in Region],
        default=Region.PT.value,
        help="Country code (e.g., 'PT' for Portugal)")
    parser.add_argument(
        "--format",
        choices=list(FORMATS),
        default="tsv",
        help="Format of the raw data file")
    args = parser.parse_args()
    main(country=Region(args.country), file_path=FORMATS[args.format])
