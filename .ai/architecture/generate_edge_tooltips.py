"""Regenere les metadonnees de navigation de chaque edge du diagramme :
- `source_label` : nom lisible du noeud `source`
- `target_label` : nom lisible du noeud `target`

Poses comme metadonnees ordinaires (au meme titre que `relation_type`), pas
comme tooltip : draw.io les liste automatiquement des qu'elles existent,
sans mecanisme special a maintenir.

Source de verite : les attributs `source`, `target` et `relation_type` deja
presents sur chaque edge, et l'attribut `label` de chaque node (titre en gras).
Ce script ne fait que DERIVER `source_label`/`target_label` a partir de cette
structure existante ; il ne cree, ne deplace et ne renomme jamais un noeud,
un edge, un id, un source/target ou un label metier. Les deux champs sont un
cache derive, pas une source de verite alternative : ils sont toujours
regeneres a partir des memes `source`/`target`, donc ne peuvent pas diverger
entre eux ni du graphe.

Ordre des attributs sur la balise <object> d'un edge, pour une lecture
naturelle "source -> relation -> target" :
    label, source_label, relation_type, target_label, kind, id

A relancer (idempotent) apres toute modification de source/target/label sur
IA_Diagramme_architecture.drawio, sous peine de laisser ces champs perimes.

Usage :
    python generate_edge_tooltips.py [chemin_du_fichier.drawio]
"""

import html
import re
import sys
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent / "IA_Diagramme_architecture.drawio"

OBJECT_TAG_RE = re.compile(r"<object\b[^>]*>")
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
BOLD_RE = re.compile(r"<b>(.*?)</b>", re.IGNORECASE | re.DOTALL)
TAG_STRIP_RE = re.compile(r"<[^>]+>")

# Ordre de lecture naturel ; toute cle absente de cette liste (aucune en
# pratique pour un edge de ce fichier) est simplement ajoutee a la fin.
EDGE_ATTR_ORDER = ["label", "source_label", "relation_type", "target_label", "kind", "id"]


def decode_label(raw_label: str) -> str:
    # Le fichier contient au moins un noeud dont l'esperluette a ete
    # double-echappee par l'editeur draw.io (&amp;amp;) ; deux passes
    # d'unescape restent un no-op sur un label deja simplement echappe.
    text = html.unescape(html.unescape(raw_label))
    match = BOLD_RE.search(text)
    title = match.group(1) if match else text
    title = TAG_STRIP_RE.sub(" ", title)
    return re.sub(r"\s+", " ", title).strip()


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_attrs(tag_text: str) -> dict:
    # dict() garde l'ordre de premiere apparition (Python 3.7+), utile pour
    # les cles qu'on ne reordonne pas explicitement.
    return dict(ATTR_RE.findall(tag_text))


def build_node_names(text: str) -> dict:
    names = {}
    for match in OBJECT_TAG_RE.finditer(text):
        attrs = parse_attrs(match.group(0))
        node_id = attrs.get("id", "")
        if node_id.startswith("node_") and "label" in attrs:
            names[node_id] = decode_label(attrs["label"])
    return names


def render_tag(attrs: dict) -> str:
    """Reconstruit <object ...> dans EDGE_ATTR_ORDER.

    Les valeurs deja presentes dans le fichier (label, relation_type, kind,
    id) sont reinjectees telles quelles : elles sont deja XML-echappees en
    entree, les re-echapper les corromprait (double encodage des entites).
    Seules les valeurs nouvellement calculees (source_label/target_label,
    du texte brut decode) doivent passer par xml_escape().
    """
    raw_only = {"source_label", "target_label"}
    ordered_keys = [k for k in EDGE_ATTR_ORDER if k in attrs]
    ordered_keys += [k for k in attrs if k not in ordered_keys]

    parts = []
    for key in ordered_keys:
        value = attrs[key]
        if key in raw_only:
            value = xml_escape(value)
        parts.append(f'{key}="{value}"')
    return "<object " + " ".join(parts) + ">"


def patch_edge_metadata(text: str, node_names: dict) -> tuple[str, list[dict]]:
    report = []
    edits = []  # (start, end, replacement)

    for match in OBJECT_TAG_RE.finditer(text):
        tag_text = match.group(0)
        attrs = parse_attrs(tag_text)
        edge_id = attrs.get("id", "")
        if not edge_id.startswith("edge_"):
            continue

        # source/target vivent sur le mxCell enfant, juste apres l'object.
        window_end = text.find("</object>", match.end())
        child = text[match.end():window_end] if window_end != -1 else ""
        src_match = re.search(r'source="(node_[a-zA-Z_0-9]+)"', child)
        tgt_match = re.search(r'target="(node_[a-zA-Z_0-9]+)"', child)
        if not src_match or not tgt_match:
            report.append({"id": edge_id, "status": "SKIPPED_NO_SOURCE_TARGET"})
            continue

        src_id, tgt_id = src_match.group(1), tgt_match.group(1)
        src_name = node_names.get(src_id, src_id)
        tgt_name = node_names.get(tgt_id, tgt_id)

        was_present = "source_label" in attrs and "target_label" in attrs

        new_attrs = dict(attrs)
        new_attrs.pop("tooltip", None)  # champ retire : plus de tooltip
        new_attrs["source_label"] = src_name
        new_attrs["target_label"] = tgt_name

        new_tag = render_tag(new_attrs)

        if new_tag != tag_text:
            edits.append((match.start(), match.end(), new_tag))
            report.append(
                {
                    "id": edge_id,
                    "status": "UPDATED" if was_present else "ADDED",
                    "source_label": src_name,
                    "relation_type": attrs.get("relation_type", ""),
                    "target_label": tgt_name,
                }
            )
        else:
            report.append({"id": edge_id, "status": "UNCHANGED"})

    new_text = text
    for start, end, replacement in sorted(edits, key=lambda e: e[0], reverse=True):
        new_text = new_text[:start] + replacement + new_text[end:]

    return new_text, report


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    original = path.read_text(encoding="utf-8", newline="")

    node_names = build_node_names(original)
    updated, report = patch_edge_metadata(original, node_names)

    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="")

    added = sum(1 for r in report if r["status"] == "ADDED")
    changed = sum(1 for r in report if r["status"] == "UPDATED")
    unchanged = sum(1 for r in report if r["status"] == "UNCHANGED")
    skipped = [r for r in report if r["status"] == "SKIPPED_NO_SOURCE_TARGET"]

    print(f"Nodes indexed: {len(node_names)}")
    print(f"Edges processed: {len(report)}")
    print(f"  source_label/target_label added:   {added}")
    print(f"  source_label/target_label updated: {changed}")
    print(f"  unchanged:                          {unchanged}")
    if skipped:
        print(f"  SKIPPED (no source/target found): {len(skipped)}")
        for r in skipped:
            print(f"    - {r['id']}")


if __name__ == "__main__":
    main()
