
import gzip
from pathlib import Path


resource_dir = Path(__file__).resolve().parent / "_resources"


def from_gaf_lines(lines, qualified_only=True):
    """Read gene association entries
    Reference:
        http://www.geneontology.org/page/go-annotation-file-gaf-format-21
    """
    lines_iter = iter(lines)

    # Header
    fv_line = next(lines_iter)
    format_ver = fv_line.split(":")[1].strip()
    print(f"gaf-version: {format_ver}")
    annots = {}
    # Records
    for line in lines_iter:
        if line.startswith("!"):
            continue
        row = line.split("\t")
        uid = row[1]  # DB Object ID (= UniProt ID)
        if uid not in annots:
            annots[uid] = {
                "db_object_id": uid,
                "db_object_symbol": row[2],
                "db_object_name": row[9],
                "db_object_type": row[11],
                "annotation": {}
            }
        qualifiers = row[3].split("|")
        if qualified_only:
            if "NOT" in qualifiers:
                continue
        # Add GO annotation
        go_id = row[4]
        annots[uid]["annotation"][go_id] = {
            "go_id": go_id,
            "qualifier": qualifiers,
            "evidence_code": row[6],
        }
    return annots


def from_gaf(pathlike, **kwargs):
    with gzip.open(pathlike, "rt") as f:
        annot = from_gaf_lines(f, **kwargs)
    return annot


def from_resource(name, **kwargs):
    filename = f"{name}.gaf.gz"
    return from_gaf(resource_dir / filename, **kwargs)
