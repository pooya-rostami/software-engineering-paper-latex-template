"""
make.py — build a self-contained submission archive
====================================================
Produces a ZIP file (default: final.zip) containing a single flattened
paper.tex (all \input{} files inlined), all referenced figures, and the
required support files (style, bibliography, etc.).

Usage
-----
    python make.py               # uses defaults below
    python make.py --help        # show all options

Directory layout expected
-------------------------
    paper.tex
    preamble.tex
    biblio.bib
    input/
        0_introduction.tex
        1_related_work.tex
        ...
    Figures/
        fig1.pdf
        fig2.png
        ...
"""

import argparse
import os
import re
import shutil

# ── Configuration ─────────────────────────────────────────────────────────────

# Files that must be copied into the archive as-is.
REQUIRED_FILES = [
    "biblio.bib",
    "elsarticle.cls",
    "elsarticle-num.bst",
]

MAIN_FILE = "paper"          # no .tex extension
FIGURES_DIR = "Figures"      # folder that holds all figures

# Regex: capture filename inside {Figures/...} or {./Figures/...}
FIGURE_RE = re.compile(r"\{(?:\./)?Figures/([^\}]+)\}")

# Regex: capture filename inside \input{...}  (leading spaces allowed)
INCLUDE_TEX_RE = re.compile(r"^ *\\input\{([^\}]+)\}")

BASE_PATH = "./"
OUTPUT_PATH = "output"
ARCHIVE_NAME = "final"


# ── Helpers ───────────────────────────────────────────────────────────────────

def resolve_figure(base: str, output: str, raw_name: str) -> None:
    """Copy a figure file to the output directory, trying .pdf first."""
    source = os.path.join(base, FIGURES_DIR, raw_name)
    target = os.path.join(output, raw_name)
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    try:
        shutil.copyfile(source + ".pdf", target + ".pdf")
    except FileNotFoundError:
        shutil.copyfile(source, target)


def get_tex_lines(filepath: str, base: str, output: str) -> list[str]:
    """
    Read *filepath*.tex, recursively inline \\input{} calls, strip inline
    comments, and copy any referenced figures to *output*.
    """
    lines: list[str] = []
    full_path = os.path.join(base, filepath + ".tex")

    with open(full_path, encoding="utf-8") as fh:
        for line in fh:
            # ── Figure reference ──────────────────────────────────────────────
            fig_match = FIGURE_RE.search(line)
            if fig_match:
                # Flatten path: {Figures/name} → {name}
                line = FIGURE_RE.sub(r"{\1}", line)
                resolve_figure(base, output, fig_match.group(1))

            # ── Inlined \input ────────────────────────────────────────────────
            inc_match = INCLUDE_TEX_RE.search(line)
            if inc_match:
                included = inc_match.group(1)
                print(f"  → inlining  {included}  (from {filepath})")
                try:
                    lines.extend(get_tex_lines(included, base, output))
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"Could not find '{included}.tex' referenced in '{filepath}.tex'"
                    )
            else:
                # Strip inline comments but keep the newline
                lines.append(re.sub(r"(?<!\\)%.*", "%", line))

    return lines


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--main",    default=MAIN_FILE,   help="Root .tex file (no extension)")
    parser.add_argument("--output",  default=OUTPUT_PATH, help="Temporary output directory")
    parser.add_argument("--archive", default=ARCHIVE_NAME, help="Archive base name (no .zip)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Flatten paper.tex
    print(f"Flattening {args.main}.tex …")
    lines = get_tex_lines(args.main, BASE_PATH, args.output)
    out_tex = os.path.join(args.output, args.main + ".tex")
    with open(out_tex, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print(f"  → wrote {out_tex}")

    # Copy required support files
    missing = []
    for fname in REQUIRED_FILES:
        src = os.path.join(BASE_PATH, fname)
        dst = os.path.join(args.output, fname)
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            print(f"  → copied  {fname}")
        else:
            print(f"  ⚠  missing {fname} (skipped)")
            missing.append(fname)

    if missing:
        print("\nWarning: the following required files were not found:")
        for f in missing:
            print(f"  • {f}")
        print("Add them to the project root before submitting.\n")

    # Create ZIP archive
    archive_path = shutil.make_archive(args.archive, "zip", args.output)
    print(f"\nArchive created: {archive_path}")

    # Clean up temporary folder
    shutil.rmtree(args.output)
    print("Temporary output directory removed.")


if __name__ == "__main__":
    main()
