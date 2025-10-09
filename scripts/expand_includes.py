#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

TAG = re.compile(r'<include\b([^>]*)/\s*>')

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
    want = {}
    for kv in cond.split(','):
        if not kv.strip():
            continue
        k, v = kv.split('=', 1)
        want[k.strip()] = v.strip()
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
    return f"```{lang}\n{body.rstrip()}\n```\n"

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

