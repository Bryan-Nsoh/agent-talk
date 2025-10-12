# Writing Workflow Upgrade Tasks

## 1. Extract Structural Heuristics from a Reference Paper
- **Input:** Provide a well-written research paper (e.g., Google/DeepMind publication) that demonstrates effective layout, float handling, narrative flow, section sequencing, typography.
- **Process:**
  - Create a high-level outline: section order, approximate lengths, positioning of related work, conclusions, appendices.
  - Record how floats (figures/tables) are introduced, referenced, and kept near their sections; note use of `ef`, `
eedspace`, barriers, captions.
  - Capture narrative devices: intro hook, transitions, use of examples or intuition callouts, how limitations are framed, where future work sits.
  - Note typography/format conventions: callouts, inline math style, footnotes, bullet usage, table styling, figure captions.
  - Identify “reader guidance” patterns: sentences pointing to figures, summary sentences before/after tables, reminders in text about where to find supporting artifacts.
  - Identify missing pieces from our current repo (where we fall short) and opportunities to adopt those heuristics.
- **Output:**
  - Create `notes/reference-paper-heuristics.md` summarizing findings (outline, bullet list of rules, verbatim examples if helpful).
  - Add any emblematic snapshots (screenshots/snips) in `notes/reference-figures/` if visuals clarify layout.

## 2. Codify Heuristics into Writing Workflow
- **Input:** `notes/reference-paper-heuristics.md` from Task 1.
- **Process:**
  - Translate heuristics into concrete rules the writing agent must follow (e.g., “Before each major figure insert ‘Figure X shows…’ sentence,” “Use `\FloatBarrier` after figures to prevent drift,” “Limit intuition boxes to sections containing new mental models”).
  - Incorporate float-spacing guidance (blank space vs. figure placement, trimming whitespace in diagrams) based on findings.
- **Output:**
  - Update `agents.md` under the writing mode section with subsections: “Section Structure,” “Float Discipline,” “Narrative Flow,” “Typography,” “Verification Checklist.”
  - Include actionable checklists or macros for the writing agent.

## 3. Verify and Bake Into Workflow
- **Process:**
  - Run through a short writing sprint applying the new rules to a sample section (e.g., update a documentation chapter) to ensure the instructions are usable.
  - Record any friction points or missing rules; adjust `agents.md` accordingly.
  - Announce the new workflow in the repository changelog or README if needed.

---
**Status Tracking:**
- [ ] Task 1: Reference paper selected and heuristics extracted.
- [ ] Task 2: Heuristics codified in `agents.md`.
- [ ] Task 3: Trial run completed and workflow validated.
