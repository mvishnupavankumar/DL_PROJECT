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
