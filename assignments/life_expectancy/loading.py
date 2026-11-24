"""Data loading and saving module."""

from pathlib import Path
import pandas as pd

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"

def load_data() -> pd.DataFrame:
    """Loads raw life expectancy data from the data directory."""
    raw_path = DATA_DIR / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(raw_path, sep="\t")


def save_data(df: pd.DataFrame, country: str = "PT") -> None:
    """Saves cleaned dataframe to a CSV file without numerical index."""
    output_path = DATA_DIR / f"{country.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)
