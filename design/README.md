# Design de referência

Material de referência do Claude Design. Não entra no build do site: o deploy publica só `dist/` e
`src/content/posts/`.

- `templates/` — fundações do design system (`styles.css`, `tokens/`, `Foundations.dc.html`), os
  protótipos do site (`Seidelbots.dc.html`, `Seidelbots Site.dc.html`) e três templates de página
  para os repositórios de projeto:
  - `technical-report.html` — relatório técnico com cara de documento (folha com borda, só tema
    claro), preenchido pelo `tools/render_report.py`;
  - `benchmark.html` + `render_benchmark.py` — página de uma rodada de benchmark, gerada a partir
    de um JSON de resultados;
  - `human-validation.html` — página de revisão humana de exemplos de dataset (estática ou servida
    por um servidor local).
- `templates/post-example/` — o post-modelo "How this shop works" (en e pt): mostra o frontmatter e
  como cada elemento de markdown (títulos, citação, código, tabela) aparece no tema. A cópia publicada
  fica em `src/content/posts/`.

Os tokens em uso pelo site estão em `src/styles/tokens/`; os daqui são a cópia original.

## Ferramentas

- `tools/render_report.py` — gera o relatório técnico em HTML a partir de um markdown com front
  matter, no template `templates/technical-report.html`. Roda de qualquer repositório de projeto
  (o `uv` resolve as dependências) e grava o HTML ao lado do markdown, com repositório e commit
  tirados do git da pasta dele:

      uv run ~/Projetos/git/seidelbots-blog/design/tools/render_report.py docs/reports/<nome>.md

  O modelo comentado, com todos os elementos (seções, nota, figura, tabela, código), está em
  `tools/report-example.md`.
