#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["markdown>=3.5", "pyyaml>=6"]
# ///
"""Relatório técnico em HTML a partir de um markdown, no template ``design/templates/technical-report.html``.

Ferramenta avulsa: roda de qualquer repositório de projeto, sem instalar nada (o ``uv`` resolve as
dependências). O HTML sai ao lado do markdown; repositório e commit vêm do git da pasta dele.
Modelo comentado: ``design/tools/report-example.md``.

    uv run ~/Projetos/git/seidelbots-blog/design/tools/render_report.py docs/reports/meu-relatorio.md

* Cada ``##`` vira uma seção numerada (e entra no sumário lateral); ``###`` fica dentro dela.
* Tabelas ganham a moldura do template; colunas alinhadas à direita (``---:``) viram números.
  Um parágrafo logo depois que começa com ``**Table N.**`` vira a legenda.
* Blocos de código ganham a barra com o nome da linguagem e o botão de copiar.
* ``> [!NOTE]`` e ``> [!WARNING]`` viram as caixas de nota e de ressalva.
* ``![alt](figura.png "Figure 1. Legenda")`` vira figura com legenda.
* Front matter: ``title``, ``abstract``, ``number``, ``version``, ``status`` (draft | final), ``author``,
  ``published``, ``updated``, ``project``, ``license``, ``blog``, ``stats`` (lista de
  ``{value, label}``), ``highlights``, ``changelog`` (lista de ``{version, date, note}``).
  A seção de citação (BibTeX) é gerada.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from datetime import date
from pathlib import Path

import markdown
import yaml

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "technical-report.html"


def git(folder: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(folder), *args], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def repo_info(folder: Path) -> dict:
    """``repo`` (owner/nome no GitHub) e ``commit`` curto do repositório onde está o markdown."""
    url = git(folder, "config", "--get", "remote.origin.url") or ""
    match = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return {"repo": match.group(1) if match else None, "commit": git(folder, "rev-parse", "--short", "HEAD")}


def embed_json(data) -> str:
    """JSON seguro dentro de ``<script>``: ``</`` fecharia a tag antes da hora."""
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
CALLOUTS = {"NOTE": ("note", "Note"), "TIP": ("note", "Tip"), "WARNING": ("warn", "Caveat"),
            "CAUTION": ("warn", "Caveat"), "IMPORTANT": ("warn", "Important")}


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "secao"


def convert_body(md: str) -> tuple[str, list[str]]:
    """Markdown -> seções ``.sec`` numeradas. Devolve o HTML e os títulos."""
    chunks = re.split(r"^## +(.+)$", md, flags=re.M)
    intro, pairs = chunks[0], list(zip(chunks[1::2], chunks[2::2]))
    out, titles, used = [], [], set()
    if intro.strip():
        out.append(f'<div class="intro">{blocks(intro)}</div>')
    for n, (title, body) in enumerate(pairs, 1):
        anchor = slugify(title)
        while anchor in used:
            anchor += "-x"
        used.add(anchor)
        titles.append(title.strip())
        out.append(f'<section class="sec" id="{anchor}">\n<h2><span class="n">{n}</span>{inline(title.strip())}</h2>\n'
                   f"{blocks(body)}\n</section>")
    return "\n\n".join(out), titles


def inline(text: str) -> str:
    return markdown.markdown(text).removeprefix("<p>").removesuffix("</p>")


def blocks(md: str) -> str:
    out = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
                            output_format="html")
    # callouts: > [!NOTE] ...
    def callout(m: re.Match) -> str:
        inner = m.group(1)
        kind = re.match(r"\s*<p>\[!(\w+)\]\s*", inner)
        if not kind or kind.group(1).upper() not in CALLOUTS:
            return m.group(0)
        cls, label = CALLOUTS[kind.group(1).upper()]
        inner = inner[:kind.start()] + "<p>" + inner[kind.end():]
        inner = re.sub(r"<p>\s*</p>", "", inner)
        return f'<div class="callout {cls}"><span class="tag">{label}</span>{inner}</div>'
    out = re.sub(r"<blockquote>(.*?)</blockquote>", callout, out, flags=re.S)
    # código
    def code(m: re.Match) -> str:
        lang = m.group(1) or "text"
        return (f'<div class="code"><div class="bar-top"><span>{esc(lang)}</span>'
                f'<button type="button" data-copy>copy</button></div><pre>{m.group(2)}</pre></div>')
    out = re.sub(r'<pre><code(?: class="language-([\w+-]+)")?>(.*?)</code></pre>', code, out, flags=re.S)
    # tabelas
    out = re.sub(r'<(td|th) style="text-align: right;">', r'<\1 class="num">', out)
    out = re.sub(r'<(td|th) style="text-align: (?:left|center);">', r"<\1>", out)
    out = re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', out, flags=re.S)
    out = re.sub(r"<p><strong>(Table \d+\.)</strong>", r'<p class="table-note"><b>\1</b>', out)
    # figuras
    def figure(m: re.Match) -> str:
        attrs = m.group(1)
        title = re.search(r'title="([^"]*)"', attrs)
        caption = ""
        if title:
            cap = html.unescape(title.group(1))
            head = re.match(r"((?:Figure|Figura) \d+\.)\s*", cap)
            caption = (f"<figcaption><b>{esc(head.group(1))}</b> {esc(cap[head.end():])}</figcaption>" if head
                       else f"<figcaption>{esc(cap)}</figcaption>")
            attrs = attrs.replace(title.group(0), "")
        return f"<figure><img{attrs}>{caption}</figure>"
    out = re.sub(r"<p><img([^>]*?)\s*/?></p>", figure, out)
    return out


def read_time(text: str) -> str:
    return f"{max(1, round(len(text.split()) / 220))} min"


def head_html(meta: dict, words: str) -> str:
    status = str(meta.get("status", "draft")).lower()
    number = " · ".join(esc(x) for x in (meta.get("number"), meta.get("version") and f"v{meta['version']}") if x)
    rows = [("Author", esc(meta.get("author", "Seidel")), False),
            ("Published", esc(meta.get("published", date.today().isoformat())), False),
            ("Updated", esc(meta.get("updated") or meta.get("published") or date.today().isoformat()), False),
            ("Read time", read_time(words), False),
            ("Repository", '<a data-bind="repoUrl:href" data-text="repo" href="#">repo</a>', True),
            ("Commit", '<a data-bind="treeUrl:href" data-text="short" href="#">commit</a>', True),
            ("Project", esc(meta.get("project", "code-language-model")), True),
            ("License", esc(meta.get("license", "MIT")), False)]
    dl = "\n".join(f'    <div><dt class="eyebrow">{k}</dt><dd{" class=\"mono\"" if mono else ""}>{v}</dd></div>'
                   for k, v, mono in rows)
    blog = '\n    <a class="btn" data-bind="blog:href" href="#">Blog post →</a>' if meta.get("blog") else ""
    return f"""<div class="doc-top">
  <span class="mono"><a href="https://seidelbots.com">Seidelbots</a> · technical report{' · ' + number if number else ''}</span>
  <span class="tag {'final' if status == 'final' else 'draft'}">{'Final' if status == 'final' else 'Draft'}</span>
</div>

<section class="head">
  <h1>{esc(meta['title'])}</h1>
  <p class="dek">{inline(str(meta.get('abstract', '')))}</p>
  <dl class="meta">
{dl}
  </dl>
  <div class="actions">
    <button class="btn" type="button" id="open-code" aria-haspopup="dialog">Code at <span class="btn-mono" data-text="short">commit</span></button>{blog}
    <button class="btn" type="button" onclick="window.print()">Save as PDF</button>
  </div>
</section>

"""


def tldr_html(meta: dict) -> str:
    stats, highlights = meta.get("stats") or [], meta.get("highlights") or []
    if not stats and not highlights:
        return ""
    s = "".join(f'<div class="stat"><b>{esc(x["value"])}</b><span>{inline(str(x["label"]))}</span></div>' for x in stats)
    h = "".join(f"<li>{inline(str(x))}</li>" for x in highlights)
    return (f'<div class="tldr"><p class="eyebrow">At a glance</p>'
            f'{f"<div class=\"stats\">{s}</div>" if s else ""}{f"<ul>{h}</ul>" if h else ""}</div>\n')


def extra_sections(meta: dict, start: int) -> str:
    """Citação (BibTeX) e changelog, numeradas depois das seções do markdown."""
    year = str(meta.get("published", date.today().isoformat()))[:4]
    key = "seidel" + year + slugify(meta["title"]).split("-")[0]
    bib = (f"@techreport{{{key},\n  title       = {{{esc(meta['title'])}}},\n  author      = {{{esc(meta.get('author', 'Seidel'))}}},\n"
           f"  institution = {{Seidelbots}},\n" + (f"  number      = {{{esc(meta['number'])}}},\n" if meta.get("number") else "")
           + f"  year        = {{{year}}},\n  url         = {{<span data-text=\"repoUrl\"></span>}},\n"
           f"  note        = {{Code at commit <span data-text=\"short\"></span>}}\n}}")
    out = (f'<section class="sec" id="cite">\n<h2><span class="n">{start}</span>Citing this report</h2>\n'
           f'<div class="code"><div class="bar-top"><span>bibtex</span><button type="button" data-copy>copy</button></div>'
           f"<pre>{bib}</pre></div>\n</section>\n")
    changes = meta.get("changelog") or []
    if changes:
        rows = "".join(f'<div><span class="v">{esc(c.get("version", ""))}</span><span class="d">{esc(c.get("date", ""))}</span>'
                       f'<span>{inline(str(c.get("note", "")))}</span></div>' for c in changes)
        out += (f'<section class="sec" id="changelog">\n<h2><span class="n">{start + 1}</span>Changelog</h2>\n'
                f'<div class="changelog">{rows}</div>\n</section>\n')
    return out


def render(source: str | Path, out: str | Path | None = None) -> Path:
    source = Path(source)
    text = source.read_text(encoding="utf-8")
    match = FRONT.match(text)
    meta = yaml.safe_load(match.group(1)) if match else {}
    body_md = text[match.end():] if match else text
    if "title" not in meta:
        raise SystemExit(f"{source}: o front matter precisa de 'title'")
    body, titles = convert_body(body_md)
    page = TEMPLATE.read_text(encoding="utf-8")
    info = repo_info(source.resolve().parent)
    config = {"repo": info["repo"] or "", "commit": info["commit"] or "main",
              "blog": meta.get("blog") or "https://seidelbots.com"}
    replacements = [
        (r"<title>.*?</title>", f"<title>{esc(meta['title'])} · Seidelbots</title>"),
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{esc(re.sub(r"[*_`]", "", str(meta.get("abstract", ""))))}">'),
        (r"<!-- =+ TITLE BLOCK =+ -->.*?(?=<div class=\"body\">)", head_html(meta, body_md)),
        (r"(<article>).*?(</article>)", None),
        (r"<span>Seidelbots · technical report [^<]*</span>",
         f"<span>Seidelbots · technical report{' ' + esc(meta['number']) if meta.get('number') else ''}</span>"),
        (r"var REPORT = \{.*?\};", "var REPORT = " + embed_json(config) + ";"),
    ]
    article = tldr_html(meta) + body + "\n" + extra_sections(meta, len(titles) + 1)
    for pattern, new in replacements:
        if new is None:
            page, n = re.subn(pattern, lambda m: f"{m.group(1)}\n{article}\n{m.group(2)}", page, count=1, flags=re.S)
        else:
            page, n = re.subn(pattern, lambda m, new=new: new, page, count=1, flags=re.S)
        if n != 1:
            raise ValueError(f"trecho do template não encontrado: {pattern[:40]}")
    out = Path(out) if out else source.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("markdown", nargs="+")
    args = parser.parse_args()
    for path in args.markdown:
        print(render(path))


if __name__ == "__main__":
    main()
