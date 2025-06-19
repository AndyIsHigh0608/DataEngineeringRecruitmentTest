import re
import pandas as pd

def standardise_col_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [re.sub(r"[^a-zA-Z0-9]+", " ", col) for col in df.columns]
    df.columns = [re.sub(r"[\s+]", " ", col).
                  strip().
                  replace(" ", "_").
                  lower() 
                  for col in df.columns]
    return df

def standardise_str_values(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = [val.strip().upper() if isinstance(val, str) else val for val in df[col]]

    return df

def display_unique_object_values(df):
    object_cols = df.select_dtypes(include='object').columns

    for col in object_cols:
        unique_vals = df[col].unique()
        print(f"\nColumn: {col}")
        print(f"Unique values ({len(unique_vals)}):")
        print(unique_vals)