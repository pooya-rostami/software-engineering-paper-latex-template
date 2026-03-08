"""
make.py — build a self-contained submission archive for the response letter
===========================================================================
Produces a ZIP file (default: response-final.zip) containing a single
flattened response.tex (all \\input{} calls inlined) and the required
support files.

The response letter shares biblio.bib with the parent paper folder.
By default this script looks for it one level up (../biblio.bib).
Adjust BIBLIO_PATH below if your layout differs.

Usage
-----
    python make.py               # uses defaults below
    python make.py --help        # show all options

Expected directory layout
--------------------------
    response/
        response.tex
        preamble.tex
        make.py          ← this file
    biblio.bib           ← shared with the paper (one level up)
"""

import argparse
import os
import re
import shutil

# ── Configuration ─────────────────────────────────────────────────────────────

MAIN_FILE   = "response"     # no .tex extension
BASE_PATH   = "./"
OUTPUT_PATH = "output"
ARCHIVE_NAME = "response-final"

# Path to the shared bib file (relative to this script's location).
# Change to "biblio.bib" if you keep a local copy inside the response/ folder.
BIBLIO_PATH = "../biblio.bib"

# Extra files to bundle (add .sty / .cls files here if the journal requires them)
REQUIRED_FILES = [
    BIBLIO_PATH,
]

# Regex: inline \input{filename}  (leading spaces allowed, no extension assumed)
INCLUDE_TEX_RE = re.compile(r"^ *\\input\{([^\}]+)\}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_tex_lines(filepath: str) -> list:
    """
    Read *filepath*.tex and recursively inline any \\input{} calls.
    Inline comments are stripped (replaced with a bare %).
    """
    lines = []
    full_path = os.path.join(BASE_PATH, filepath + ".tex")

    with open(full_path, encoding="utf-8") as fh:
        for line in fh:
            inc = INCLUDE_TEX_RE.search(line)
            if inc:
                included = inc.group(1)
                print(f"  → inlining  {included}  (from {filepath})")
                try:
                    lines.extend(get_tex_lines(included))
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"Could not find '{included}.tex' referenced in '{filepath}.tex'"
                    )
            else:
                # Strip inline comments but preserve the newline
                lines.append(re.sub(r"(?<!\\)%.*", "%", line))

    return lines


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--main",    default=MAIN_FILE,    help="Root .tex file (no extension)")
    parser.add_argument("--output",  default=OUTPUT_PATH,  help="Temporary output directory")
    parser.add_argument("--archive", default=ARCHIVE_NAME, help="Archive base name (no .zip)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Flatten response.tex
    print(f"Flattening {args.main}.tex …")
    lines = get_tex_lines(args.main)
    out_tex = os.path.join(args.output, args.main + ".tex")
    with open(out_tex, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print(f"  → wrote {out_tex}")

    # Copy required support files
    missing = []
    for src_path in REQUIRED_FILES:
        fname = os.path.basename(src_path)
        dst   = os.path.join(args.output, fname)
        if os.path.exists(src_path):
            shutil.copyfile(src_path, dst)
            print(f"  → copied  {fname}  (from {src_path})")
        else:
            print(f"  ⚠  missing {src_path} (skipped)")
            missing.append(src_path)

    if missing:
        print("\nWarning: the following files were not found:")
        for f in missing:
            print(f"  • {f}")
        print("Ensure biblio.bib exists at the expected path before submitting.\n")

    # Create ZIP archive
    archive_path = shutil.make_archive(args.archive, "zip", args.output)
    print(f"\nArchive created: {archive_path}")

    # Clean up
    shutil.rmtree(args.output)
    print("Temporary output directory removed.")


if __name__ == "__main__":
    main()
