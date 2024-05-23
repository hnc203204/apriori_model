from mlxtend.frequent_patterns import apriori as mlxtend_apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd

def apriori_mlxtend(
        df_path : str,
        min_support: float = 0.001,
        min_confidence: float = 1.0
):
    df = pd.read_csv(df_path)
    df.drop("Unnamed: 0", axis=1, inplace=True)
    frequent_itemsets = mlxtend_apriori(df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return frequent_itemsets, rules