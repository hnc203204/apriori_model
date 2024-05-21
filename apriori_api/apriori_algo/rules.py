#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementations of algorithms related to association rules.
"""

import typing
import numbers
import itertools
from apriori_api.apriori_algo.itemsets import apriori_gen


class Rule:
    _decimals = 3

    def __init__(
        self,
        lhs: tuple,
        rhs: tuple,
        count_full: int = 0,
        count_lhs: int = 0,
        count_rhs: int = 0,
        num_transactions: int = 0,
    ):
        self.lhs = lhs  # antecedent
        self.rhs = rhs  # consequent
        self.count_full = count_full
        self.count_lhs = count_lhs
        self.count_rhs = count_rhs
        self.num_transactions = num_transactions

    @property
    def confidence(self):
        try:
            return self.count_full / self.count_lhs
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def support(self):
        try:
            return self.count_full / self.num_transactions
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def lift(self):
        try:
            observed_support = self.count_full / self.num_transactions
            prod_counts = self.count_lhs * self.count_rhs
            expected_support = prod_counts / self.num_transactions**2
            return observed_support / expected_support
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def conviction(self):
        try:
            eps = 10e-10
            prob_not_rhs = 1 - self.count_rhs / self.num_transactions
            prob_not_rhs_given_lhs = 1 - self.confidence
            return prob_not_rhs / (prob_not_rhs_given_lhs + eps)
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def rpf(self):
        try:
            return self.confidence * self.support
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def _pf(s):
        return "{" + ", ".join(str(k) for k in s) + "}"

    def __repr__(self):
        return "{} -> {}".format(self._pf(self.lhs), self._pf(self.rhs))

    def __str__(self):
        conf = "conf: {0:.3f}".format(self.confidence)
        supp = "supp: {0:.3f}".format(self.support)
        lift = "lift: {0:.3f}".format(self.lift)
        conv = "conv: {0:.3f}".format(self.conviction)

        return "{} -> {} ({}, {}, {}, {})".format(self._pf(self.lhs), self._pf(self.rhs), conf, supp, lift, conv)

    def __eq__(self, other):
        return (set(self.lhs) == set(other.lhs)) and (set(self.rhs) == set(other.rhs))

    def __hash__(self):
        return hash(frozenset(self.lhs + self.rhs))

    def __len__(self):
        return len(self.lhs + self.rhs)

def generate_rules_apriori(
    itemsets: typing.Dict[int, typing.Dict[tuple, int]],
    min_confidence: float,
    num_transactions: int,
    verbosity: int = 0,
):
    # Validate user inputs
    if not ((0 <= min_confidence <= 1) and isinstance(min_confidence, numbers.Number)):
        raise ValueError("`min_confidence` must be a number between 0 and 1.")

    if not ((num_transactions >= 0) and isinstance(num_transactions, numbers.Number)):
        raise ValueError("`num_transactions` must be a number greater than 0.")

    def count(itemset):
        return itemsets[len(itemset)][itemset]

    if verbosity > 0:
        print("Generating rules from itemsets.")

    for size in itemsets.keys():
        if size < 2:
            continue

        if verbosity > 0:
            print(" Generating rules of size {}.".format(size))

        for itemset in itemsets[size].keys():
            H_1 = []
            for removed in itertools.combinations(itemset, 1):
                remaining = set(itemset).difference(set(removed))
                lhs = tuple(sorted(remaining))

                conf = count(itemset) / count(lhs)
                if conf >= min_confidence:
                    yield Rule(
                        lhs,
                        removed,
                        count(itemset),
                        count(lhs),
                        count(removed),
                        num_transactions,
                    )

                    H_1.append(removed)

            if len(H_1) == 0:
                continue

            yield from _ap_genrules(itemset, H_1, itemsets, min_confidence, num_transactions)

    if verbosity > 0:
        print("Rule generation terminated.\n")


def _ap_genrules(
    itemset: tuple,
    H_m: typing.List[tuple],
    itemsets: typing.Dict[int, typing.Dict[tuple, int]],
    min_conf: float,
    num_transactions: int,
):


    def count(itemset):
        return itemsets[len(itemset)][itemset]
    if len(itemset) <= (len(H_m[0]) + 1):
        return
    H_m = list(apriori_gen(H_m))
    H_m_copy = H_m.copy()

    for h_m in H_m:
        lhs = tuple(sorted(set(itemset).difference(set(h_m))))
        if (count(itemset) / count(lhs)) >= min_conf:
            yield Rule(
                lhs,
                h_m,
                count(itemset),
                count(lhs),
                count(h_m),
                num_transactions,
            )
        else:
            H_m_copy.remove(h_m)

    if H_m_copy:
        yield from _ap_genrules(itemset, H_m_copy, itemsets, min_conf, num_transactions)
