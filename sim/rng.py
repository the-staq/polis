"""SeededRandom — deterministic randomness for replayable sims.

Every Sim instance carries one of these. The seed is recorded in the sim's
config so a run can be replayed bit-for-bit from EventLog given the stub LLM
hook (real LLM hooks add nondeterminism — that's a feature, not a bug).
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class SeededRandom:
    """Wraps `random.Random` with conveniences for sim configs.

    Use the high-level helpers (`weighted_choice`, `bernoulli`, etc.) in config
    code so swapping in a different RNG implementation later is a single change.
    """

    __slots__ = ("seed", "_rng")

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self._rng = random.Random(seed)

    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        return self._rng.uniform(low, high)

    def bernoulli(self, p: float) -> bool:
        """Returns True with probability `p`."""
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"bernoulli p must be in [0, 1], got {p}")
        return self._rng.random() < p

    def choice(self, seq: Sequence[T]) -> T:
        return self._rng.choice(seq)

    def weighted_choice(self, choices: Sequence[T], weights: Sequence[float]) -> T:
        """Sample from `choices` with given weights. Weights are normalized."""
        if len(choices) != len(weights):
            raise ValueError(f"choices ({len(choices)}) and weights ({len(weights)}) must match")
        return self._rng.choices(choices, weights=weights, k=1)[0]

    def normal(self, mean: float = 0.0, stdev: float = 1.0) -> float:
        return self._rng.gauss(mean, stdev)

    def integer(self, low: int, high: int) -> int:
        """Inclusive on both ends."""
        return self._rng.randint(low, high)
