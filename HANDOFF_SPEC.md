# External Expert Handoff (Auto‑Insert, Raw‑Only, Self‑Contained)

## Why
- One file contains raw results, sample data, full code that produced them, and exact reproduction commands — no repo browsing.
- Final artifact is path‑free and portable: all referenced content is inlined.
- Inlining is automated via include directives, so there’s no manual copy/paste.

## What To Include (Raw)
- Results: latest summary tables (CSV/JSON)
- Data samples: small slice of the dataset (e.g., first 3 JSONL lines)
- Transcripts/logs: representative raw records (reachable + unreachable or success + failure)
- Reproduction commands: exact shell lines that rebuilt and reran
- Full code: core logic modules (verbatim) that define behavior
- Optional: configs used for the run

## Principles
- Deterministic: pin seeds, versions, and commands
- Path‑free final: no file paths in the final handoff; everything is inlined
- Raw‑first: avoid narrative; raw tables/logs/code are the source of truth
- Verifiable: all numbers in prose (if any) appear in tables below

## Include Directives (Template Language)
Use pseudo‑XML tags in a template Markdown. The expander replaces each with a fenced block containing current file contents (or a filtered slice).

Attributes:
- `path`: repo‑relative file path
- `lang`: fence language (default `text`)
- `block`: `code` (fenced), `text` (fenced), or `none` (raw, no fence)
- `head`: include first N lines
- `tail`: include last N lines
- `jsonl_match`: key=value (comma‑separated) to include the first JSONL line that matches
- `bytes`: include up to N bytes (safety cap)

Examples:
- <include path="runs/latest_summary.csv" lang="text" block="code"/>
- <include path="data/cache.jsonl" lang="json" head="3" block="code"/>
- <include path="runs/system.jsonl" jsonl_match="seed=123,split=test" block="code"/>
- <include path="src/core/engine.py" lang="python" block="code"/>

## Handoff Template Skeleton (EXPERT_HANDOFF.template.md)
Copy into your repo and edit paths; the expander will produce EXPERT_HANDOFF.md.

```
Last updated: <UTC_TIMESTAMP>

## Summary (raw)
<include path="runs/latest_summary.csv" lang="text" block="code"/>

## Dataset sample (raw)
<include path="data/cache.jsonl" lang="json" head="3" block="code"/>

## Representative transcripts/logs (raw)
<include path="runs/system.jsonl" jsonl_match="seed=REACHABLE_SEED" block="code"/>
<include path="runs/system.jsonl" jsonl_match="seed=UNREACHABLE_SEED" block="code"/>

## Reproduction commands (raw)
```
<your exact shell here>
```

## Code (verbatim, raw)
<include path="src/core/messages.py" lang="python" block="code"/>
<include path="src/core/protocol.py" lang="python" block="code"/>
<include path="src/env/grid.py" lang="python" block="code"/>
<include path="src/oracle/oracle.py" lang="python" block="code"/>
<include path="src/oracle/flow.py" lang="python" block="code"/>
<include path="src/agents/agent_a.py" lang="python" block="code"/>
<include path="src/agents/agent_b.py" lang="python" block="code"/>
<include path="src/runners/simulate.py" lang="python" block="code"/>
<include path="src/runners/batch_eval.py" lang="python" block="code"/>

## Decisions requested (raw bullets)
- Approve/deny: <short decision one>
- Approve/deny: <short decision two>
- Guidance: <one sentence question>
```

## Expander (scripts/expand_includes.py)
Drop‑in script to resolve `<include …/>` and write a path‑free EXPERT_HANDOFF.md.

```python
#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

TAG = re.compile(r'<include\s+([^/>]+?)\s*/\s*>')

def parse_attrs(s: str) -> dict:
    attrs = {}
    for m in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', s):
        attrs[m.group(1)] = m.group(2)
    return attrs

def load_text(p: Path, head=None, tail=None, bytes_limit=None):
    if bytes_limit:
        return p.read_bytes()[:int(bytes_limit)].decode('utf-8', errors='replace')
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines(keepends=True)
    if head: return ''.join(lines[:int(head)])
    if tail: return ''.join(lines[-int(tail):])
    return ''.join(lines)

def jsonl_match(p: Path, cond: str):
    want = dict(kv.split('=') for kv in cond.split(','))
    with p.open('r', encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not line.strip(): continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if all(str(obj.get(k)) == v for k, v in want.items()):
                return line
    return ""

def fence(lang: str, body: str, kind: str):
    if kind == 'none': return body
    return f"```{lang}
{body.rstrip()}
```
"

def expand_one(root: Path, attrs: dict) -> str:
    path = root / attrs.get('path', '')
    lang = attrs.get('lang', 'text')
    block = attrs.get('block', 'code')
    head = attrs.get('head')
    tail = attrs.get('tail')
    bytes_limit = attrs.get('bytes')
    jmatch = attrs.get('jsonl_match')

    if jmatch:
        body = jsonl_match(path, jmatch)
    else:
        body = load_text(path, head=head, tail=tail, bytes_limit=bytes_limit)
    return fence(lang, body, block)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    ap.add_argument('--root', default='.')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    text = Path(args.inp).read_text(encoding='utf-8', errors='replace')

    def repl(m):
        attrs = parse_attrs(m.group(1))
        return expand_one(root, attrs)

    out = TAG.sub(repl, text)
    Path(args.outp).write_text(out, encoding='utf-8')

if __name__ == '__main__':
    main()
```

## How To Use
1) Author `EXPERT_HANDOFF.template.md` with include tags
2) Run: `uv run python scripts/expand_includes.py --in EXPERT_HANDOFF.template.md --out EXPERT_HANDOFF.md`
3) Share only `EXPERT_HANDOFF.md` (path‑free, self‑contained)

## Reviewer Prompts (General)
- Bytes/rounds: Remove redundant turns/fields to hit targets while preserving interpretability?
- Schema: Accept compact/short keys for final run?
- Baselines: Keep/replace proposed baseline given success rate?
- Outliers: Approve stop rule at α·cap when no certificate yet?

## Checklist Before Send
- Replace timestamps/paths in template
- Confirm summary table matches raw run data
- Transcripts are complete JSON records
- Core code files included in full
- Re-run expander; spot check `EXPERT_HANDOFF.md`
- Final doc contains no file paths
