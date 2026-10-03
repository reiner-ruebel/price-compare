"""Build an explicit-file delivery ZIP; never include private run/session captures."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--result", type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    output = root.parent / "output"
    output.mkdir(exist_ok=True)
    result = json.loads(args.result.read_text(encoding="utf-8"))
    for key in ("quote_reference", "run_id", "input_sha256"):
        result.pop(key, None)
    result["sample_notice"] = "Redacted real result observed on 7 September 2026. Not a prediction of the next run."
    entries = {name: (root / name).read_bytes() for name in (
        "README.md", "collect_quote.py", "observe_quote.py", "case-owner-example.json",
        "requirements.txt", "requirements-browser.txt", "test_collect_quote.py",
    )}
    entries["FINDINGS.md"] = (root.parent / "docs/lemonade-investigation-results-2026-09-07.md").read_bytes()
    entries["sample-result.json"] = json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8")
    entries["SHA256SUMS.txt"] = "\n".join(f"{hashlib.sha256(body).hexdigest()}  {name}" for name, body in entries.items()).encode("ascii") + b"\n"
    destination = output / "lemonade-worker-poc-2026-09-07.zip"
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for name, body in entries.items():
            archive.writestr(name, body)
    with ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(entries)
        assert not any("private" in name or "runs/" in name or name.startswith(".venv/") for name in archive.namelist())
    print(destination)
    print("Files:", len(entries), "Bytes:", destination.stat().st_size)
    print("SHA256:", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
