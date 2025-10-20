from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class SEIRParameters:
    population: float
    beta: float
    sigma: float
    gamma: float


def simulate_seir(
    params: SEIRParameters,
    exposed0: float,
    infected0: float,
    recovered0: float,
    days: float,
    dt: float = 0.25,
    beta_time_function: Callable[[float, float], float] | None = None,
    random_seed: int | None = None,
) -> Dict[str, np.ndarray]:
    """
    Deterministic SEIR dynamics using simple Euler integration.

    Returns dict with keys: t, S, E, I, R
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    if days <= 0:
        raise ValueError("days must be positive")

    if random_seed is not None:
        np.random.seed(random_seed)

    population = float(params.population)
    infected0 = float(infected0)
    exposed0 = float(exposed0)
    recovered0 = float(recovered0)
    susceptible0 = population - exposed0 - infected0 - recovered0
    if susceptible0 < 0:
        raise ValueError("Initial compartments exceed population")

    num_steps = int(np.ceil(days / dt)) + 1
    t = np.linspace(0.0, dt * (num_steps - 1), num_steps)

    S = np.zeros(num_steps, dtype=float)
    E = np.zeros(num_steps, dtype=float)
    I = np.zeros(num_steps, dtype=float)
    R = np.zeros(num_steps, dtype=float)

    S[0] = susceptible0
    E[0] = exposed0
    I[0] = infected0
    R[0] = recovered0

    def get_beta(time: float) -> float:
        if beta_time_function is None:
            return params.beta
        return max(beta_time_function(time, params.beta), 0.0)

    inv_population = 1.0 / population if population != 0 else 0.0

    for k in range(num_steps - 1):
        time = t[k]
        beta_value = get_beta(time)

        infection_force = beta_value * S[k] * I[k] * inv_population
        exposed_to_infected = params.sigma * E[k]
        recovery = params.gamma * I[k]

        dS = -infection_force
        dE = infection_force - exposed_to_infected
        dI = exposed_to_infected - recovery
        dR = recovery

        S[k + 1] = S[k] + dt * dS
        E[k + 1] = E[k] + dt * dE
        I[k + 1] = I[k] + dt * dI
        R[k + 1] = R[k] + dt * dR

        # Numerical guardrails
        if S[k + 1] < 0:
            S[k + 1] = 0.0
        if E[k + 1] < 0:
            E[k + 1] = 0.0
        if I[k + 1] < 0:
            I[k + 1] = 0.0
        if R[k + 1] < 0:
            R[k + 1] = 0.0

        total = S[k + 1] + E[k + 1] + I[k + 1] + R[k + 1]
        if total != population and population > 0:
            # Renormalize to avoid drift
            scale = population / total
            S[k + 1] *= scale
            E[k + 1] *= scale
            I[k + 1] *= scale
            R[k + 1] *= scale

    return {"t": t, "S": S, "E": E, "I": I, "R": R}


def piecewise_beta_with_intervention(
    intervention_day: float,
    reduction_fraction: float,
) -> Callable[[float, float], float]:
    """
    Create a beta(t) function that reduces beta by given fraction from intervention_day onward.
    reduction_fraction in [0,1], e.g. 0.4 means reduce beta to 60%.
    """
    if not (0.0 <= reduction_fraction <= 1.0):
        raise ValueError("reduction_fraction must be within [0, 1]")

    def beta_time_fn(time: float, base_beta: float) -> float:
        if time >= intervention_day:
            return base_beta * (1.0 - reduction_fraction)
        return base_beta

    return beta_time_fn
