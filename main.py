"""
Project01_46W38 — Simple power curve model.

One function:
    power_output(v, prated=15, v_in=3, v_rated=11, v_out=25, interpolation="linear")

Implements the required piecewise model with two options for g(v):
- linear: g(v) = (v - v_in) / (v_rated - v_in)
- cubic : g(v) = v**3 / v_rated**3

Returns power in the same units as prated (MW by assignment convention).
"""

def power_output(
    v: float,
    prated: float = 15.0,
    v_in: float = 3.0,
    v_rated: float = 11.0,
    v_out: float = 25.0,
    interpolation: str = "linear",
) -> float:
    """
    Compute turbine power P(v) using a simple piecewise model.

    Parameters
    ----------
    v : float
        Wind speed at hub height (m/s).
    prated : float, default 15.0
        Rated power (MW).
    v_in : float, default 3.0
        Cut-in wind speed (m/s).
    v_rated : float, default 11.0
        Rated wind speed (m/s).
    v_out : float, default 25.0
        Cut-out wind speed (m/s).
    interpolation : {"linear", "cubic"}, default "linear"
        Weighting function g(v) on [v_in, v_rated).

    Returns
    -------
    float
        Power output P(v) in MW.

    Notes
    -----
    Only the interpolation string is validated (per assignment).
    """
    # Region 1 & 4: below cut-in OR at/above cut-out → zero power
    if v < v_in or v >= v_out:
        return 0.0

    # Region 3: rated plateau
    if v >= v_rated:
        return float(prated)

    # Region 2: ramp-up region — choose g(v)
    if interpolation == "linear":
        g = (v - v_in) / (v_rated - v_in)
    elif interpolation == "cubic":
        g = (v ** 3) / (v_rated ** 3)
    else:
        raise ValueError('interpolation must be "linear" or "cubic"')

    # Clamp g to [0, 1] (на случай граничных округлений)
    if g < 0.0:
        g = 0.0
    if g > 1.0:
        g = 1.0

    return float(g * prated)