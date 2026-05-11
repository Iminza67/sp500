import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sp500_analysis_ready.parquet"


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run preprocess.py first."
        )

    return pd.read_parquet(DATA_PATH)


if __name__ == "__main__":
    print(load_data().head())