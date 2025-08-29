from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np
from scipy.optimize import minimize

__all__ = [
    "TransformerSpecs",
    "Weighting",
    "optimize_transformer",
]

# -----------------------------------------------------------------------------
# Dataclasses holding user‑configurable information
# -----------------------------------------------------------------------------

@dataclass(slots=True)
class TransformerSpecs:
    """Electrical specification of the transformer to optimise."""

    primary_voltage: float  # V (phase‑to‑phase)
    secondary_voltage: float  # V (phase‑to‑phase or phase‑to‑neutral)
    power_kva: float  # rated power in kVA

    def power_w(self) -> float:
        """Rated power in watts."""
        return self.power_kva * 1_000.0


@dataclass(slots=True)
class Weighting:
    """Weights for the composite objective function.

    All four weights must sum to 1.0 (the function does *not* enforce this).
    Increasing `efficiency` lowers the penalty for low efficiency, since the
    cost component for efficiency is defined as (1 ‑ η).
    """

    mass: float = 0.25
    cost: float = 0.25
    efficiency: float = 0.25  # weight applied to (1‑η) so higher weight favours *high* η
    losses: float = 0.25


# -----------------------------------------------------------------------------
# Low‑level physical/financial models
# -----------------------------------------------------------------------------

DENSITY_STEEL_G_CM3 = 7.6
DENSITY_CU_G_CM3 = 8.9
PRICE_STEEL_EUR_KG = 2.0
PRICE_CU_EUR_KG = 8.0
CORE_STACK_CM = 30.0  # assumed constant stack depth
WINDING_LENGTH_M = 2.0  # average conductor length per mm² (rough estimate)


def compute_mass(params: Tuple[float, float]) -> float:
    """Return total mass *in kg* for given core (cm²) and copper (mm²)."""

    s_fer_cm2, s_cuivre_mm2 = params

    mass_steel_g = s_fer_cm2 * CORE_STACK_CM * DENSITY_STEEL_G_CM3
    mass_cu_g = s_cuivre_mm2 * WINDING_LENGTH_M * DENSITY_CU_G_CM3

    return (mass_steel_g + mass_cu_g) / 1_000.0  # g → kg


def compute_cost(params: Tuple[float, float]) -> float:
    """Return material cost *in €* for a single unit."""

    s_fer_cm2, s_cuivre_mm2 = params

    mass_steel_kg = (s_fer_cm2 * CORE_STACK_CM * DENSITY_STEEL_G_CM3) / 1_000.0
    mass_cu_kg = (s_cuivre_mm2 * WINDING_LENGTH_M * DENSITY_CU_G_CM3) / 1_000.0

    return mass_steel_kg * PRICE_STEEL_EUR_KG + mass_cu_kg * PRICE_CU_EUR_KG


def compute_losses(params: Tuple[float, float], specs: TransformerSpecs) -> float:
    """Approximate total losses *in W* at rated load."""

    s_fer_cm2, s_cuivre_mm2 = params

    # Empirical core loss model (no‑load): P_core ∝ B^1.5 ~ s_fer^1.5
    p_core = 1.1 * s_fer_cm2 ** 1.5

    # Copper losses (load): P_cu = I²·R.  R ∝ length/area;  I ∝ power/voltage.
    # The constant 0.006 has been tuned for typical LV windings.
    p_cu = 0.006 * (specs.power_w() ** 2) / s_cuivre_mm2

    return p_core + p_cu


def compute_efficiency(params: Tuple[float, float], specs: TransformerSpecs) -> float:
    """Return efficiency (0‑1) at rated load."""

    losses = compute_losses(params, specs)
    return specs.power_w() / (specs.power_w() + losses)


# -----------------------------------------------------------------------------
# Objective + constraints
# -----------------------------------------------------------------------------


def _objective_weighted(
        params: Tuple[float, float],
        specs: TransformerSpecs,
        weights: Weighting,
) -> float:
    """Composite objective to *minimise* via a weighted normalisation approach."""

    mass_kg = compute_mass(params)
    cost_eur = compute_cost(params)
    efficiency = compute_efficiency(params, specs)  # 0‑1
    losses_w = compute_losses(params, specs)

    # --- Normalisation (heuristic, adjust if scale issues appear) ---
    mass_norm = mass_kg / 1_000.0      # expect <1 t
    cost_norm = cost_eur / 10_000.0    # expect <10 k€
    eff_norm = 1.0 - efficiency        # want to minimise (1‑η)
    losses_norm = losses_w / 10_000.0  # expect <10 kW

    return (
        weights.mass * mass_norm
        + weights.cost * cost_norm
        + weights.efficiency * eff_norm
        + weights.losses * losses_norm
    )


def _temperature_constraint(params: Tuple[float, float]) -> float:
    """Inequality constraint: must be >= 0 → T_max ≤ 90 °C."""

    s_fer_cm2, s_cuivre_mm2 = params
    temp_c = 20.0 + 0.03 * (s_fer_cm2 + s_cuivre_mm2) ** 1.2
    return 90.0 - temp_c


# -----------------------------------------------------------------------------
# Public optimisation helper
# -----------------------------------------------------------------------------


def optimize_transformer(
        specs: TransformerSpecs,
        weights: Weighting | None = None,
        bounds: Tuple[Tuple[float, float], Tuple[float, float]] | None = None,
        initial_guess: Tuple[float, float] | None = None,
) -> Dict[str, float]:
    """Run SLSQP optimisation and return a dict of useful results.

    Parameters
    ----------
    specs : TransformerSpecs
        Electrical specification for which to size the transformer.
    weights : Weighting, optional
        Relative importance of each objective (default 0.25 each).
    bounds : ((min,max),(min,max)), optional
        Bounds for (core_section_cm2, copper_section_mm2). Defaults to
        (10‑200 cm², 50‑1000 mm²).
    initial_guess : (core, copper), optional
        Starting point for the optimizer (default 60 cm², 200 mm²).
    """

    weights = weights or Weighting()
    bounds = bounds or ((10.0, 200.0), (50.0, 1_000.0))
    initial_guess = initial_guess or (60.0, 200.0)

    result = minimize(
        _objective_weighted,
        initial_guess,
        args=(specs, weights),
        bounds=bounds,
        constraints=[{"type": "ineq", "fun": _temperature_constraint}],
        method="SLSQP",
        options={"ftol": 1e-6, "disp": False},
    )

    if not result.success:
        raise RuntimeError(f"Optimisation failed: {result.message}")

    s_fer_cm2, s_cuivre_mm2 = result.x

    losses_w = compute_losses(result.x, specs)
    efficiency_pc = compute_efficiency(result.x, specs) * 100.0
    temp_max_c = 20.0 + 0.03 * (s_fer_cm2 + s_cuivre_mm2) ** 1.2

    return {
        "core_section_cm2": round(s_fer_cm2, 2),
        "copper_section_mm2": round(s_cuivre_mm2, 2),
        "mass_kg": round(compute_mass(result.x), 2),
        "cost_eur": round(compute_cost(result.x), 2),
        "losses_w": round(losses_w, 2),
        "efficiency_percent": round(efficiency_pc, 2),
        "temperature_c": round(temp_max_c, 2),
    }


# -----------------------------------------------------------------------------
# CLI usage for quick testing
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import pprint

    specs_demo = TransformerSpecs(
        primary_voltage=20_000.0,
        secondary_voltage=400.0,
        power_kva=250.0,
    )

    best = optimize_transformer(specs_demo)

    pprint.pprint(best)
