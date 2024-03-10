# import pandas as pd
# import re
#
#
# def validate_data(df: pd.DataFrame) -> bool:
#     genes = {'IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR', 'CIC', 'MUC16', 'PIK3CA', 'NF1', 'PIK3R1', 'FUBP1', 'RB1',
#              'NOTCH1', 'BCOR', 'CSMD3', 'SMARCA4', 'GRIN2A', 'IDH2', 'FAT4', 'PDGFRA'}
#
#     checkers = []
#     columns = set(df.columns)
#
#     # проверка - все гены присутствуют в датасете
#     checkers.append(columns.intersection(genes) == genes)
#
#     # проверка - все гены правильно закодированы
#     for gene in genes:
#         checkers.append(set(df[gene].unique()).issubset({"MUTATED", "NOT_MUTATED"}))
#
#     checkers.append("Gender" in columns)
#     checkers.append(set(df["Gender"].unique()).issubset({"Male", "Female"}))
#
#     checkers.append("Age_at_diagnosis" in columns)
#
#     def checkup_years(item):
#         years_check = re.compile(r'\d+\s*years')
#         output = years_check.search(item)
#         return output is not None
#
#     def checkup_days(item):
#         days_check = re.compile(r'\d+\s*days')
#         output = days_check.search(item)
#         return output is not None
#
#     years_series = df[df['Age_at_diagnosis'].str.contains("years")]["Age_at_diagnosis"]
#     counts_raws = years_series.apply(lambda x: checkup_years(x)).sum()
#     checkers.append(counts_raws == len(years_series))
#
#     days_series = df[df['Age_at_diagnosis'].str.contains("days")]["Age_at_diagnosis"]
#     counts_raws = days_series.apply(lambda x: checkup_days(x)).sum()
#     checkers.append(counts_raws == len(days_series))
#
#     if all(checkers):
#         return True
#     else:
#         return False