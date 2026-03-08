# response/

Reviewer response letter for the paper submission.
Lives as a self-contained sub-folder inside the paper repository.

## Files

```
response/
├── response.tex   ← Main document: editor + per-reviewer sections
├── preamble.tex   ← Packages and macros (response-specific, minimal)
├── make.py        ← Builds a self-contained response-final.zip
└── README.md
```

The bibliography (`biblio.bib`) is shared with the parent paper and is
referenced as `../biblio.bib` by default. No copy is kept here.

## Compile

```bash
pdflatex response && bibtex response && pdflatex response && pdflatex response
```

Or with latexmk:

```bash
latexmk -pdf response.tex
```

## Build a submission archive

```bash
python make.py
```

Produces `response-final.zip` with a flattened `response.tex` and a copy
of `biblio.bib`. Adjust `BIBLIO_PATH` in `make.py` if your bib file lives
elsewhere.

## Writing conventions

| Macro | Purpose |
|---|---|
| `\review{…}` | Paste the reviewer's original comment (renders in dark gray) |
| `\reply{…}` | Your response (renders in blue) |
| `\changed{…}` | Mark text changed in the manuscript — enable colour in `preamble.tex` |
| `\changedTo{…}` | Always renders in red (for fully rewritten passages) |
| `\say{…}` | Inline quote from the manuscript: `"…"` in italics |
| `\authorA{…}` | Internal draft note for Author A (disable via `todonotes` option) |

## Structure

Add one `\section*{Reviewer N}` block per reviewer, with
`\subsection*{Major comments}` and `\subsection*{Minor comments}` as needed.
Keep the editor block at the top. Add a `\section*{Reviewer 3}` block by
copy-pasting the Reviewer 2 block if there is a third reviewer.
