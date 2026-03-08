# input/

Each file in this directory contains one section of the paper.
They are included in `paper.tex` via `\input{input/filename}` in the order listed below.

## Section files

| File                  | Section                |
|-----------------------|------------------------|
| `0_introduction.tex`  | Introduction           |
| `1_related_work.tex`  | Related Work           |
| `2_methodology.tex`   | Methodology            |
| `3_results.tex`       | Results                |
| `4_discussion.tex`    | Discussion             |
| `5_threats.tex`       | Threats to Validity    |
| `6_conclusion.tex`    | Conclusion             |
| `appendix.tex`        | Appendix (optional)    |

## Guidelines

- Keep each file focused on a single section.
- Start each file with a `\section{}` and `\label{}`.
- Use `\authorA{…}` / `\authorB{…}` inline todo notes for collaboration.
- Commit often — small, section-scoped commits make code review and merges easier.

## Adding or removing sections

1. Create (or delete) the `.tex` file here.
2. Add (or remove) the corresponding `\input{input/filename}` line in `paper.tex`.
