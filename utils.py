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