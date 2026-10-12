"""
AegisOps — Verified Statistical Testing Library
Provides verified, exact statistical tests for paired binary outcomes, confidence intervals,
and contingency analyses adhering to academic research standards.
"""
from __future__ import annotations

import math
from typing import Tuple
import scipy.stats as stats


def mcnemar_exact_test(b: int, c: int) -> float:
    """
    Computes the exact two-sided binomial test p-value for McNemar's paired test
    based on discordant pairs b and c.

    Under H0, the discordant pairs (b + c) are equally likely to fall in either category (p = 0.5).
    The exact two-sided p-value is calculated using the binomial distribution.

    Special test case:
        b = 4, c = 2 -> p = 0.6875
    """
    if b < 0 or c < 0:
        raise ValueError("Discordant counts b and c must be non-negative integers.")
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    res = stats.binomtest(k, n, p=0.5, alternative="two-sided")
    return float(res.pvalue)


def mcnemar_chi2_test(b: int, c: int, continuity: bool = True) -> Tuple[float, float]:
    """
    Computes McNemar's asymptotic chi-squared statistic and p-value.
    With Edwards continuity correction: chi2 = (|b - c| - 1)^2 / (b + c)
    """
    n = b + c
    if n == 0:
        return 0.0, 1.0
    if continuity:
        num = (abs(b - c) - 1.0) ** 2
    else:
        num = float((b - c) ** 2)
    stat = num / n
    p_val = float(stats.chi2.sf(stat, df=1))
    return stat, p_val


def paired_difference_ci(
    b: int, c: int, n: int, confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    Computes the paired difference in proportions (p1 - p2 = (b - c) / n)
    and its asymptotic Wald confidence interval.
    """
    if n <= 0:
        raise ValueError("Total sample count n must be positive.")
    diff = (b - c) / n
    z = stats.norm.ppf(1.0 - (1.0 - confidence) / 2.0)
    variance = ((b + c) - ((b - c) ** 2 / n)) / (n ** 2)
    se = math.sqrt(max(0.0, variance))
    ci_low = diff - z * se
    ci_high = diff + z * se
    return diff, max(-1.0, ci_low), min(1.0, ci_high)


def wilson_score_ci(
    k: int, n: int, confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Computes the Wilson score interval for a binomial proportion k/n.
    Particularly robust for boundary proportions (k=0 or k=n).
    """
    if n <= 0:
        raise ValueError("Sample size n must be positive.")
    if k < 0 or k > n:
        raise ValueError(f"Success count k={k} must be in [0, n={n}].")
    p = k / n
    z = stats.norm.ppf(1.0 - (1.0 - confidence) / 2.0)
    denom = 1.0 + (z ** 2) / n
    center = (p + (z ** 2) / (2.0 * n)) / denom
    margin = (z * math.sqrt(p * (1.0 - p) / n + (z ** 2) / (4.0 * (n ** 2)))) / denom
    return max(0.0, center - margin), min(1.0, center + margin)
