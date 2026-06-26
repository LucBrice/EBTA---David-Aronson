"""OOS confidence interval procedure.

Source: SOP 01 sections 3, 4, 7, 8, 10, 13, 15, and 20; DN-019 to DN-022.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

import math
from typing import Any

from ebta_engine.procedures.bootstrap import stationary_block_indices


def oos_confidence_interval(
    oos_returns: list[float],
    *,
    replications: int,
    mean_block_length: float,
    seed: int,
    bootstrap_source: str = "OOS_STATIONARY_BLOCK",
    power: float = 0.80,
    sessions_per_year: int = 252,
) -> dict[str, Any]:
    if not oos_returns:
        raise ValueError("OOS confidence interval requires a non-empty OOS series")
    if "WRC" in bootstrap_source.upper() or "TEST" in bootstrap_source.upper():
        raise ValueError("OOS confidence interval must not reuse WRC Test bootstrap distribution")
    indices = stationary_block_indices(
        len(oos_returns),
        replications=replications,
        mean_block_length=mean_block_length,
        seed=seed,
    )
    bootstrap_means = [
        sum(oos_returns[index] for index in sample) / len(sample)
        for sample in indices
    ]
    estimate = sum(oos_returns) / len(oos_returns)
    lower_95 = _quantile(bootstrap_means, 0.05)
    upper_90 = _quantile(bootstrap_means, 0.95)
    verdict = _statistical_verdict(estimate, lower_95, power)
    power_check = validate_power_target(power, target_power=0.80)
    return {
        "artifact_type": "oos_confidence_interval",
        "source_normative": "SOP 01 sections 3, 4, 7, 8, 10, 13, 15, 20; DN-019 to DN-022",
        "source": bootstrap_source,
        "oos_observation_count": len(oos_returns),
        "estimate": estimate,
        "lower_95_one_sided": lower_95,
        "upper_90_descriptive": upper_90,
        "ci_90_descriptive": [lower_95, upper_90],
        "annualized_log_estimate": sessions_per_year * estimate,
        "annualized_simple_estimate": math.exp(sessions_per_year * estimate) - 1.0,
        "bootstrap_means": bootstrap_means,
        "replications": replications,
        "seed": seed,
        "power": power,
        "power_check": power_check,
        "statistical_gate": verdict,
    }


def _quantile(values: list[float], probability: float) -> float:
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between 0 and 1")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[int(position)]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _statistical_verdict(estimate: float, lower_bound: float, power: float) -> str:
    if power < 0.80:
        return "INCONCLUSIVE"
    if estimate <= 0:
        return "FAIL"
    if lower_bound > 0:
        return "PASS"
    return "NOT_VALIDATED"


def validate_power_target(
    achieved_power: float,
    *,
    target_power: float = 0.80,
) -> dict[str, object]:
    """Validate that achieved power meets the preregistered target.

    Source: SOP 01; DN-021 — OOS analysis requires a target power of at
    least 80% per the preregistered plan.

    Parameters
    ----------
    achieved_power:
        Power estimate computed or supplied by the research pipeline.
    target_power:
        Preregistered minimum power target.  Defaults to 0.80 (DN-021).

    Returns
    -------
    dict
        ``status``: PASS | INCONCLUSIVE
    """
    if achieved_power >= target_power:
        return {
            "status": "PASS",
            "achieved_power": achieved_power,
            "target_power": target_power,
            "authority": "SOP 01 / DN-021",
        }
    return {
        "status": "INCONCLUSIVE",
        "achieved_power": achieved_power,
        "target_power": target_power,
        "authority": "SOP 01 / DN-021",
        "description": (
            f"Achieved power {achieved_power:.2f} is below the preregistered "
            f"target {target_power:.2f}. The OOS result is INCONCLUSIVE "
            "until the information stop criterion is met (DN-021)."
        ),
    }


def validate_information_stop_point(
    oos_observation_count: int,
    *,
    preregistered_stop_count: int | None = None,
    preregistered_stop_date: str | None = None,
    actual_date: str | None = None,
) -> dict[str, object]:
    """Verify that the verdict is computed at the preregistered stop point.

    Source: DN-004 — the OOS verdict must be produced at the preregistered
    information stop criterion, not opportunistically on significance.

    Parameters
    ----------
    oos_observation_count:
        Number of OOS observations in the current series.
    preregistered_stop_count:
        Preregistered number of OOS days at which to compute the verdict.
    preregistered_stop_date:
        Preregistered calendar date at which to compute the verdict.
    actual_date:
        Actual date of the verdict computation (ISO-8601 string).

    Returns
    -------
    dict
        ``status``: PASS | INCONCLUSIVE | FAIL
    """
    violations: list[str] = []

    if preregistered_stop_count is not None:
        if oos_observation_count < preregistered_stop_count:
            violations.append(
                f"OOS has {oos_observation_count} observations but the "
                f"preregistered stop requires {preregistered_stop_count}. "
                "The verdict must not be computed early (DN-004)."
            )

    if preregistered_stop_date is not None and actual_date is not None:
        if actual_date < preregistered_stop_date:
            violations.append(
                f"Verdict computed on {actual_date} before the preregistered "
                f"stop date {preregistered_stop_date}. "
                "Early stopping is only allowed by an independent rule (DN-004)."
            )

    return {
        "status": "PASS" if not violations else "FAIL",
        "oos_observation_count": oos_observation_count,
        "preregistered_stop_count": preregistered_stop_count,
        "preregistered_stop_date": preregistered_stop_date,
        "authority": "SOP 01 / DN-004",
        "violations": violations,
    }

