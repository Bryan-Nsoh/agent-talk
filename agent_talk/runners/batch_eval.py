"""Batch evaluation runner."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

from agent_talk.agents import (
    AgentA,
    AgentB,
    AgentConfig,
    SendAllAgentA,
    SendAllAgentB,
)
from agent_talk.core.coords import bytes_to_coords, decode_cells_delta16
from agent_talk.core.rle import decode_path_rle4
from agent_talk.core.protocol import ConversationLimits
from agent_talk.env.grid import Grid
from agent_talk.io import CacheEntry, iter_cache, append_log
from agent_talk.oracle.oracle import OracleError, verify_cut_cert, verify_path_cert, union_grid
from agent_talk.runners import simulate_conversation

try:  # optional dependency
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is not None:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return simple_yaml_load(path.read_text(encoding="utf-8"))


def simple_yaml_load(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    stack: list[Tuple[int, Dict[str, Any]]] = [(0, data)]
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.lstrip().partition(":")
        key = key.strip()
        value = value.strip()
        while stack and indent < stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if not value:
            new_dict: Dict[str, Any] = {}
            container[key] = new_dict
            stack.append((indent + 2, new_dict))
        else:
            container[key] = parse_scalar(value)
    return data


def parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def make_limits(cfg: Dict[str, Any]) -> ConversationLimits:
    return ConversationLimits(
        max_rounds=int(cfg.get("max_rounds", 64)),
        max_bytes_per_message=int(cfg.get("max_bytes_per_message", 256)),
        max_total_bytes=int(cfg.get("max_total_bytes", 3 * 1024)),
    )


def apply_ablation(system_cfg: Dict[str, Any], ablation_cfg: Dict[str, Any]) -> Dict[str, Any]:
    merged = json.loads(json.dumps(system_cfg))
    if not ablation_cfg:
        return merged
    if "encoding" in ablation_cfg:
        merged.setdefault("encoding", {}).update(ablation_cfg["encoding"])
    if ablation_cfg.get("forbid_path"):
        merged["allow_path"] = False
    if ablation_cfg.get("forbid_cut"):
        merged["allow_cut"] = False
    if "grid_size" in ablation_cfg:
        merged["grid_size"] = ablation_cfg["grid_size"]
    return merged


def make_agent_configs(entry: CacheEntry, system: str, cfg: Dict[str, Any]) -> Tuple[AgentConfig, AgentConfig, Dict[str, Any]]:
    grid_override = cfg.get("grid_size")
    if grid_override and entry.height != grid_override:
        raise ValueError("grid size mismatch for ablation")

    encoding_cfg = cfg.get("encoding", {})
    base_params = {
        "max_path_attempts": cfg.get("max_path_attempts", cfg.get("max_probes", 6)),
        "max_path_length": cfg.get("max_path_length", 64),
        "allow_path": cfg.get("allow_path", True),
        "allow_cut": cfg.get("allow_cut", True),
        "path_encoding": encoding_cfg.get("paths", "RLE4_v1"),
        "cut_encoding": encoding_cfg.get("cuts", "DELTA16_v1"),
    }
    config_a = AgentConfig(
        name="A",
        height=entry.height,
        width=entry.width,
        start=entry.start,
        goal=entry.goal,
        private_mask=entry.mask_a,
        **base_params,
    )
    config_b = AgentConfig(
        name="B",
        height=entry.height,
        width=entry.width,
        start=entry.start,
        goal=entry.goal,
        private_mask=entry.mask_b,
        **base_params,
    )
    return config_a, config_b, cfg


def instantiate_agents(system: str, config_a: AgentConfig, config_b: AgentConfig, system_cfg: Dict[str, Any]):
    if system == "certtalk" or system == "greedyprobe":
        return AgentA(config_a), AgentB(config_b)
    if system == "cutgrow":
        config_a.allow_path = False
        config_b.allow_path = False
        return AgentA(config_a), AgentB(config_b)
    if system == "sendall":
        chunk_size = system_cfg.get("chunk_size", 32)
        return SendAllAgentA(config_a, chunk_size=chunk_size), SendAllAgentB(config_b, chunk_size=chunk_size)
    raise ValueError(f"unknown system {system}")


def decode_path_length(payload: Dict[str, Any]) -> int:
    encoding = payload.get("encoding")
    data = base64.b64decode(payload.get("runs", ""), validate=True)
    start = tuple(payload.get("s"))
    if encoding == "RLE4_v1":
        path = decode_path_rle4(start, data)
    elif encoding == "ABS16_v1":
        path = bytes_to_coords(data)
    else:
        raise ValueError("unknown path encoding")
    return max(0, len(path) - 1)


def decode_cut_size(payload: Dict[str, Any]) -> int:
    encoding = payload.get("encoding")
    data = base64.b64decode(payload.get("cells", ""), validate=True)
    if encoding == "DELTA16_v1":
        cells = decode_cells_delta16(data)
    elif encoding == "ABS16_v1":
        cells = bytes_to_coords(data)
    else:
        raise ValueError("unknown cut encoding")
    return len(cells)


def run(cache: Path, system: str, out: Path, config_path: Path, ablation: Optional[str], ablation_path: Optional[Path], split: Optional[str]) -> None:
    base_cfg = load_yaml(config_path) if config_path else {}
    system_cfg = base_cfg.get("systems", {}).get(system, {})
    limits_cfg = base_cfg.get("limits", {})
    ablation_cfg: Dict[str, Any] = {}
    if ablation and ablation_path:
        ablations = load_yaml(ablation_path)
        ablation_cfg = ablations.get(ablation, {}) if isinstance(ablations, dict) else {}
    merged_cfg = apply_ablation(system_cfg, ablation_cfg)
    limits = make_limits(limits_cfg)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        pass  # truncate

    for entry in iter_cache(cache):
        if split and entry.split != split:
            continue
        try:
            config_a, config_b, effective_cfg = make_agent_configs(entry, system, merged_cfg)
        except ValueError:
            continue
        agent_a, agent_b = instantiate_agents(system, config_a, config_b, effective_cfg)
        result = simulate_conversation(agent_a, agent_b, limits)

        grid_a = Grid.from_flat(entry.height, entry.width, entry.mask_a)
        grid_b = Grid.from_flat(entry.height, entry.width, entry.mask_b)
        union = union_grid(grid_a, grid_b)

        oracle_ok = False
        path_gap = None
        cut_gap = None
        if result.certificate_type and result.certificate_payload:
            try:
                if result.certificate_type == "PATH_CERT":
                    oracle_ok = verify_path_cert(result.certificate_payload, union, entry.start, entry.goal)
                    if entry.shortest is not None:
                        path_gap = decode_path_length(result.certificate_payload) - entry.shortest
                elif result.certificate_type == "CUT_CERT":
                    oracle_ok = verify_cut_cert(result.certificate_payload, union, entry.start, entry.goal)
                    if entry.min_cut is not None:
                        cut_gap = decode_cut_size(result.certificate_payload) - entry.min_cut
            except OracleError:
                oracle_ok = False

        record = {
            "system": system,
            "split": entry.split,
            "seed": entry.seed,
            "outcome": result.outcome,
            "bytes": result.bytes_used,
            "rounds": result.rounds,
            "certificate_type": result.certificate_type,
            "oracle_accepted": oracle_ok,
            "path_gap": path_gap,
            "cut_gap": cut_gap,
            "reason": result.reason,
            "ablation": ablation,
            "transcript": result.transcript,
        }
        append_log(out, record)


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Run batch evaluations.")
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--system", type=str, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/base.yaml"))
    parser.add_argument("--ablation", type=str, default=None)
    parser.add_argument("--ablations-config", type=Path, default=Path("configs/ablations.yaml"))
    parser.add_argument("--split", type=str, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)

    run(
        cache=args.cache,
        system=args.system,
        out=args.out,
        config_path=args.config,
        ablation=args.ablation,
        ablation_path=args.ablations_config,
        split=args.split,
    )


if __name__ == "__main__":
    main()
