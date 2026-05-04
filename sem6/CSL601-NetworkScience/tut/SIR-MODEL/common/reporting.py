from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import pandas as pd


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_timeseries_csv(records: Iterable[Dict], output_file: Path) -> None:
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)


def save_summary_csv(summary_rows: List[Dict], output_file: Path) -> None:
    df = pd.DataFrame(summary_rows)
    df.to_csv(output_file, index=False)


def plot_si_comparison(
    timesteps: List[int],
    top5_i: List[int],
    random5_i: List[int],
    model_name: str,
    output_file: Path,
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, top5_i, label="Top-5 degree seeds", linewidth=2)
    plt.plot(timesteps, random5_i, label="Random-5 seeds", linewidth=2)
    plt.title(f"SI Comparison on {model_name} (10K nodes)")
    plt.xlabel("Time step")
    plt.ylabel("Infected count")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def plot_sir_comparison(
    timesteps: List[int],
    top5_i: List[int],
    top5_r: List[int],
    random5_i: List[int],
    random5_r: List[int],
    model_name: str,
    output_file: Path,
) -> None:
    plt.figure(figsize=(11, 6))
    plt.plot(timesteps, top5_i, label="Top-5 infected", linewidth=2)
    plt.plot(timesteps, top5_r, label="Top-5 recovered", linewidth=2)
    plt.plot(timesteps, random5_i, label="Random-5 infected", linewidth=2)
    plt.plot(timesteps, random5_r, label="Random-5 recovered", linewidth=2)
    plt.title(f"SIR Comparison on {model_name} (10K nodes)")
    plt.xlabel("Time step")
    plt.ylabel("Node count")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def plot_si_curve(
    timesteps: List[int],
    infected: List[int],
    model_name: str,
    scenario_name: str,
    output_file: Path,
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, infected, label="Infected", linewidth=2)
    plt.title(f"SI on {model_name} ({scenario_name})")
    plt.xlabel("Time step")
    plt.ylabel("Infected count")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def plot_sir_curve(
    timesteps: List[int],
    infected: List[int],
    recovered: List[int],
    model_name: str,
    scenario_name: str,
    output_file: Path,
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, infected, label="Infected", linewidth=2)
    plt.plot(timesteps, recovered, label="Recovered", linewidth=2)
    plt.title(f"SIR on {model_name} ({scenario_name})")
    plt.xlabel("Time step")
    plt.ylabel("Node count")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def plot_sis_curve(
    timesteps: List[int],
    susceptible: List[int],
    infected: List[int],
    model_name: str,
    scenario_name: str,
    output_file: Path,
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, susceptible, label="Susceptible", linewidth=2)
    plt.plot(timesteps, infected, label="Infected", linewidth=2)
    plt.title(f"SIS on {model_name} ({scenario_name})")
    plt.xlabel("Time step")
    plt.ylabel("Node count")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
