"""Generate the code reference pages.

Source: https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""

from pathlib import Path

import mkdocs_gen_files

SRC = "src"

for path in sorted(Path(SRC).rglob("*.py")):
    module_path = path.relative_to(SRC).with_suffix("")
    doc_path = path.relative_to(SRC).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)

    if parts[-1] == "__init__":
        continue
    if parts[-1] == "__main__":
        continue

    with mkdocs_gen_files.open(full_doc_path, mode="w") as fd:
        print("::: " + ".".join(parts), file=fd)

    mkdocs_gen_files.set_edit_path(name=full_doc_path, edit_name=path)
