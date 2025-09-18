"""
Project01_46W38 — Power curve model for a wind turbine.

Implements an approximate power curve P(v) with two interpolation options:
- "linear": g(v) = (v - v_in) / (v_rated - v_in)
- "cubic" : g(v) = (v**3) / (v_rated**3)

Returned power uses the same units as `prated` (per spec: MW).

Defaults follow the assignment:
    prated=15, v_in=3, v_rated=11, v_out=25, interpolation="linear"

Notes
-----
* Thresholds are validated to avoid silent misconfiguration.
* Interpolation option is validated; invalid values raise ValueError.
* Demo at the bottom prints a readable table for both interpolation modes.
"""

from typing import Iterable, List, Literal, Sequence


# ---------- Small helpers ----------

def _clamp01(x: float) -> float:
    """Clamp value to [0, 1] interval."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _validate_thresholds(v_in: float, v_rated: float, v_out: float) -> None:
    """Validate that v_in < v_rated < v_out; raise ValueError otherwise."""
    if not (v_in < v_rated < v_out):
        raise ValueError("Expected thresholds to satisfy v_in < v_rated < v_out.")


def _validate_interpolation(name: str) -> None:
    """Validate interpolation option."""
    if name not in ("linear", "cubic"):
        raise ValueError('Interpolation must be either "linear" or "cubic".')


def _validate_prated(prated: float) -> None:
    """Ensure rated power is strictly positive."""
    if prated <= 0.0:
        raise ValueError("prated must be > 0 (got {prated}).")


def _interp_weight(v: float, v_in: float, v_rated: float, interpolation: str) -> float:
    """
    Compute weighting g(v) for v in [v_in, v_rated).

    Linear ramps from 0 at v_in to 1 at v_rated.
    Cubic mimics the v^3 dependency of available wind power.
    """
    if interpolation == "linear":
        denom = (v_rated - v_in)
        if denom <= 0:
            raise ValueError("Invalid thresholds: v_rated must be greater than v_in.")
        g = (v - v_in) / denom
        return _clamp01(g)

    # interpolation == "cubic"
    if v_rated <= 0:
        raise ValueError("v_rated must be positive for cubic interpolation.")
    g = (v ** 3) / (v_rated ** 3)
    return _clamp01(g)


# ---------- Core API ----------

def compute_power(
    v: float,
    prated: float = 15.0,
    v_in: float = 3.0,
    v_rated: float = 11.0,
    v_out: float = 25.0,
    interpolation: Literal["linear", "cubic"] = "linear",
) -> float:
    """
    Compute wind turbine power output P(v) using the piecewise model.

    Parameters
    ----------
    v : float
        Wind speed at hub height (m/s).
    prated : float, default 15.0
        Rated power (MW); must be > 0.
    v_in : float, default 3.0
        Cut-in wind speed (m/s).
    v_rated : float, default 11.0
        Rated wind speed (m/s).
    v_out : float, default 25.0
        Cut-out wind speed (m/s).
    interpolation : {"linear", "cubic"}, default "linear"
        Interpolation used on [v_in, v_rated).

    Returns
    -------
    float
        Power output at wind speed v (MW).

    Raises
    ------
    ValueError
        If thresholds are inconsistent, prated <= 0, or interpolation is invalid.
    """
    # Validate configuration once per call
    _validate_prated(prated)
    _validate_thresholds(v_in, v_rated, v_out)
    _validate_interpolation(interpolation)

    # Region 1 and 4: below cut-in OR at/above cut-out → no power
    if v < v_in or v >= v_out:
        return 0.0

    # Region 3: rated plateau in [v_rated, v_out)
    if v >= v_rated:
        return float(prated)

    # Region 2: ramp-up region [v_in, v_rated)
    g = _interp_weight(v, v_in, v_rated, interpolation)
    return float(g * prated)


def compute_power_series(
    speeds: Iterable[float],
    prated: float = 15.0,
    v_in: float = 3.0,
    v_rated: float = 11.0,
    v_out: float = 25.0,
    interpolation: Literal["linear", "cubic"] = "linear",
) -> List[float]:
    """
    Convenience wrapper to compute P(v) for many wind speeds.

    Returns a list aligned with the input iterable.
    """
    _validate_prated(prated)
    _validate_thresholds(v_in, v_rated, v_out)
    _validate_interpolation(interpolation)
    return [
        compute_power(v, prated, v_in, v_rated, v_out, interpolation)
        for v in speeds
    ]


# ---------- Demo helpers (manual sanity checks) ----------

def _format_row(v: float, p: float) -> str:
    """Format one table row for demo output."""
    return f"{v:>6.2f}  ->  {p:>7.3f} MW"


def _print_demo_table(
    speeds: Sequence[float],
    prated: float,
    v_in: float,
    v_rated: float,
    v_out: float,
    interpolation: Literal["linear", "cubic"],
) -> None:
    """Print a small table for a chosen interpolation method."""
    print(f"\n=== {interpolation.capitalize()} interpolation ===")
    print("  v [m/s]   P [MW]")
    print("  ------    ------")
    for v in speeds:
        p = compute_power(v, prated, v_in, v_rated, v_out, interpolation)
        print(_format_row(v, p))


if __name__ == "__main__":
    # Main script: quick demo covering all regions of the model.
    speeds_demo = [0.0, 2.9, 3.0, 5.0, 8.0, 10.9, 11.0, 15.0, 24.9, 25.0, 30.0]
    _print_demo_table(speeds_demo, 15.0, 3.0, 11.0, 25.0, "linear")
    _print_demo_table(speeds_demo, 15.0, 3.0, 11.0, 25.0, "cubic")