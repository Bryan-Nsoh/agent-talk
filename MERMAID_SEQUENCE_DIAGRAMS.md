# Sequence Diagrams (Mermaid Source)

These are the exact Mermaid definitions for the four sequence diagrams now rendered as vector PDFs and included in the paper. Drop them into a Mermaid live editor or render locally with mermaid-cli to review or tweak the flows.

Build locally (PDF output):

```
# Ensure mermaid-cli is installed
npm install -g @mermaid-js/mermaid-cli

# Render all diagrams to cert-talk-paper/figs/*.pdf
./scripts/build_diagrams.sh
```

Direct one-off command (example):

```
mmdc -i diagrams/seq_certtalk.mmd -o cert-talk-paper/figs/seq_certtalk.pdf -b transparent -w 1400
```

---

## CertTalk (ours)

```mermaid
sequenceDiagram
    autonumber
    participant A as Robot A (initiator)
    participant B as Robot B (responder)
    Note over A: Start with private map A
    A->>B: PATH_PROPOSE [PROOF] (~70-120 B)
    Note over B: Validate against B hazards
    alt Path valid
        B-->>A: PATH_CERT [PROOF + signed_by] (~70-120 B)
        A->>B: ACK (digest echo) (~16-30 B)
        Note over A,B: Fast path terminates (3 messages)
    else Path blocked
        B-->>A: NACK [CONFLICTS] (~15-40 B)
        A->>B: CUT_PROPOSE [PROOF cells,k,witness] (~100-130 B)
        B-->>A: CUT_CERT [PROOF + signed_by] (~110-130 B)
        A->>B: ACK (digest echo) (~60-70 B)
        Note over A,B: Cut path terminates (5 messages)
    end
```

---

## Send-All (map streaming)

```mermaid
sequenceDiagram
    autonumber
    participant A as Robot A (sender)
    participant B as Robot B (receiver)
    Note over A: Stream blocked indices in chunks
    A->>B: PROBE CHUNK #1 [RAW] (~180-200 B)
    B-->>A: ACK (chunk id) (~60-70 B)
    A->>B: PROBE CHUNK #2 [RAW] (~150-200 B)
    B-->>A: ACK
    A->>B: PROBE CHUNK #N [RAW] (final)
    Note over B: Build union A+B and certify
    B-->>A: PATH_CERT or CUT_CERT [PROOF] (~80-140 B)
    A->>B: ACK (digest echo) (~16-30 B)
```

---

## Greedy-Probe (hint-first)

```mermaid
sequenceDiagram
    autonumber
    participant A as Robot A
    participant B as Robot B
    A->>B: PATH_PROPOSE [PROOF] (~70-120 B)
    B-->>A: NACK [CONFLICTS] (~15-40 B)
    A->>B: PROBE [k<=6 cells] (~20-40 B)
    B-->>A: PROBE_REPLY [bits] (~15-30 B)
    A->>B: PATH_PROPOSE' or CUT_PROPOSE [PROOF]
    alt Valid
        B-->>A: PATH_CERT / CUT_CERT [PROOF]
        A->>B: ACK
    else Not valid yet
        A->>B: (repeat probe/guess loop)
    end
```

---

## Responder-MinCut (responder-led)

```mermaid
sequenceDiagram
    autonumber
    participant A as Robot A (initiator)
    participant B as Robot B (responder-led)
    Note over B: Compute min-cut on B map
    B-->>A: CUT_PROPOSE / CUT_CERT [PROOF] (~80-120 B)
    alt Insufficient
        A->>B: NACK [CONFLICTS] (~30-90 B)
        B-->>A: PROBE [k<=6] (~40-80 B)
        A->>B: PROBE_REPLY [bits] (~20-40 B)
        B-->>A: CUT_CERT (retry) [PROOF] (~80-130 B)
        A->>B: ACK
    else Accepted
        A->>B: ACK
    end
```

