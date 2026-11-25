"""Data loading and saving module."""

from pathlib import Path
from typing import Optional
import pandas as pd

from .region import Region
from .strategies import DataStrategy, get_strategy

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"
TSV_PATH = DATA_DIR / "eu_life_expectancy_raw.tsv"
JSON_PATH = DATA_DIR / "eurostat_life_expect.zip"

def load_data(
    file_path: Path = TSV_PATH, strategy: Optional[DataStrategy] = None
) -> pd.DataFrame:
    """Loads raw data, picking the strategy from the file extension by default."""
    strategy = strategy or get_strategy(file_path)
    return strategy.load(file_path)


def save_data(df: pd.DataFrame, country: Region = Region.PT) -> None:
    """Saves cleaned dataframe to a CSV file without numerical index."""
    output_path = DATA_DIR / f"{country.value.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)
