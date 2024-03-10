import pandas as pd
import re


def process_age(entry: str) -> int:
    pattern_years = re.compile(r"(\d+)\s*years")
    match = pattern_years.search(entry)
    years = int(match.group(1))

    pattern_days = re.compile(r"(\d+)\s*days")
    match = pattern_days.search(entry)

    if match:
        days = int(match.group(1))
        return 365 * years + days

    return 365 * years


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    featues = ['IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR', 'CIC', 'MUC16', 'PIK3CA', 'NF1',
               'PIK3R1', 'FUBP1', 'RB1', 'NOTCH1', 'BCOR', 'CSMD3', 'SMARCA4',
               'GRIN2A', 'IDH2', 'FAT4', 'PDGFRA', 'Age_at_diagnosis', 'Gender']

    genes = featues[:-2]

    for gene in genes:
        df.loc[:, gene] = df[gene].apply(lambda x: 1 if x == "MUTATED" else 0)

    df.loc[:, "Gender"] = df["Gender"].apply(lambda x: 1 if x == "Male" else 0)

    df.loc[:, "Age_at_diagnosis"] = df["Age_at_diagnosis"].apply(process_age)

    return df

