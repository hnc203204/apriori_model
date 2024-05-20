import itertools
from dataclasses import dataclass, field
from collections import defaultdict
import typing

@dataclass
class ItemsetCount:
    itemset_count: int
    members: field(default_factory=set)

class Transaction_maner:
    def __init__(self, transactions):
        self.indices_by = defaultdict(set)

        id = -1
        for id, transaction in enumerate(transactions):
            for item in transaction:
                self.indices_by[item].add(id)
        self._transactions_count = id + 1

    @property
    def items(self):
        return set(self.indices_by.keys())

    def __len__(self):
        return self._transactions_count

    def transaction_indices(self, transaction : typing.Iterable[typing.Hashable]):
        """trả về tập các index của transaction mà có "transaction" là subset"""

        transaction = set(transaction)
        item = transaction.pop()
        indices = self.indices_by[item]
        while transaction:
            item = transaction.pop()
            indices = indices.intersection(self.indices_by[item])
        return indices




    def transactions_indices_sc(self, transaction : typing.Iterable[typing.Hashable], minsup: float = 0):
        """check transaction là subset của transaction nào và thoả mãn minsup"""

        transaction = sorted(transaction, key = lambda item: len(self.indices_by[item]), reverse = True)


        item = transaction.pop()
        indices = self.indices_by[item]
        support = len(indices) / len(self)

        if support < minsup:
            return False, None

        while transaction:
            item = transaction.pop()
            indices = indices.intersection(self.indices_by[item])

            support = len(indices) / len(self)
            if support < minsup:
                return False, None

        return True, indices


def join_step(itemsets: typing.List[tuple]):

    i = 0
    while i < len(itemsets):
        skip = 1
        *itemset_first, last = itemsets[i]

        last_items = [last]
        last_items_append = last_items.append
        for j in range(i + 1, len(itemsets)):
            *itemset_second, last = itemsets[j]

            if itemset_first == itemset_second:
                last_items_append(last)
            else:
                break
            skip += 1
        i += skip
        itemset_first = tuple(itemset_first)
        for a, b in itertools.combinations(last_items, 2):
            yield itemset_first + (a, ) + (b, )

def prune_step():
    pass


