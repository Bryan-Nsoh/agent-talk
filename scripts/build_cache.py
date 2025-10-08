#!/usr/bin/env python3
"""Convenience wrapper for generating caches."""
from __future__ import annotations

import argparse
from pathlib import Path

from agent_talk.env.generator import main as generator_main


def parse_args() -> list[str]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--out", type=Path, default=Path("data/cache.jsonl"))
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--size", type=int, default=10)
    parser.add_argument("--seed", type=int, default=123)
    args = parser.parse_args()
    return [
        "--out",
        str(args.out),
        "--n",
        str(args.n),
        "--size",
        str(args.size),
        "--seed",
        str(args.seed),
    ]


def main() -> None:
    generator_main(parse_args())


if __name__ == "__main__":
    main()
