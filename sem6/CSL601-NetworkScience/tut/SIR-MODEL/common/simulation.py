from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, Iterable, List, Set

import networkx as nx


@dataclass
class SIResult:
    s_count: List[int]
    i_count: List[int]


@dataclass
class SIRResult:
    s_count: List[int]
    i_count: List[int]
    r_count: List[int]


@dataclass
class SISResult:
    s_count: List[int]
    i_count: List[int]


def _validate_seeds(graph: nx.Graph, seeds: Iterable[int]) -> Set[int]:
    seed_set = set(seeds)
    if len(seed_set) == 0:
        raise ValueError("Seed list is empty")
    missing = [node for node in seed_set if node not in graph]
    if missing:
        raise ValueError(f"Seed nodes not in graph: {missing[:5]}")
    return seed_set


def simulate_si(
    graph: nx.Graph,
    seeds: Iterable[int],
    beta: float,
    steps: int,
) -> SIResult:
    """Discrete-time SI model with infection probability beta."""
    infected = _validate_seeds(graph, seeds)
    s_count = [graph.number_of_nodes() - len(infected)]
    i_count = [len(infected)]

    for _ in range(steps):
        new_infected: Set[int] = set()
        for src in infected:
            for nbr in graph.neighbors(src):
                if nbr in infected:
                    continue
                if random.random() < beta:
                    new_infected.add(nbr)

        infected.update(new_infected)
        s_count.append(graph.number_of_nodes() - len(infected))
        i_count.append(len(infected))

    return SIResult(s_count=s_count, i_count=i_count)


def simulate_sir(
    graph: nx.Graph,
    seeds: Iterable[int],
    beta: float,
    gamma: float,
    steps: int,
) -> SIRResult:
    """Discrete-time SIR model with infection probability beta and recovery gamma."""
    infected = _validate_seeds(graph, seeds)
    recovered: Set[int] = set()

    s_count = [graph.number_of_nodes() - len(infected)]
    i_count = [len(infected)]
    r_count = [0]

    for _ in range(steps):
        new_infected: Set[int] = set()
        new_recovered: Set[int] = set()

        for src in infected:
            for nbr in graph.neighbors(src):
                if nbr in infected or nbr in recovered:
                    continue
                if random.random() < beta:
                    new_infected.add(nbr)

            if random.random() < gamma:
                new_recovered.add(src)

        infected.difference_update(new_recovered)
        recovered.update(new_recovered)
        infected.update(new_infected)

        s_count.append(graph.number_of_nodes() - len(infected) - len(recovered))
        i_count.append(len(infected))
        r_count.append(len(recovered))

    return SIRResult(s_count=s_count, i_count=i_count, r_count=r_count)


def simulate_sis(
    graph: nx.Graph,
    seeds: Iterable[int],
    beta: float,
    gamma: float,
    steps: int,
) -> SISResult:
    """Discrete-time SIS model with infection probability beta and recovery gamma."""
    infected = _validate_seeds(graph, seeds)

    s_count = [graph.number_of_nodes() - len(infected)]
    i_count = [len(infected)]

    for _ in range(steps):
        new_infected: Set[int] = set()
        become_susceptible: Set[int] = set()

        for src in infected:
            for nbr in graph.neighbors(src):
                if nbr in infected:
                    continue
                if random.random() < beta:
                    new_infected.add(nbr)

            if random.random() < gamma:
                become_susceptible.add(src)

        infected.difference_update(become_susceptible)
        infected.update(new_infected)

        s_count.append(graph.number_of_nodes() - len(infected))
        i_count.append(len(infected))

    return SISResult(s_count=s_count, i_count=i_count)


def summarize_counts(series: List[int], total_nodes: int) -> Dict[str, float]:
    peak_value = max(series)
    peak_step = series.index(peak_value)
    return {
        "final_count": float(series[-1]),
        "final_fraction": series[-1] / total_nodes,
        "peak_count": float(peak_value),
        "peak_fraction": peak_value / total_nodes,
        "peak_step": float(peak_step),
    }
