# LaTeX Paper Template

A clean, modular template for writing academic papers with `elsarticle` (Elsevier), structured for collaborative writing and easy submission packaging.

## Repository layout

```
.
├── paper.tex          ← Root document (title, authors, abstract, section order)
├── preamble.tex       ← All packages, macros, and style definitions
├── biblio.bib         ← BibTeX bibliography database
├── make.py            ← Build script: produces a self-contained submission ZIP
│
├── input/             ← One .tex file per paper section
│   ├── 0_introduction.tex
│   ├── 1_related_work.tex
│   ├── 2_methodology.tex
│   ├── 3_results.tex
│   ├── 4_discussion.tex
│   ├── 5_threats.tex
│   ├── 6_conclusion.tex
│   └── appendix.tex   ← Uncomment \input in paper.tex to include
│
└── Figures/           ← All figures (.pdf preferred, .png/.jpg accepted)
    └── README.md
```

## Quickstart

### 1. Compile locally (latexmk recommended)

```bash
latexmk -pdf paper.tex
```

Or with `pdflatex` manually:

```bash
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

### 2. Build a submission archive

```bash
python make.py
```

This produces `final.zip` containing a flattened `paper.tex` (all `\input{}` calls inlined), all referenced figures, and the required support files. The temporary build folder is removed automatically.

Options:

```
--main     root .tex file (default: paper)
--output   temporary directory (default: output)
--archive  archive base name (default: final)
```

### 3. Required support files (not tracked by git)

Download from the journal/conference and place in the project root:

| File                  | Purpose                        |
|-----------------------|--------------------------------|
| `elsarticle.cls`      | Elsevier document class        |
| `elsarticle-num.bst`  | Numbered bibliography style    |

## Writing conventions

- **One section per file** in `input/` — this keeps diffs small and merges clean.
- **Author notes** use `\authorA{…}`, `\authorB{…}`, etc. (defined in `preamble.tex`). Disable all notes for the final version by switching to `\usepackage[disable]{todonotes}`.
- **Change tracking**: wrap revised text with `\changed{…}` or `\changedTo{…}`.
- **Figures**: save in `Figures/` as `fig_name.pdf` (vector preferred). Reference as `\includegraphics{./Figures/fig_name}`.
- **Cross-references**: use `\fig{}`, `\tab{}`, `\sect{}`, `\listing{}` shorthands.

## Customising for a new paper

1. Update `paper.tex`: title, authors, affiliations, journal name, section list.
2. Update `preamble.tex`: rename author note commands, add domain-specific macros.
3. Replace `biblio.bib` with your references.
4. Add / rename section files in `input/` and update the `\input{}` calls in `paper.tex`.
