

import typing
from apriori_api.apriori_algo.itemsets import itemsets_from_transactions
from apriori_api.apriori_algo.rules import generate_rules_apriori

def apriori(
    transactions: typing.Iterable[typing.Union[set, tuple, list]],
    min_support: float = 0.5,
    min_confidence: float = 0.5,
    max_length: int = 8,
    verbosity: int = 0,
    output_transaction_ids: bool = False,
):
    itemsets, num_trans = itemsets_from_transactions(
        transactions,
        min_support,
        max_length,
        verbosity,
        output_transaction_ids=True,
    )

    itemsets_raw = {
        length: {item: counter.itemset_count for (item, counter) in itemsets.items()}
        for (length, itemsets) in itemsets.items()
    }
    rules = generate_rules_apriori(itemsets_raw, min_confidence, num_trans, verbosity)

    if output_transaction_ids:
        return itemsets, list(rules)

    return itemsets_raw, list(rules)

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