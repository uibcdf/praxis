"""Map installed-package coverage to identical committed sources without changing hits."""

import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize(root, report, observation, manifest, output):
    if observation["source_commit"] != manifest["source_commit"]:
        raise ValueError("Coverage observation belongs to another candidate")
    if observation["artifact_sha256"] != manifest["conda_sha256"]:
        raise ValueError("Coverage observation belongs to another artifact")
    package = Path(observation["import_path"])
    tree = ET.parse(report)
    count = 0
    for group in tree.findall("packages/package"):
        names = set()
        for item in group.findall("classes/class"):
            path = Path(item.attrib["filename"])
            if not path.is_absolute() or not path.is_relative_to(package):
                raise ValueError("Coverage contains an unexpected installed path")
            relative = path.relative_to(package)
            name = "praxis/" + relative.as_posix()
            source = Path(root) / "src" / name
            expected = manifest["runtime_hashes"].get(name)
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                raise ValueError("Coverage source differs from installed resource: " + name)
            item.set("filename", "src/" + name)
            names.add(
                "praxis"
                + (
                    "." + relative.parent.as_posix().replace("/", ".")
                    if relative.parent != Path(".")
                    else ""
                )
            )
            count += 1
        if len(names) != 1:
            raise ValueError("Ambiguous coverage package grouping")
        group.set("name", names.pop())
    if count == 0:
        raise ValueError("Coverage report has no measured Praxis files")
    sources = tree.getroot().find("sources")
    if sources is None:
        raise ValueError("Coverage report has no sources element")
    sources.clear()
    ET.SubElement(sources, "source").text = "."
    tree.write(output, encoding="utf-8", xml_declaration=True)
    return {
        "source_commit": manifest["source_commit"],
        "files": count,
        "artifact_sha256": observation["artifact_sha256"],
        "original_sha256": hashlib.sha256(Path(report).read_bytes()).hexdigest(),
        "normalized_sha256": hashlib.sha256(Path(output).read_bytes()).hexdigest(),
        "scope": "Path mapping of identical installed sources; coverage hits/statistics unchanged",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("observation", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if actual != manifest["source_commit"]:
        raise ValueError("Coverage report comes from another checkout commit")
    result = normalize(
        Path(__file__).resolve().parents[1],
        args.report,
        json.loads(args.observation.read_text()),
        manifest,
        args.output,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
