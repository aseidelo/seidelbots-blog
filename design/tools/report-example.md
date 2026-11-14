---
# Modelo de relatório técnico. Copie para docs/reports/<nome>.md no repositório do projeto e gere com:
#   uv run ~/Projetos/git/seidelbots-blog/design/tools/render_report.py docs/reports/<nome>.md
title: A claim, not a question — what the report shows
abstract: Two or three sentences. What goes in, what comes out, and the headline number.
number: CLM-TR-2026-01
version: "1.0"
status: draft            # draft | final
author: Seidel
published: 2026-11-13
updated: 2026-11-13
project: code-language-model
license: MIT · CC BY 4.0
blog:                    # link do post no seidelbots.com, quando houver
stats:
  - {value: "8.5%", label: "HumanEval pass@1"}
  - {value: "113M", label: "parameters"}
highlights:
  - One line per key finding.
changelog:
  - {version: "1.0", date: 2026-11-13, note: First release.}
---

## Motivation

Each `##` heading is a numbered section and goes into the table of contents.

## Method

### 2.1 A subsection

> [!NOTE]
> Notes and caveats use GitHub's callout syntax (`[!NOTE]`, `[!WARNING]`).

![Training loss](figures/loss.png "Figure 1. Caption under the figure.")

## Results

| Configuration | pass@1 | tokens |
|---|---:|---:|
| baseline | 4.1% | 2.0B |
| this run | 8.5% | 10B |

**Table 1.** A paragraph that starts with "Table N." right after a table is its caption.

## Reproducing

```bash
uv run python -m eval.passk --checkpoint base-v2/step-43938 --mode completar
```
