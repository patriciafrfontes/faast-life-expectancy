"""Data cleaning module for EU life expectancy dataset."""

import argparse
import pandas as pd

from life_expectancy.loading import load_data, save_data

def clean_data(df: pd.DataFrame, country: str = "PT") -> pd.DataFrame:
    """Cleans the life expectancy data for a given country."""
    first_col = df.columns[0]
    df_split = df.copy()
    df_split[["unit", "sex", "age", "region"]] = (
        df_split[first_col].str.split(",", expand=True)
    )
    df_split = df_split.drop(columns=[first_col])

    df_long = df_split.melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    df_long["year"] = df_long["year"].str.extract(r"(\d+)")[0].astype(int)
    df_long["value"] = df_long["value"].str.extract(r"(\d+\.?\d*)")[0]
    df_long = df_long.dropna(subset=["value"])
    df_long["value"] = df_long["value"].astype(float)

    return df_long[df_long["region"] == country].reset_index(drop=True)

def main(country: str = "PT") -> pd.DataFrame:
    """Main function to load, clean, and save life expectancy data."""
    df_raw = load_data()
    df_cleaned = clean_data(df_raw, country=country)
    save_data(df_cleaned, country=country)
    return df_cleaned

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Clean EU life expectancy data.")
    parser.add_argument(
        "--country",
        default="PT",
        help="Country code (e.g., 'PT' for Portugal)")
    args = parser.parse_args()
    main(country=args.country)
