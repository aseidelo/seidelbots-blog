---
title: How this shop works
dek: A markdown blog and a shelf of subdomains, built with Astro and this design system.
pubDate: 2026-09-15
category: Note
tags: [meta]
---

This is a template post — replace it with your first real one, or delete it.

Everything here is markdown. Frontmatter drives the list pages (`title`, `dek`,
`pubDate`, `category`, `tags`), and this body renders through the `.prose`
styles in `src/styles/global.css`, which map headings, code blocks, tables and
quotes onto the type scale in `src/styles/tokens/typography.css`.

## Headings look like this

Public Sans carries the paragraphs, Syne carries anything short and loud.

> Blockquotes sit in a dashed violet-tinted box — used sparingly, for a claim
> worth setting apart from the surrounding argument.

A code block, for machine strings:

```python
def lookup(order_id: str) -> Status:
    row = db.get(order_id)
    return Status(state=row.state, eta=row.eta)
```

And a table, for anything that wants columns:

| Change | Result |
| --- | --- |
| Baseline | 61% |
| Trimmed payloads | 78% |

Projects live in `src/data/projects.ts`, not as posts — add one there once it
has a subdomain to point at.

## Another header

Oi tudo bom?

```bash
./install.sh
```

dassaddasdass