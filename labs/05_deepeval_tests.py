"""Lab 05 — evaluation as unit tests with DeepEval under pytest.

Run:   docker compose exec labs python -m pytest -q 05_deepeval_tests.py
The deterministic metric runs offline. The LLM-judged FaithfulnessMetric runs only when OPENAI_API_KEY is set (DeepEval's
default judge); pin the judge model in real projects and keep a human-labelled calibration set.
Try:   change the answer for the late-payment case to "3% monthly" and watch the build fail.
"""

from __future__ import annotations

import os
import re

import pytest
from deepeval import assert_test
from deepeval.metrics import BaseMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase


class NumbersGroundedMetric(BaseMetric):
    """Every number in the answer must appear in the retrieved context (catches invented rates and limits)."""

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase) -> float:
        nums = set(re.findall(r"\d+(?:\.\d+)?", test_case.actual_output))
        context = set(re.findall(r"\d+(?:\.\d+)?", " ".join(test_case.retrieval_context or [])))
        self.score = 1.0 if not nums else len(nums & context) / len(nums)
        self.success = self.score >= self.threshold
        self.reason = f"{len(nums & context)}/{len(nums)} numbers grounded" if nums else "no numbers to ground"
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(self.success)

    @property
    def __name__(self):
        return "Numbers grounded"


CASES = [
    LLMTestCase(input="What is the gold loan LTV cap?", actual_output="Gold loans are capped at 75% loan-to-value.",
                retrieval_context=["Gold loan loan-to-value must not exceed 75% of the appraised gold value."]),
    LLMTestCase(input="What interest applies to late small-business payments?", actual_output="Late small-business instalments attract 2% interest per month.",
                retrieval_context=["Late payment interest is 2% per month on overdue small-business instalments."]),
]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.input[:30])
def test_numbers_grounded(case):
    assert_test(case, [NumbersGroundedMetric()])


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="LLM-judged metric needs a judge model key")
@pytest.mark.parametrize("case", CASES, ids=lambda c: c.input[:30])
def test_faithfulness_llm_judge(case):
    assert_test(case, [FaithfulnessMetric(threshold=0.8)])
