# SIR-MODEL (10K Nodes)

This implementation creates 10,000-node networks using:
- Barabasi-Albert model
- Erdos-Renyi model

Two scenarios are implemented in separate directories:
- `scenario_top5_degree/`: top-5 highest-degree seed nodes
- `scenario_random5/`: 5 random seed nodes

Each scenario runs:
- SI simulation (Susceptible-Infected)
- SIR simulation (Susceptible-Infected-Recovered)
- SIS simulation (Susceptible-Infectious-Susceptible)

## Parameters
- Nodes: 10,000
- BA: m=3
- ER: p=0.001
- Infection probability (`beta`): 0.1
- Recovery probability (`gamma`): 0.05
- Steps: 100

## Run

From `SIR-MODEL`:

```bash
python scenario_top5_degree/run_top5_degree.py
python scenario_random5/run_random5.py
```

## Outputs

Generated under:
- `outputs/scenario_top5_degree/`
- `outputs/scenario_random5/`

Each contains:
- per-model SI CSV
- per-model SIR CSV
- per-model SIS CSV
- summary CSV
- SI, SIR, and SIS curve PNG plots
