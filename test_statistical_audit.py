"""
Regression tests for statistical methods used in AegisOps research.
Validates the exact two-sided binomial test for paired binary outcomes,
including the mandatory benchmark case b=4, c=2 -> p=0.6875.
"""
from __future__ import annotations

import math
import pytest
from research.statistical_tests import (
    mcnemar_exact_test,
    mcnemar_chi2_test,
    paired_difference_ci,
    wilson_score_ci,
)


def test_mcnemar_exact_b4_c2_equals_0_6875():
    """
    Mandatory test case: discordant counts b=4 and c=2.
    Under H0 (p=0.5, n=6):
        P(X=0) = 1/64
        P(X=1) = 6/64
        P(X=2) = 15/64
        P(X <= 2) = 22/64 = 0.34375
        Two-sided exact p-value = 2 * 0.34375 = 0.6875
    """
    p_val = mcnemar_exact_test(4, 2)
    assert math.isclose(p_val, 0.6875, rel_tol=1e-5), f"Expected 0.6875, got {p_val}"
    # Commutative: (2, 4) should yield the identical p-value
    assert math.isclose(mcnemar_exact_test(2, 4), 0.6875, rel_tol=1e-5)


def test_mcnemar_exact_boundary_and_symmetry():
    # Zero discordant pairs
    assert mcnemar_exact_test(0, 0) == 1.0
    # Symmetric discordant pairs
    assert math.isclose(mcnemar_exact_test(1, 1), 1.0, rel_tol=1e-5)
    assert math.isclose(mcnemar_exact_test(10, 10), 1.0, rel_tol=1e-5)
    # One-sided 0 discordant count
    # n=1, k=0 -> 2 * (0.5)^1 = 1.0
    assert math.isclose(mcnemar_exact_test(1, 0), 1.0, rel_tol=1e-5)
    # n=2, k=0 -> 2 * (0.5)^2 = 0.5
    assert math.isclose(mcnemar_exact_test(2, 0), 0.5, rel_tol=1e-5)


def test_mcnemar_exact_experiment_a_values():
    """
    Validates Experiment A discordant pairs:
    b=63 (LSTM detected, IsoForest missed), c=0 (IsoForest detected, LSTM missed).
    """
    p_val = mcnemar_exact_test(63, 0)
    expected_p = 2.0 * (0.5 ** 63)
    assert math.isclose(p_val, expected_p, rel_tol=1e-5)
    assert p_val < 1e-18


def test_mcnemar_chi2_continuity_correction():
    stat, p_val = mcnemar_chi2_test(63, 0, continuity=True)
    # ((63 - 1)^2) / 63 = 3844 / 63 = 61.01587...
    assert math.isclose(stat, (62 ** 2) / 63, rel_tol=1e-4)
    assert p_val < 1e-14


def test_wilson_score_ci():
    # 100% success on n=11 trials
    low, high = wilson_score_ci(11, 11)
    assert 0.70 < low < 0.75
    assert math.isclose(high, 1.0, rel_tol=1e-5)

    # 0% success on n=11 trials
    low, high = wilson_score_ci(0, 11)
    assert math.isclose(low, 0.0, rel_tol=1e-5)
    assert 0.25 < high < 0.30


def test_wilcoxon_signed_rank_exact_and_tied_ranks():
    from research.statistical_tests import wilcoxon_signed_rank_test

    # Ground-truth scenario recalls:
    # LSTM: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    # IsoForest: [0.40, 0.25, 0.85, 0.75, 0.40, 0.20]
    # Differences: [+0.60, +0.75, +0.15, +0.25, +0.60, +0.80]
    # Note: tied ranks at |+0.60| (ranks 3 and 4, mean rank 3.5).
    # All 6 differences strictly positive -> W- = 0.0, exact two-sided p = 2 * (1/2)^6 = 0.03125.
    lstm_recalls = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    iso_recalls = [0.40, 0.25, 0.85, 0.75, 0.40, 0.20]

    stat, p_val = wilcoxon_signed_rank_test(lstm_recalls, iso_recalls, alternative="two-sided")
    assert math.isclose(stat, 0.0, abs_tol=1e-6)
    assert math.isclose(p_val, 0.03125, rel_tol=1e-5)

    # One-sided test (greater): statistic = 21.0, p = 0.015625
    stat_g, p_val_g = wilcoxon_signed_rank_test(lstm_recalls, iso_recalls, alternative="greater")
    assert math.isclose(stat_g, 21.0, abs_tol=1e-6)
    assert math.isclose(p_val_g, 0.015625, rel_tol=1e-5)

