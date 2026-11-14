# Seidelbots — design system foundations

Personal site for Seidel: a markdown blog about agentic AI, plus a shelf of deployed
projects, each on its own subdomain (`ledger.seidelbots`, `scout.seidelbots`…).
Framing: a robot outfitter on a far-off planet selling retrofits to passing ships.

Source of truth for the visual language: `Seidelbots.dc.html` in this project
(the Showroom direction, turns 1 and 2).

## Files

- `styles.css` — entry point, imports everything below
- `tokens/fonts.css` — Syne + Public Sans from Google Fonts
- `tokens/colors.css` — light and dark palettes, semantic aliases
- `tokens/typography.css` — the type scale and its markdown mapping
- `tokens/shape.css` — borders, radii, offset shadows, spacing
- `Foundations.dc.html` — visual specimen of the type scale and both palettes

## Visual foundations

**Sticker objects.** Every card, pill, badge and tile is a 2px ink outline with a
14px radius and a 2px solid offset shadow in the same ink (1px on pills). No blur,
no gradients, no transparency anywhere. Dark mode keeps that ink near-black
(`--edge` and `--shadow-ink`, `#0e0c14`) and lifts the GROUND instead — canvas
`#262035`, cards `#332b47` — so the outline and the offset both still read.
`--slab` (`#1d1a24` / `#0e0c14`) is the one field that is dark in both modes:
the code-block header and the project-shell bar.

**One ink.** `--ink` is the primary text color; `--edge` / `--shadow-ink` draw
every border and shadow. They are the same value in light mode and diverge only
in dark, where text goes light and the ink stays dark. Greys are for text only,
never for structure.

**Header.** The wordmark is a sticker too: "Seidelbots" in Syne 800/18px inside a
`--surface` plate with the standard border and 2px offset. Nav items are pills —
amber when active, transparent otherwise — and the theme toggle is a square
outlined button holding ☾ / ☀.

**Accents are fields, not ink.** Violet is identity, amber is writing, green is
shipped. They appear as backgrounds — nav pills, tags, hero bands, callouts — and
text on them is always `--on-accent`. A control sitting inside an accent field
uses `--on-accent-surface`, which stays light in both modes. Never colored body
text, never colored links.

**Type.** Syne 800/700 for anything short and loud, with negative tracking.
Public Sans for anything anyone reads. Monospace only for machine strings:
subdomains, file names, code, stock codes. Micro labels are uppercase and tracked out.

**Illustration.** The identity depends on a recurring cartoon icon set (Telegram-doc
flavored): one drawing per project, one per post category, one per empty state, plus
margin diagrams in posts. Until those exist, every slot is a hatched tile
(`--hatch`) with a monospace label naming what belongs there. Those labels are
specifications, not decoration — the drawings are not yet made.

**Layout.** 900px content frame, 34px gutters, prose column plus a 210px sidebar
holding the table of contents, margin notes and cross-links. Lists are dense and
newest-first; posts and projects share one stream.

**Copy.** First person, matter-of-fact, no exclamation marks and no emoji. Titles
are claims ("Tool-use is the drivetrain, not the engine"), not questions. Project
descriptions say what goes in and what comes out. The shop metaphor is allowed in
headings and empty states, never in technical explanation.

## Pages

`Seidelbots Site.dc.html` is the working prototype built entirely on these tokens:
home index, writing index, single post, projects shelf, about, project-subdomain
shell and 404, with the light/dark toggle persisted to `localStorage`.
`Seidelbots.dc.html` holds the original design exploration.

## Not yet built

Reusable components, the icon set, and the cartoon illustrations every hatched
slot is waiting for.
