# Design de referência

Material de referência do Claude Design. Não entra no build do site: o deploy publica só `dist/` e
`src/content/posts/`.

- `templates/` — fundações do design system (`styles.css`, `tokens/`, `Foundations.dc.html`), os
  protótipos do site (`Seidelbots.dc.html`, `Seidelbots Site.dc.html`) e três templates de página
  para os repositórios de projeto:
  - `technical-report.html` — relatório técnico (`docs/reports/` de cada projeto);
  - `benchmark.html` + `render_benchmark.py` — página de uma rodada de benchmark, gerada a partir
    de um JSON de resultados;
  - `human-validation.html` — página de revisão humana de exemplos de dataset (estática ou servida
    por um servidor local).

Os tokens em uso pelo site estão em `src/styles/tokens/`; os daqui são a cópia original.
