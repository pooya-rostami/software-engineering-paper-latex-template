# Figures

Place all paper figures in this directory.

## Naming convention

Use lowercase, hyphen-separated names that reflect the figure content:

```
fig_overview.pdf
fig_rq1_results.pdf
fig_comparison_table.png
```

## Format

- **PDF** (vector) is strongly preferred — it scales without quality loss.
- **PNG** is acceptable for screenshots, raster plots, or photos.
- Avoid JPEG for diagrams and charts (compression artefacts are visible in print).

## Referencing in LaTeX

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\figsize]{./Figures/fig_overview}
  \caption{Caption text here.}
  \label{fig:overview}
\end{figure}
```

Use `\fig{fig:overview}` (defined in `preamble.tex`) for cross-references.

## Note on `make.py`

The build script copies every figure referenced in the source into the
submission archive and rewrites the path from `./Figures/name` to just `name`,
so the archive is self-contained and flat.
