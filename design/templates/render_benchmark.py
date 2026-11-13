"""Write a Seidelbots benchmark page from a results dict.

Standard library only. Call it at the end of an evaluation script:

    from render_benchmark import render
    render(results, "docs/benchmarks")   # -> docs/benchmarks/<model>_<run id>.html

or from the shell, with a results JSON written by the evaluation:

    python render_benchmark.py results.json docs/benchmarks

`results` follows the run-data schema documented at the top of
benchmark.html (task, model, run, code, baselines, benchmarks, ...).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TEMPLATE = Path(__file__).with_name("benchmark.html")
BLOCK = re.compile(
    r'(<script type="application/json" id="run-data">)(.*?)(</script>)', re.S
)


def _git(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def _fill_defaults(data: dict) -> dict:
    """Fill run id, date and code.commit/repo from the clock and git when missing."""
    run = data.setdefault("run", {})
    now = datetime.now().astimezone()
    run.setdefault("date", now.isoformat(timespec="seconds"))
    run.setdefault("id", now.strftime("%Y%m%d-%H%M"))
    run.setdefault("generator", Path(sys.argv[0]).name or "render_benchmark.py")

    code = data.setdefault("code", {})
    code.setdefault("commit", _git("rev-parse", "--short", "HEAD"))
    if "repo" not in code:
        url = _git("config", "--get", "remote.origin.url") or ""
        m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
        if m:
            code["repo"] = m.group(1)
    if _git("status", "--porcelain"):
        run.setdefault("notes", "Working tree had uncommitted changes when this ran.")
    return data


def render(data: dict, out_dir: str | Path, template: str | Path = TEMPLATE, filename: str | None = None) -> Path:
    data = _fill_defaults(dict(data))
    html = Path(template).read_text(encoding="utf-8")
    # "</" inside the JSON would close the <script> tag early
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html, count = BLOCK.subn(lambda m: f"{m.group(1)}\n{payload}\n{m.group(3)}", html, count=1)
    if count != 1:
        raise ValueError("run-data block not found in template")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    model = re.sub(r"[^A-Za-z0-9._-]+", "-", data.get("model", {}).get("name", "model"))
    path = out_dir / (filename or f"{model}_{data['run']['id']}.html")
    path.write_text(html, encoding="utf-8")
    return path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python render_benchmark.py results.json OUT_DIR")
    results = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(render(results, sys.argv[2]))
