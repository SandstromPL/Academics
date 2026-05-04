from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List

import networkx as nx


@dataclass(frozen=True)
class GraphConfig:
    n_nodes: int = 10_000
    ba_m: int = 3
    er_p: float = 0.001


def generate_barabasi_albert(cfg: GraphConfig) -> nx.Graph:
    """Generate a Barabasi-Albert graph."""
    return nx.barabasi_albert_graph(n=cfg.n_nodes, m=cfg.ba_m)


def generate_erdos_renyi(cfg: GraphConfig) -> nx.Graph:
    """Generate an Erdos-Renyi graph."""
    return nx.erdos_renyi_graph(n=cfg.n_nodes, p=cfg.er_p)


def top_k_by_degree(graph: nx.Graph, k: int) -> List[int]:
    """Return top-k nodes by degree (descending)."""
    ranked = sorted(graph.degree, key=lambda item: item[1], reverse=True)
    return [node for node, _ in ranked[:k]]


def random_k_nodes(graph: nx.Graph, k: int) -> List[int]:
    """Return k random nodes."""
    return random.sample(list(graph.nodes()), k)
