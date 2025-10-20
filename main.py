from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

from seir.model import SEIRParameters, simulate_seir, piecewise_beta_with_intervention
from seir.plotting import plot_compartments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SEIR model simulation")
    parser.add_argument("--population", type=float, required=True, help="Total population")
    parser.add_argument("--beta", type=float, required=True, help="Contact rate")
    parser.add_argument("--sigma", type=float, required=True, help="Incubation to infectious rate")
    parser.add_argument("--gamma", type=float, required=True, help="Recovery rate")
    parser.add_argument("--exposed0", type=float, default=0.0, help="Initial exposed population")
    parser.add_argument("--infected0", type=float, default=1.0, help="Initial infected population")
    parser.add_argument("--recovered0", type=float, default=0.0, help="Initial recovered population")
    parser.add_argument("--days", type=float, default=160.0, help="Simulation duration in days")
    parser.add_argument("--dt", type=float, default=0.25, help="Time step size")
    parser.add_argument("--intervention_day", type=float, default=None, help="Day to start intervention")
    parser.add_argument("--intervention_reduction", type=float, default=None, help="Fraction to reduce beta (0-1)")
    parser.add_argument("--plot", action="store_true", help="Show plot")
    parser.add_argument("--save_csv", type=str, default=None, help="Save results to CSV file")
    parser.add_argument("--save_plot", type=str, default=None, help="Save plot to file")
    return parser.parse_args()


def ensure_parent_dir(path_str: str | None):
    if not path_str:
        return
    path = Path(path_str)
    if path.suffix:
        parent = path.parent
    else:
        parent = path
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def main():
    args = parse_args()
    params = SEIRParameters(
        population=args.population,
        beta=args.beta,
        sigma=args.sigma,
        gamma=args.gamma,
    )

    beta_fn = None
    if args.intervention_day is not None and args.intervention_reduction is not None:
        beta_fn = piecewise_beta_with_intervention(
            intervention_day=float(args.intervention_day),
            reduction_fraction=float(args.intervention_reduction),
        )

    results = simulate_seir(
        params=params,
        exposed0=args.exposed0,
        infected0=args.infected0,
        recovered0=args.recovered0,
        days=args.days,
        dt=args.dt,
        beta_time_function=beta_fn,
    )

    if args.plot or args.save_plot:
        title = "SEIR Simulation"
        if args.intervention_day is not None:
            title += f" (Intervention at day {args.intervention_day})"
        fig, _ = plot_compartments(results, title=title)
        if args.save_plot:
            ensure_parent_dir(args.save_plot)
            fig.savefig(args.save_plot, dpi=150, bbox_inches='tight')
        if args.plot:
            import matplotlib.pyplot as plt
            plt.show()

    if args.save_csv:
        ensure_parent_dir(args.save_csv)
        df = pd.DataFrame(results)
        df.to_csv(args.save_csv, index=False)
        print(f"Results saved to {args.save_csv}")


if __name__ == "__main__":
    main()
