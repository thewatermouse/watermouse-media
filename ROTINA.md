# Rotina do portal — Watermouse Media (media.thewatermouse.com)

Manual para montar e publicar as matérias do dia do portal de notícias **@watermousemedia**.
O site é estático (GitHub Pages, repo nesta pasta). Publicar = commit + push para a branch `main`.

Responda sempre em **português do Brasil**. Peça a aprovação do Rodrigo **antes de dar push** (publicar) e antes de postar qualquer coisa no Instagram.

---

## 1. O que é / regras (NUNCA quebrar)

- **Nicho:** notícias internacionais **fora do radar** da imprensa brasileira — ciência, cultura, mundo, tecnologia, negócios. Priorize histórias boas e pouco cobertas aqui; evite a manchete que todo portal já deu.
- **Zero invenção.** Só reescreva notícia **pública e com fonte**. Todo fato vem da fonte original; nada de número, nome, data ou citação que não esteja na fonte. Na dúvida, corte.
- **Uma fonte principal por matéria**, citada e linkada no bloco `.attrib`. O texto é cobertura própria em PT (não é tradução), mas os fatos são atribuídos ("segundo X").
- **Nota de cautela** sempre que algo for alegação/expectativa e não fato consolidado (ex.: "é a avaliação do ministro, não conclusão científica"). Isso é marca da casa.
- **Pessoas citadas: não inferir gênero pelo nome.** Pesquisadores, autores e fontes citados por nome só entram com forma neutra, porque as fontes quase nunca dizem o gênero. Escreva "Fulano, da Universidade X (área de física)", "assina como primeira autoria", "lidera o projeto", "diz Fulano"; evite "o físico", "a geoquímica", "o doutorando", "a autora principal", "o professor" etc. Só use forma marcada se a fonte trouxer o gênero ou o pronome. Vale também para este manual e para legendas de reels.
- **Nada de:** morte/tragédia explorada, doença de pessoa específica, menores identificáveis, crime não confirmado, discurso de ódio.
- **Imagens:** só **domínio público ou Creative Commons** (NASA/ESA, Wikimedia Commons), **com crédito** na `figcaption`. Nunca foto de agência/paparazzi. Cheque se não tem criança identificável.
- **Categorias** (id/classe no site): `mundo`, `tecnologia`, `ciencia`, `negocios`, `cultura`. Rótulos: Mundo, Tecnologia, Ciência, Negócios, Cultura.

## 2. Quantidade

1 a 2 matérias por dia. Qualidade > volume.

## 3. Passo a passo

### a) Escolher a(s) notícia(s)
- Use busca na web por notícias internacionais recentes e **subcobertas** no Brasil (preferir estudo/relatório/achado interessante). Leia a **matéria/estudo ORIGINAL** inteiro antes de escrever (WebFetch na fonte).
- Defina: categoria, manchete (h1), linha-fina (dek), e a fonte (nome + URL).

### b) Criar o arquivo HTML da matéria

> **Atalho (use este):** escreva um JSON de especificação e rode `python -I tools/build_article.py spec.json` na raiz do repo. Ele faz TUDO dos passos b, d e dos itens de sitemap/feed/link na bio abaixo (clona a matéria mais recente da mesma categoria, troca os campos, insere os cards, atualiza `sitemap.xml`, `feed.xml` e `links/index.html`). Os campos do JSON estão no cabeçalho do próprio script; o corpo vai em `body_html` com `<!--AD1-->` marcando o 1º anúncio do meio. Ele **não** faz commit nem push. Falta só a imagem (passo c, em `media/`) e a aprovação (passo e). Exemplo real: matéria `geleiras-suicas-perda-gelo-2026`. Os passos manuais abaixo ficam como referência do que o script faz.

- **Clone uma matéria REAL já existente da MESMA categoria** como base (ex.: `encelado-oceano-vida-2026.html` para Ciência). Assim você herda `<head>` (GA, fontes, AdSense, estilos `.hero-fig`, slots de anúncio), header, rodapé e banner de cookies prontos. **Não** use `noticia-modelo.html` (ele tem `.hero-img` gradiente e tarja de exemplo).
- Nome do arquivo: slug curto + `-2026.html` (ex.: `cidade-finlandesa-4-dias-2026.html`).
- Troque **só** estes pontos (mantenha todo o resto igual, inclusive os dois `div.ad-slot` com os `data-ad-slot` 8356866030 e 7043784364):
  - `<title>` → "Manchete | Watermouse Media"
  - `<link rel="canonical">`, `og:title`, `og:description`, `og:url` → novo arquivo/manchete/dek
  - `<meta name="description">` → resumo real
  - Bloco JSON-LD `NewsArticle`: `headline`, `description`, `datePublished`/`dateModified` (data de hoje, `-03:00`), `articleSection` (categoria), `mainEntityOfPage` (novo arquivo), `isBasedOn` (URL da fonte)
  - `<div class="a-cat">` → rótulo da categoria
  - `<h1>` → manchete
  - `<p class="dek">` → linha-fina
  - `<div class="meta">` → `Por <b>Redação Watermouse Media</b>` · data por extenso (ex.: "29 de setembro de 2026") · "X min de leitura"
  - `<figure class="hero-fig">`: `<img src="media/ARQUIVO.jpg" alt="descrição" loading="lazy">` + `<figcaption>` com descrição + "Crédito: ...".
  - `<div class="body">`: parágrafos `<p>` (4 a 8), 1 a 2 `<h2>`, **mantendo os dois `ad-slot` onde estão** (um no meio do corpo, outro depois). Pode usar `*trechos*`? Não — aqui é HTML, use `<strong>` se precisar destacar, com moderação.
  - Bloco `.attrib`: `<b>Fonte:</b> com base em reportagem de <a href="URL" ...>[Veículo]</a>.` + a nota padrão. **Remova** qualquer `.example-note`.

### c) Imagem (domínio público / CC)
- Busque no Wikimedia Commons (API `generator=search&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata|size|mime&iiurlwidth=1440`), filtrando `LicenseShortName` por Public domain / CC0 / CC BY / CC BY-SA, só `image/jpeg`/`image/png`, largura ≥ 1100. Salve em `media/ARQUIVO.jpg`. Anote o crédito (Artist) para a `figcaption` e, se for CC BY/BY-SA, cite o autor.
- **O Commons às vezes devolve 429 (rate limit).** Faça backoff (espere 15-30s e tente de novo, até ~4x). Se mesmo assim falhar, deixe o `<figure>` com uma classe `hero-img` (gradiente, sem crédito) como placeholder e avise o Rodrigo que a imagem ficou pendente.

### d) Inserir os cards (senão a matéria fica órfã)
O card tem este formato (copie um card EXISTENTE da mesma categoria para herdar as classes certas e troque só href, img, alt, h3 e dek):
```html
<a href="ARQUIVO.html" class="card"><div class="card-img CAT"><img src="media/ARQUIVO.jpg" alt="" loading="lazy"></div><span class="chip CAT">Rótulo</span><h3>Manchete</h3><p class="dek">Linha-fina curta.</p></a>
```
- **Na home (`index.html`):** ache a seção `<section class="cat-sec" id="CATEGORIA">` → dentro do `<div class="grid">` insira o card novo como **primeiro** (antes do primeiro card existente = mais recente no topo).
- **Na página da categoria (`CATEGORIA.html`, ex.: `ciencia.html`):** o container ali é `<div class="cat-grid">` (diferente da home, que usa `<div class="grid">`). Insira o card novo antes do primeiro `<a href=... class="card">` dentro dele.
- **`sitemap.xml`:** acrescente `<url><loc>https://media.thewatermouse.com/SLUG.html</loc><lastmod>AAAA-MM-DD</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>` logo depois da entrada da home, e atualize o `lastmod` da home para hoje.
- **`feed.xml` (RSS):** acrescente um `<item>` (title, link, guid, pubDate em RFC-822 com `-0300`, category, description) como PRIMEIRO item e atualize `<lastBuildDate>`.
- **Página "link na bio" (`links/index.html`):** depois de atualizar o `feed.xml`, rode `python -I tools/build_links.py` na raiz do repo. Ela lista as 6 matérias mais recentes do feed (com UTM do Instagram) e é o link que está na bio do @watermousemedia (`https://media.thewatermouse.com/links`). Inclua `links/index.html` no commit.
- Referência de implementação: o script que gerou a matéria de Kikai (clone do Encélado + regex nos campos + cards + sitemap + feed) é um bom modelo; os pontos de troca são exatamente os listados no passo b.

### e) Aprovação
- Mostre ao Rodrigo: manchete, categoria, dek, a fonte (link) e um resumo do corpo. Se útil, abra o arquivo no navegador interno para ele ver. **Não dê push sem o "sim" dele.**

### f) Publicar (deploy)
- `git add -A` → `git commit -m "Nova matéria: <slug> (<categoria>)"` → `git push`.
- Encerre a mensagem de commit com: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
- **Nunca** use travessão (—, em-dash) em nada; depois de escrever, confira com busca por `—`.

### g) (Opcional, com OK) Alimentar a fila de Reels
- Para levar a matéria ao Instagram, adicione um reel em `posts/fila/posts.json` (schema em `tools/make_reel.py`: `cover` com a imagem + `cenas` com `fala`/`tela`/`foto`, roteiro **fiel**), renderize com `python -I tools/make_reel.py posts/fila <id>` e deixe pronto. A tarefa `reels-diario` publica depois, com aprovação.

## 4. Se algo quebrar

Diga exatamente o que falhou (fonte fora do ar, Commons em rate limit, erro de git/push) e siga com o que der. Nunca publique com fato não conferido.
