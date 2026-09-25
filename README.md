# seidelbots-blog

Blog estático em [Astro](https://astro.build) para [seidelbots.com](https://seidelbots.com).
Markdown vira post, deploy é estático (S3 + CloudFront).

## Estrutura

- `src/content/posts/*.md` — posts (frontmatter: `title`, `dek`, `pubDate`, `category`, `tags`, `draft`)
- `src/data/projects.ts` — o "shelf" de projetos (cada um aponta pro seu próprio subdomínio)
- `src/config.ts` — título, descrição, links sociais do site
- `src/styles/tokens/` — design tokens (cores, tipografia, forma) vindos do `Seidelbots` no Claude Design
- `src/layouts/BaseLayout.astro` — header, nav, toggle de tema, footer

## Comandos

| Comando           | Ação                                      |
| ------------------ | ------------------------------------------ |
| `npm install`       | Instala dependências                       |
| `npm run dev`       | Dev server em `localhost:4321`             |
| `npm run build`     | Build estático em `./dist/`                |
| `npm run preview`   | Preview do build de produção               |

## Escrever um post

A pasta é o idioma. Criar `src/content/posts/en/nome-do-post.md` (ou `pt/`):

```md
---
title: Título
dek: Uma linha resumindo o post.
pubDate: 2026-09-15
category: Essay
tags: [agents]
---

Corpo em markdown.
```

### Traduzir

Dois arquivos com o **mesmo nome** em `en/` e `pt/` são o mesmo post em dois
idiomas. Eles compartilham uma única URL (`/writing/nome-do-post/`), que traz as
duas versões, e um toggle EN/PT escolhe qual aparece — a escolha do leitor fica
no `localStorage` e vale para os próximos posts.

Post que existe em um idioma só funciona normalmente: o botão do idioma que
falta aparece desabilitado. Nas listagens, no RSS e nas tags o post aparece uma
vez só, em inglês quando existe, senão no idioma em que foi escrito.

Título, `dek`, `tags` e data são por arquivo, então cada idioma tem os seus. O
`<title>` e a meta description da aba ficam sempre no idioma primário, já que
são únicos por URL.
## Fluxo de trabalho

Para atualizar o blog, criar branch `feat/<nome>` e publicá-la no remoto. O
`.github/workflows/open-pr.yml` valida e, se passar, **abre o PR para a `main`
sozinho**. O merge do PR dispara o deploy.

```
git switch -c feat/meu-post
git push -u origin feat/meu-post   # valida e abre o PR
```

A validação (`.github/workflows/validate.yml`, compartilhada) tem três checks,
nenhum deles toca na AWS:

| Check | O que faz |
| ----- | --------- |
| `validate / branch-name` | Exige o padrão `feat/<nome>` |
| `validate / verify`      | `npm run check` + `npm run build` |
| `validate / secrets`     | gitleaks no histórico completo |

A `main` exige PR com esses três checks verdes. O `ci.yml` roda a mesma
validação em PR aberto na mão; o PR automático não dispara esse gatilho — PR
criado com o `GITHUB_TOKEN` não dispara workflow de `pull_request` —, mas os
checks já ficaram ancorados no commit e aparecem verdes no PR do mesmo jeito.

## Deploy

GitHub Actions, a cada push na `main` (`.github/workflows/deploy.yml`):
build estático → `s3 sync` no bucket → invalidação do CloudFront.
Também dá pra disparar na mão pela aba Actions (`workflow_dispatch`).

O job que tem credencial AWS não executa código do repo — ele só recebe o
artefato pronto do job de build. A autenticação é via OIDC (sem chave de longa
duração): a role só pode ser assumida por este repo, na branch `main`.

Layout do bucket:

```
s3://<bucket>/
├── content/
│   ├── static/    Origin Path do CloudFront — o site buildado
│   └── writings/  markdown dos posts, publicado mas fora do alcance do CDN
└── logs/
    └── cloudfront/
```

O Origin Path faz o CloudFront prefixar toda requisição com `content/static`, então
nada fora dali é alcançável pela web. O markdown em `content/writings/` é uma cópia
publicada da fonte; quem alimenta o build continua sendo `src/content/posts/`.

Cache: `_astro/*` tem hash no nome e vai com `max-age` de 1 ano (`immutable`);
HTML, feed e favicons vão com `max-age=0, must-revalidate`.
