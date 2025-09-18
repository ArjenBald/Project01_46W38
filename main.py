"""
Project01_46W38 — Power curve model for a wind turbine.

Implements an approximate power curve P(v) with two interpolation options:
- "linear": g(v) = (v - v_in)/(v_rated - v_in)
- "cubic" : g(v) = (v**3)/(v_rated**3)

Returns power in the same units as Prated (per spec: MW).

Author: Aleksei
"""

from typing import Literal


def compute_power(
    v: float,
    prated: float = 15.0,
    v_in: float = 3.0,
    v_rated: float = 11.0,
    v_out: float = 25.0,
    interpolation: Literal["linear", "cubic"] = "linear",
) -> float:
    """
    Compute the wind turbine power output P(v) using an approximate piecewise model.

    Parameters
    ----------
    v : float
        Wind speed at hub height (m/s).
    prated : float, default 15.0
        Rated power of the turbine (MW).
    v_in : float, default 3.0
        Cut-in wind speed (m/s).
    v_rated : float, default 11.0
        Rated wind speed (m/s).
    v_out : float, default 25.0
        Cut-out wind speed (m/s).
    interpolation : {"linear", "cubic"}, default "linear"
        Interpolation method for  v_in ≤ v < v_rated:
        - "linear": g(v) = (v - v_in) / (v_rated - v_in)
        - "cubic" : g(v) = (v**3) / (v_rated**3)

    Returns
    -------
    float
        Power output at wind speed v (MW).

    Raises
    ------
    ValueError
        If `interpolation` is not "linear" or "cubic".
        If invalid speed thresholds (e.g., v_rated <= v_in or v_out <= v_rated).
    """
    # --- Basic validity checks on thresholds (avoid division by zero or nonsense configs)
    if not (v_in < v_rated < v_out):
        raise ValueError("Expected v_in < v_rated < v_out.")

    # Region 1 and 4: below cut-in OR at/above cut-out → no power
    if v < v_in or v >= v_out:
        return 0.0

    # Region 3: rated plateau
    if v_rated <= v < v_out:
        return float(prated)

    # Region 2: ramp-up region v_in ≤ v < v_rated
    if interpolation == "linear":
        denom = (v_rated - v_in)
        if denom <= 0:
            # Defensive programming: should already be prevented by threshold check above
            raise ValueError("Invalid thresholds: v_rated must be greater than v_in.")
        g = (v - v_in) / denom
    elif interpolation == "cubic":
        if v_rated <= 0:
            raise ValueError("v_rated must be positive for cubic interpolation.")
        g = (v ** 3) / (v_rated ** 3)
    else:
        # Requirement: raise error for invalid interpolation string
        raise ValueError('Interpolation must be either "linear" or "cubic".')

    # Safety clamp: keep g in [0, 1] near interval boundaries
    if g < 0.0:
        g = 0.0
    elif g > 1.0:
        g = 1.0

    # Final power is a fraction of the rated power
    return float(g * prated)


def _demo():
    """
    Minimal demo: compute a small table for both interpolation methods.
    """
    speeds = [0, 2.9, 3, 5, 8, 10.9, 11, 15, 24.9, 25, 30]
    print("=== Linear interpolation ===")
    print("v [m/s] -> P [MW]")
    for v in speeds:
        p = compute_power(v, prated=15, v_in=3, v_rated=11, v_out=25, interpolation="linear")
        print(f"{v:>6.1f} -> {p:>6.3f}")

    print("\n=== Cubic interpolation ===")
    print("v [m/s] -> P [MW]")
    for v in speeds:
        p = compute_power(v, prated=15, v_in=3, v_rated=11, v_out=25, interpolation="cubic")
        print(f"{v:>6.1f} -> {p:>6.3f}")


if __name__ == "__main__":
    # Main script: run demo example.
    _demo()