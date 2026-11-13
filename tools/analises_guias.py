# -*- coding: utf-8 -*-
"""Gera 4 guias originais de metodo (correlacao, grafico de dispersao em escala log, PPC, Gini) em rascunhos/guias/.
Numeros de exemplo calculados de paises.json (Banco Mundial). Uso: python -I tools/analises_guias.py"""
import json, pathlib, sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads(pathlib.Path(r"C:\Users\rodri\clients\watermouse-ferramentas\data\paises.json").read_text(encoding="utf-8"))
P = [p for p in D["paises"] if p.get("pop", 0) >= 1e6]
BR = next(p for p in P if p["iso3"] == "BRA")
n1 = lambda v: f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
n0 = lambda v: f"{v:,.0f}".replace(",", ".")
r2s = lambda v: f"{v:.2f}".replace(".", ",")
usd = lambda v: "US$ " + n0(v)


def corr(a, b, log=False):
    xs = [(p[a], p[b]) for p in P if p.get(a) is not None and p.get(b) is not None and (not log or p[a] > 0)]
    x = np.array([t[0] for t in xs], float); y = np.array([t[1] for t in xs], float)
    if log:
        x = np.log(x)
    return len(xs), float(np.corrcoef(x, y)[0, 1])


def lst(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " e " + items[-1]


NOTE = ("Guia original da Redação Watermouse Media, escrito para explicar conceitos que aparecem com frequência nas análises e nas notícias. "
        "Os números de exemplo são calculados por nós a partir de dados públicos do Banco Mundial.")
ATTR = ('<b>Sobre este guia:</b> texto original da Redação Watermouse Media, sem fonte-base única. Os exemplos usam dados do '
        '<a href="https://data.worldbank.org" target="_blank" rel="noopener">Banco Mundial, World Development Indicators</a> (atualização de out/2026), '
        'com cálculos da Watermouse Media. Veja a <a href="politica-editorial.html">política editorial</a>.')
CTX = '<!--ctx-->\n<h2>Para entender o contexto</h2>\n\n{t}'
guias = []


def guia(slug, title, dek, dek_card, og, image, alt, cap, body, read=7):
    assert chr(0x2014) not in body + title + dek
    s = dict(slug=slug, cat="mundo", cat_label="Mundo", title=title, dek=dek, dek_card=dek_card, og_desc=og, date_iso="2026-12-01T15:30:00-03:00",
             read_min=str(read), image="media/" + image, image_alt=alt, image_caption_html=cap, body_html=body, note=NOTE, attrib_html=ATTR)
    pathlib.Path(ROOT / "rascunhos" / "guias" / f"2026-11-13-{slug}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    guias.append(slug)


# ---------- 1. Correlacao nao e causa ----------
nv, rv = corr("pibpc", "vida", True)
nh, rh = corr("gini", "homic")
ns, rs = corr("saude", "vida")
nc, rc = corr("pibpc", "mata", True)
body = f"""<p>Quando uma análise diz que duas coisas "têm correlação", é fácil ler isso como "uma causa a outra". Não é. Correlação é uma medida de quanto duas variáveis andam juntas, e ela não diz por que andam. Este guia explica o que o número significa, como lê-lo e quais armadilhas aparecem ao comparar países, com exemplos das análises que publicamos com dados do Banco Mundial.</p>

<!--AD1-->

<h2>O que é o coeficiente de correlação</h2>

<p>O coeficiente de correlação (de Pearson, o mais usado) varia de -1 a +1. Perto de +1, as duas variáveis sobem juntas. Perto de -1, uma sobe quando a outra cai. Perto de zero, não há relação em linha reta. Nas nossas análises, a correlação entre o logaritmo do PIB por pessoa e a expectativa de vida de {nv} países é de {r2s(rv)}, muito forte. Entre a desigualdade (Gini) e os homicídios de {nh} países, é de {r2s(rh)}, moderada. E entre o gasto em saúde (% do PIB) e a expectativa de vida de {ns} países, é só {r2s(rs)}, fraca. Entre renda e área de floresta, é {r2s(rc)}, praticamente nula.</p>

<h2>Quanto da variação o número explica</h2>

<p>Elevando a correlação ao quadrado, obtém-se uma medida do quanto de uma variável é "explicado" pela outra em uma reta de tendência. Com r = {r2s(rv)}, o quadrado é {r2s(rv ** 2)}: a renda acompanha cerca de {n0(rv ** 2 * 100)}% da variação da expectativa de vida entre países. Com r = {r2s(rs)}, o quadrado é {r2s(rs ** 2)}: o gasto em saúde sozinho acompanha só cerca de {n0(rs ** 2 * 100)}% da variação. O restante vem de outros fatores que o cálculo não captura.</p>

<h2>Cinco armadilhas ao comparar países</h2>

<p><b>1. Um terceiro fator pode explicar os dois.</b> Sorvete e afogamentos sobem juntos no verão: o calor aumenta os dois, e um não causa o outro. Entre países, a renda costuma ser esse terceiro fator: ela se associa a escolaridade, saneamento, saúde e infraestrutura ao mesmo tempo.</p>

<p><b>2. A direção da causa pode ser a oposta.</b> Países com economia forte podem gastar mais em saúde, e países que gastam mais em saúde podem crescer mais. A correlação não mostra qual dos dois acontece, nem se os dois acontecem.</p>

<p><b>3. A média do país não é o indivíduo.</b> Uma relação entre países pode não valer entre pessoas dentro de um país. Isso é conhecido como falácia ecológica: tirar conclusões sobre indivíduos a partir de médias de grupos.</p>

<p><b>4. Poucos casos extremos pesam muito.</b> Um ou dois países muito diferentes podem puxar a correlação para cima ou para baixo. Por isso, nas nossas análises, usamos só países com 1 milhão de habitantes ou mais, o que exclui microestados que distorcem os números.</p>

<p><b>5. Os dados têm datas e métodos diferentes.</b> Os indicadores vêm do ano mais recente disponível de cada país, e cada país mede à sua maneira. Diferenças pequenas entre posições vizinhas quase sempre estão dentro da margem de erro.</p>

<h2>Como ler uma análise com correlação</h2>

<p>Três perguntas ajudam. O número é forte ou fraco, e qual é o tamanho da amostra? A análise aponta algum terceiro fator que poderia explicar a relação? E os autores tratam o resultado como associação, ou afirmam uma causa sem prova? Nas nossas análises, a seção final de cada texto lista os limites do cálculo justamente para isso.</p>

{CTX.format(t="A correlação de Pearson mede a força de uma relação linear entre duas variáveis. Quando a relação é curva, como a entre renda e expectativa de vida, é comum aplicar um logaritmo a uma das variáveis antes de calcular, o que deixa a relação mais próxima de uma reta. Veja o guia sobre gráficos de dispersão em escala logarítmica.")}"""
guia("guia-correlacao-nao-e-causa-comparar-paises-2026",
     "Correlação não é causa: como ler comparações entre países sem cair em armadilhas",
     "Correlação mede quanto duas coisas andam juntas, não por que andam. Veja o que o número significa, quando ele é forte ou fraco e as cinco armadilhas mais comuns ao comparar países, com exemplos reais do Banco Mundial.",
     "O que o coeficiente de correlação mostra, o que ele não prova e cinco armadilhas ao comparar países.",
     "Guia sobre correlação e causa: como ler o coeficiente de correlação, quanto da variação ele explica e cinco armadilhas ao comparar países, com exemplos do Banco Mundial.",
     "graf-gini-homicidios.jpg", "Gráfico de dispersão com índice de Gini e taxa de homicídios de 132 países, com uma linha de tendência",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (índice de Gini e homicídios por 100 mil habitantes).", body)

# ---------- 2. Grafico de dispersao em escala logaritmica ----------
body = f"""<p>Nas nossas análises de dados, o gráfico mais comum é o de dispersão: cada ponto é um país, e a posição mostra o valor de duas medidas ao mesmo tempo. Muitas vezes o eixo da renda aparece em "escala logarítmica", e isso confunde quem vê pela primeira vez. Este guia explica como ler esse tipo de gráfico, por que ele é útil e o que a linha pontilhada realmente mostra.</p>

<!--AD1-->

<h2>Como ler um gráfico de dispersão</h2>

<p>No eixo horizontal fica uma medida, como o PIB por pessoa. No vertical, outra, como a expectativa de vida. Cada país vira um ponto. Se os pontos formam uma nuvem inclinada de baixo para cima, as duas medidas sobem juntas. Se formam uma nuvem sem direção, não há relação clara. Para destacar um país, como o Brasil, ele costuma ter cor e rótulo próprios.</p>

<h2>Por que usar escala logarítmica</h2>

<p>As rendas dos países variam muito: o PIB por pessoa vai de poucas centenas a mais de cem mil dólares. Em escala comum (linear), os países pobres ficam amontoados à esquerda, e quase não se enxerga a diferença entre eles. Na escala logarítmica, cada divisão do eixo multiplica o valor por 10: de 1.000 para 10.000 e para 100.000, com o mesmo espaço entre uma marca e outra. Isso reflete algo intuitivo: passar de US$ 1.000 para US$ 2.000 por pessoa muda muito mais a vida do que passar de US$ 51.000 para US$ 52.000.</p>

<h2>O que a linha de tendência mostra</h2>

<p>A linha pontilhada é o melhor ajuste em linha reta aos pontos. No nosso gráfico de renda e expectativa de vida, ela indica que cada vez que a renda por pessoa dobra, a expectativa de vida sobe cerca de 3 anos, em média. Para o Brasil, com {usd(BR['pibpc'])} por pessoa e {n1(BR['vida'])} anos de expectativa de vida, o ponto fica perto da linha: a diferença para o valor previsto é pequena. Países acima da linha têm um resultado melhor do que a renda sugere, e os abaixo, pior.</p>

<h2>Três cuidados</h2>

<p><b>A linha é uma média, não uma lei.</b> Há países muito acima e muito abaixo dela, e vale olhar quem são. <b>Não confunda posição com causa.</b> Um país acima da linha pode ter feito bem em saúde ou ter dados mais favoráveis, e o gráfico sozinho não diz qual. <b>Cuidado com os eixos.</b> Em escala logarítmica, uma linha reta representa um crescimento proporcional, não constante. Sempre confira se o eixo diz "escala logarítmica".</p>

{CTX.format(t="Um logaritmo de base 10 diz a quantas vezes é preciso multiplicar 10 por si mesmo para chegar a um número: o logaritmo de 1.000 é 3 e o de 100.000 é 5. Por isso, nessa escala, a distância entre 1.000 e 10.000 é igual à distância entre 10.000 e 100.000. Veja também o guia sobre correlação e causa.")}"""
guia("guia-grafico-de-dispersao-escala-logaritmica-2026",
     "Como ler um gráfico de dispersão com escala logarítmica, passo a passo",
     "Cada ponto é um país, e a linha pontilhada mostra a tendência média. Veja como ler esse tipo de gráfico, por que a renda aparece em escala logarítmica e o que fazer ao ver um país acima ou abaixo da linha.",
     "Como ler pontos, eixos e a linha de tendência de um gráfico de dispersão, e por que a renda aparece em escala logarítmica.",
     "Guia sobre gráficos de dispersão: como ler os eixos, a escala logarítmica e a linha de tendência, com o exemplo de renda e expectativa de vida.",
     "graf-renda-vida.jpg", "Gráfico de dispersão com PIB por pessoa em escala logarítmica e expectativa de vida de 159 países, com o Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e expectativa de vida, valor mais recente).", body)

# ---------- 3. PPC ----------
pp = [p for p in P if p.get("pibppc") and p.get("pibpc")]
for p in pp:
    p["_rz"] = p["pibppc"] / p["pibpc"]
pp_s = sorted(pp, key=lambda p: p["_rz"], reverse=True)
mz = float(np.median([p["_rz"] for p in pp]))
usa = next(p for p in pp if p["iso3"] == "USA"); che = next(p for p in pp if p["iso3"] == "CHE")
body = f"""<p>Quanto vale um dólar? Depende de onde ele é gasto. Um corte de cabelo, uma refeição ou um aluguel custam muito menos em alguns países do que em outros, mesmo depois de converter tudo para dólares. A paridade de poder de compra, ou PPC, é a forma de corrigir essa diferença ao comparar a renda de países. Este guia explica a ideia, como ela é usada e por que o PIB por pessoa em PPC e em dólares correntes contam histórias diferentes.</p>

<!--AD1-->

<h2>O problema do câmbio</h2>

<p>Para comparar o PIB de países, é preciso uma moeda comum, e o mais simples é converter pela taxa de câmbio do mercado. O problema é que o câmbio reflete o preço de moedas, não o de uma cesta de compras. Com a mesma renda em dólares, uma pessoa vive de forma bem diferente em lugares com custo de vida diferente. O câmbio também oscila: uma desvalorização forte da moeda derruba o PIB em dólares sem que as pessoas tenham ficado materialmente mais pobres no dia seguinte.</p>

<h2>A ideia da paridade de poder de compra</h2>

<p>A PPC compara quanto custa a mesma cesta de bens e serviços em cada país, e define uma taxa de conversão em que essa cesta custa o mesmo. Uma unidade da moeda "dólar internacional" compra, em teoria, o mesmo que um dólar nos Estados Unidos. As estimativas vêm do Programa de Comparação Internacional, coordenado pelo Banco Mundial, que coleta preços em mais de uma centena de economias. Um exemplo informal da ideia é o "índice Big Mac", criado pela revista The Economist em 1986, que compara o preço do mesmo sanduíche em vários países.</p>

<h2>Na prática: a razão entre PPC e dólares correntes</h2>

<p>Dividindo o PIB por pessoa em PPC pelo PIB por pessoa em dólares correntes, obtém-se uma razão que mostra quanto mais (ou menos) o dinheiro rende em cada lugar. Entre {len(pp)} países com 1 milhão de habitantes ou mais, a mediana é de {n1(mz)} vezes. O Brasil tem {usd(BR['pibpc'])} por pessoa em dólares correntes e {usd(BR['pibppc'])} em PPC, uma razão de {n1(BR['pibppc'] / BR['pibpc'])} vezes. Nos Estados Unidos, a razão é de {n1(usa['_rz'])} (por definição, perto de 1), e na Suíça, de {n1(che['_rz'])}, onde o custo de vida é alto. Entre os países com razão mais alta aparecem {lst(f"{p['nome']} ({n1(p['_rz'])} vezes)" for p in pp_s[:3])}.</p>

<h2>Quando usar cada medida</h2>

<p>O PIB por pessoa em dólares correntes é útil para comparar o tamanho da economia em termos internacionais, como a capacidade de importar bens e pagar dívidas em dólar. O PIB por pessoa em PPC é mais adequado para comparar o padrão de vida e o poder de consumo local. Nenhuma das duas mede desigualdade, qualidade dos serviços públicos ou bem-estar, e as estimativas de PPC são revistas periodicamente, com dados mais incertos em países com preços instáveis.</p>

{CTX.format(t="O PIB por pessoa em PPC é expresso em dólares internacionais correntes. Veja o ranking completo na nossa página de ferramentas e a análise sobre quanto um dólar rende em cada país.")}"""
guia("guia-paridade-de-poder-de-compra-ppc-explicada-2026",
     "Paridade de poder de compra (PPC): por que um dólar rende diferente em cada país",
     "Comparar rendas só pelo câmbio engana, porque preços variam muito entre países. A PPC corrige isso. Entenda a ideia, de onde vêm os dados, como o Brasil aparece e quando usar PIB em PPC ou em dólares correntes.",
     "O que é PPC, por que o câmbio distorce comparações de renda e quando usar cada medida de PIB por pessoa.",
     "Guia sobre paridade de poder de compra: o que é a PPC, como ela corrige o câmbio, exemplos com o Brasil e quando usar PIB em PPC ou em dólares correntes.",
     "graf-poder-de-compra.jpg", "Gráfico de barras horizontais com a razão entre PIB por pessoa em PPC e em dólares correntes, com o Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB per capita em PPC e em dólares correntes).", body)

# ---------- 4. Gini ----------
gi = sorted([p for p in P if p.get("gini") is not None], key=lambda p: p["gini"])
body = f"""<p>O índice de Gini é um número entre 0 e 100 que resume o quanto a renda de um país está concentrada. É a medida de desigualdade mais usada em comparações internacionais, e aparece com frequência nas notícias e nas nossas análises. Este guia explica de onde vem o índice, como lê-lo e o que ele não mostra.</p>

<!--AD1-->

<h2>De onde vem a medida</h2>

<p>O índice leva o nome do estatístico italiano Corrado Gini, que o propôs em 1912. Ele se baseia na curva de Lorenz, desenhada pelo economista americano Max Lorenz em 1905: ordena-se a população do mais pobre ao mais rico e mostra-se que fatia da renda total fica com cada parcela das pessoas. Se todos ganhassem o mesmo, a curva seria uma reta diagonal. Quanto mais ela se afasta da diagonal, maior o Gini.</p>

<h2>Como ler o número</h2>

<p>Em 0, todos teriam exatamente a mesma renda. Em 100, uma pessoa ficaria com tudo. Na prática, os valores dos países com dado vão de {n1(gi[0]['gini'])} a {n1(gi[-1]['gini'])} nos dados do Banco Mundial. Entre {len(gi)} países com 1 milhão de habitantes ou mais e dado disponível, os menores valores são os de {lst(f"{p['nome']} ({n1(p['gini'])})" for p in gi[:3])}, e os maiores, os de {lst(f"{p['nome']} ({n1(p['gini'])})" for p in gi[::-1][:3])}. O Brasil tem {n1(BR['gini'])}.</p>

<h2>Cuidados ao comparar</h2>

<p><b>Renda ou consumo.</b> Em alguns países o Gini é calculado com a renda das famílias, em outros com o consumo, e o consumo costuma ser menos desigual. <b>Ano da pesquisa.</b> Os dados vêm de pesquisas domiciliares feitas em anos diferentes por cada país, e países sem pesquisa recente ficam de fora. <b>Antes ou depois de impostos.</b> Há versões que medem a renda antes e outras depois de impostos e transferências, e os números não são comparáveis entre si.</p>

<h2>O que o Gini não mostra</h2>

<p>O Gini resume uma distribuição inteira em um número, e por isso esconde onde está a diferença. Dois países com o mesmo Gini podem ter distribuições muito diferentes: em um, os mais ricos concentram quase tudo, e no outro, a diferença está entre a classe média e os pobres. O índice também não diz nada sobre o nível de renda: um país pode ter Gini baixo e ser pobre. Por isso as nossas análises sempre colocam o Gini ao lado de outras medidas, como o PIB por pessoa.</p>

{CTX.format(t="No Brasil, as estatísticas oficiais de desigualdade vêm principalmente da Pesquisa Nacional por Amostra de Domicílios (PNAD) do IBGE, e os números podem diferir dos do Banco Mundial pela metodologia. Veja também a nossa análise sobre desigualdade e renda.")}"""
guia("guia-indice-de-gini-como-ler-desigualdade-2026",
     "Índice de Gini: como ler o número que mede a desigualdade de renda",
     "O Gini vai de 0 (igualdade total) a 100 (uma pessoa fica com tudo). Entenda de onde vem o índice, como comparar países, quais valores aparecem no mundo e o que o número esconde.",
     "O que o índice de Gini mede, como ler os valores e os cuidados ao comparar a desigualdade entre países.",
     "Guia sobre o índice de Gini: origem, como ler os valores de 0 a 100, exemplos com o Brasil e limites da medida de desigualdade.",
     "graf-gini-renda.jpg", "Gráfico de dispersão com PIB por pessoa em escala logarítmica e índice de Gini de 145 países, com o Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e índice de Gini, valor mais recente).", body)
print("ok", guias)
