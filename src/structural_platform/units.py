from __future__ import annotations


def kn(value: float) -> float:
    return float(value) * 1000.0


def kn_per_m(value: float) -> float:
    return float(value) * 1000.0


def gpa(value: float) -> float:
    return float(value) * 1_000_000_000.0


def mm(value: float) -> float:
    return float(value) / 1000.0


def cm4(value: float) -> float:
    return float(value) * 1e-8
