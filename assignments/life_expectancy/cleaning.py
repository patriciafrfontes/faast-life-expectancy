"""Data cleaning module for EU life expectancy dataset."""

from pathlib import Path
import argparse
import pandas as pd

# Define caminhos relativos ao ficheiro de forma robusta
PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"


def clean_data(country: str = "PT") -> pd.DataFrame:
    """Loads, cleans, and saves life expectancy data for a given country."""
    # 1. Carregar os dados brutos (.tsv)
    raw_path = DATA_DIR / "eu_life_expectancy_raw.tsv"
    df = pd.read_csv(raw_path, sep="\t")

    # 2. Separar a primeira coluna (ex: 'unit,sex,age,geo\time') em 4 colunas
    first_col = df.columns[0]
    df[["unit", "sex", "age", "region"]] = df[first_col].str.split(",", expand=True)
    df = df.drop(columns=[first_col])

    # 3. Transformar de formato largo (wide) para comprido (long / unpivot)
    df_long = df.melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    # 4. Limpar e converter a coluna 'year' para int
    df_long["year"] = df_long["year"].str.extract(r"(\d+)")[0].astype(int)

    # 5. Limpar a coluna 'value', remover NaNs e converter para float
    # Extrai o número decimal (ex: de '80.2 b' retira '80.2')
    df_long["value"] = df_long["value"].str.extract(r"(\d+\.?\d*)")[0]
    df_long = df_long.dropna(subset=["value"])
    df_long["value"] = df_long["value"].astype(float)

    # 6. Filtrar pela região pretendida (por defeito 'PT')
    df_cleaned = df_long[df_long["region"] == country].reset_index(drop=True)

    # 7. Guardar o CSV limpo sem índice
    output_path = DATA_DIR / f"{country.lower()}_life_expectancy.csv"
    df_cleaned.to_csv(output_path, index=False)

    return df_cleaned


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Clean life expectancy data for a given country.")
    parser.add_argument(
        "--country",
        default="PT",
        help="Country code (e.g., 'PT' for Portugal)")
    args = parser.parse_args()
    clean_data(country=args.country)
