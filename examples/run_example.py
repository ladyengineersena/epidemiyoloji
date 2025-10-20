from __future__ import annotations

from pathlib import Path

import pandas as pd

from seir.model import SEIRParameters, simulate_seir, piecewise_beta_with_intervention
from seir.plotting import plot_compartments


def run():
    """Run example SEIR simulation with intervention"""
    params = SEIRParameters(population=1_000_000, beta=0.3, sigma=0.2, gamma=0.1)
    beta_fn = piecewise_beta_with_intervention(intervention_day=30.0, reduction_fraction=0.4)

    results = simulate_seir(
        params,
        exposed0=10,
        infected0=5,
        recovered0=0,
        days=160,
        dt=0.25,
        beta_time_function=beta_fn,
    )

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "seir_example.csv"
    plot_path = out_dir / "seir_example.png"

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)

    fig, _ = plot_compartments(results, title="SEIR Example with Intervention (Day 30)")
    fig.savefig(plot_path, dpi=150, bbox_inches='tight')
    
    print(f"Saved CSV to {csv_path}")
    print(f"Saved plot to {plot_path}")
    
    # Print some statistics
    max_infected = results["I"].max()
    max_infected_day = results["t"][results["I"].argmax()]
    print(f"Peak infected: {max_infected:.0f} people on day {max_infected_day:.1f}")


if __name__ == "__main__":
    run()
