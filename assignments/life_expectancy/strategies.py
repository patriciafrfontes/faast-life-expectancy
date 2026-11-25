"""Strategies to load and clean life expectancy data in different formats."""

from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

from .region import Region


class DataStrategy(ABC):
    """Interface for loading and cleaning data of a specific format."""

    @abstractmethod
    def load(self, file_path: Path) -> pd.DataFrame:
        """Loads raw data from the given file."""

    @abstractmethod
    def clean(self, df: pd.DataFrame, country: Region) -> pd.DataFrame:
        """Cleans raw data and filters it by country."""


class TSVStrategy(DataStrategy):
    """Strategy for the wide TSV format (one column per year)."""

    def load(self, file_path: Path) -> pd.DataFrame:
        return pd.read_csv(file_path, sep="\t")

    def clean(self, df: pd.DataFrame, country: Region) -> pd.DataFrame:
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

        return df_long[df_long["region"] == country.value].reset_index(drop=True)


class JSONStrategy(DataStrategy):
    """Strategy for the long JSON format (one row per year)."""

    def load(self, file_path: Path) -> pd.DataFrame:
        # compression is inferred from the extension, so zipped JSON also works
        return pd.read_json(file_path)

    def clean(self, df: pd.DataFrame, country: Region) -> pd.DataFrame:
        df_clean = df.rename(
            columns={"country": "region", "life_expectancy": "value"}
        )[["unit", "sex", "age", "region", "year", "value"]]
        df_clean = df_clean.dropna(subset=["value"])

        return df_clean[df_clean["region"] == country.value].reset_index(drop=True)


# Eurostat ships the JSON data zipped, so .zip maps to the JSON strategy
STRATEGIES_BY_EXTENSION = {
    ".tsv": TSVStrategy,
    ".json": JSONStrategy,
    ".zip": JSONStrategy,
}


def get_strategy(file_path: Path) -> DataStrategy:
    """Returns the strategy that matches the file extension."""
    try:
        return STRATEGIES_BY_EXTENSION[file_path.suffix.lower()]()
    except KeyError as error:
        raise ValueError(f"Unsupported file format: {file_path.suffix}") from error
