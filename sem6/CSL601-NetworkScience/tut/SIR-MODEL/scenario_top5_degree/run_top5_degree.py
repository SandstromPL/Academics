from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from common.graph_models import (  # noqa: E402
    GraphConfig,
    generate_barabasi_albert,
    generate_erdos_renyi,
    top_k_by_degree,
)
from common.reporting import (  # noqa: E402
    ensure_dir,
    plot_si_curve,
    plot_sis_curve,
    plot_sir_curve,
    save_summary_csv,
    save_timeseries_csv,
)
from common.simulation import simulate_si, simulate_sir, simulate_sis, summarize_counts  # noqa: E402


def run() -> None:
    cfg = GraphConfig(n_nodes=10_000, ba_m=3, er_p=0.001)
    beta = 0.1
    gamma = 0.05
    steps = 100

    out_dir = ROOT / "outputs" / "scenario_top5_degree"
    ensure_dir(out_dir)

    models = {
        "Barabasi-Albert": generate_barabasi_albert(cfg),
        "Erdos-Renyi": generate_erdos_renyi(cfg),
    }

    summary_rows: List[Dict] = []

    for model_name, graph in models.items():
        seed_nodes = top_k_by_degree(graph, 5)
        timesteps = list(range(steps + 1))

        si = simulate_si(graph, seed_nodes, beta=beta, steps=steps)
        sir = simulate_sir(graph, seed_nodes, beta=beta, gamma=gamma, steps=steps)
        sis = simulate_sis(graph, seed_nodes, beta=beta, gamma=gamma, steps=steps)

        si_records = [
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SI",
                "time": t,
                "susceptible": si.s_count[t],
                "infected": si.i_count[t],
            }
            for t in timesteps
        ]
        save_timeseries_csv(si_records, out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_si.csv")

        sir_records = [
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SIR",
                "time": t,
                "susceptible": sir.s_count[t],
                "infected": sir.i_count[t],
                "recovered": sir.r_count[t],
            }
            for t in timesteps
        ]
        save_timeseries_csv(sir_records, out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_sir.csv")

        sis_records = [
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SIS",
                "time": t,
                "susceptible": sis.s_count[t],
                "infected": sis.i_count[t],
            }
            for t in timesteps
        ]
        save_timeseries_csv(sis_records, out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_sis.csv")

        plot_si_curve(
            timesteps,
            infected=si.i_count,
            model_name=model_name,
            scenario_name="top5_degree",
            output_file=out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_si_curve.png",
        )
        plot_sir_curve(
            timesteps,
            infected=sir.i_count,
            recovered=sir.r_count,
            model_name=model_name,
            scenario_name="top5_degree",
            output_file=out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_sir_curve.png",
        )
        plot_sis_curve(
            timesteps,
            susceptible=sis.s_count,
            infected=sis.i_count,
            model_name=model_name,
            scenario_name="top5_degree",
            output_file=out_dir / f"{model_name.lower().replace('-', '_').replace(' ', '_')}_sis_curve.png",
        )

        si_summary = summarize_counts(si.i_count, cfg.n_nodes)
        sir_i_summary = summarize_counts(sir.i_count, cfg.n_nodes)
        sis_i_summary = summarize_counts(sis.i_count, cfg.n_nodes)

        summary_rows.append(
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SI",
                "seed_nodes": ",".join(map(str, seed_nodes)),
                "final_infected": si_summary["final_count"],
                "final_infected_fraction": si_summary["final_fraction"],
                "peak_infected": si_summary["peak_count"],
                "peak_infected_fraction": si_summary["peak_fraction"],
                "peak_step": si_summary["peak_step"],
                "final_recovered": 0.0,
                "final_recovered_fraction": 0.0,
            }
        )
        summary_rows.append(
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SIR",
                "seed_nodes": ",".join(map(str, seed_nodes)),
                "final_infected": sir_i_summary["final_count"],
                "final_infected_fraction": sir_i_summary["final_fraction"],
                "peak_infected": sir_i_summary["peak_count"],
                "peak_infected_fraction": sir_i_summary["peak_fraction"],
                "peak_step": sir_i_summary["peak_step"],
                "final_recovered": float(sir.r_count[-1]),
                "final_recovered_fraction": sir.r_count[-1] / cfg.n_nodes,
            }
        )
        summary_rows.append(
            {
                "model": model_name,
                "scenario": "top5_degree",
                "simulation": "SIS",
                "seed_nodes": ",".join(map(str, seed_nodes)),
                "final_infected": sis_i_summary["final_count"],
                "final_infected_fraction": sis_i_summary["final_fraction"],
                "peak_infected": sis_i_summary["peak_count"],
                "peak_infected_fraction": sis_i_summary["peak_fraction"],
                "peak_step": sis_i_summary["peak_step"],
                "final_recovered": 0.0,
                "final_recovered_fraction": 0.0,
            }
        )

        print(f"[{model_name}] top-5 degree seeds: {seed_nodes}")
        print(f"[{model_name}] SI final infected: {si.i_count[-1]} / {cfg.n_nodes}")
        print(
            f"[{model_name}] SIR final infected/recovered: "
            f"{sir.i_count[-1]} / {sir.r_count[-1]}"
        )
        print(f"[{model_name}] SIS final infected: {sis.i_count[-1]} / {cfg.n_nodes}")

    save_summary_csv(summary_rows, out_dir / "summary.csv")


if __name__ == "__main__":
    run()
